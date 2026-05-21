<!-- Modelo recomendado: claude-sonnet-4-5 -->
# Skill: /destravar-sessao

Destrava sessão Claude Code dentro do Antigravity quando o chat para de responder por causa de imagem corrompida que dispara `API Error: 400 Could not process image`. Edita o `.jsonl` da conversa cirurgicamente: remove blocos `type=image` do histórico, preserva todo o texto, mantém `tool_use_id` pareado.

> **Sintoma:** toda mensagem nova ("oi", qualquer texto) devolve `{"type":"error","error":{"type":"invalid_request_error","message":"Could not process image"}}`. Causa: um print PNG colado virou bloco `image` base64 no histórico e a API rejeita ao re-enviar como contexto.

> Procedimento validado 2 vezes (18/05/2026). Histórico: `segundo-cerebro/03-operacao/antigravity-historico.md` (a criar se inexistente).

## Quando invocar

- Sessão para de responder com erro 400 "Could not process image"
- Mensagens novas estouram sem nem o Claude começar a pensar
- Confirmado que a aba foi fechada e dá pra editar o arquivo

## Inputs

| Campo | Tipo | Obrigatório | Default |
|---|---|---|---|
| `session_id` | UUID | sim | — (UUID do `.jsonl`) |
| `project_dir` | path | sim | — (pasta em `~/.claude/projects/`) |

Pra descobrir o UUID da sessão travada: nome da aba no header da janela Antigravity bate com o nome do arquivo `.jsonl` no projects dir.

## Pré-requisitos OBRIGATÓRIOS

1. **Aba fechada no Antigravity.** Senão tem handle aberto e write pode corromper.
2. **Confirmar com {{NOME_OPERADOR}}** que aba foi fechada (uma confirmação explícita por execução).

## Fluxo

### Passo 1 — Inventário e backup

```bash
cd ~/.claude/projects/$PROJECT_DIR
ls -la $SESSION_ID.jsonl*
```

Regras de backup (NÃO sobrescrever histórico):
- `.bak` original (primeiro snapshot pré-qualquer-cleanup): **NUNCA sobrescrever**
- `.bak2`: snapshot pré-cleanup desta rodada. Se já existir de rodada anterior, renomear pra `.bak2-pre-rodadaN` antes de criar novo
- `.bak-*` com timestamp Unix: backup automático do Claude Code, deixar intocado

```bash
# Se .bak2 já existir, renomear preservando
if [ -f "$SESSION_ID.jsonl.bak2" ]; then
  TS=$(date +"%H%M")
  mv "$SESSION_ID.jsonl.bak2" "$SESSION_ID.jsonl.bak2-pre-${TS}"
fi
cp "$SESSION_ID.jsonl" "$SESSION_ID.jsonl.bak2"
```

### Passo 2 — Diagnóstico

```bash
wc -l $SESSION_ID.jsonl
grep -c '"type":"image"' $SESSION_ID.jsonl
```

Se contagem `"type":"image"` = 0, parar — não tem imagem pra limpar (problema é outro).

### Passo 3 — Localizar linhas com imagem

```bash
grep -n '"type":"image"' $SESSION_ID.jsonl | cut -d: -f1 | while read n; do
  size=$(awk -v ln="$n" 'NR==ln {print length($0)}' $SESSION_ID.jsonl)
  echo "linha $n: $size bytes"
done
```

```python
python3 <<'EOF'
import json
path = '$SESSION_ID.jsonl'
with open(path) as f:
    for i, line in enumerate(f, 1):
        if len(line) < 50000:
            continue
        obj = json.loads(line)
        role = obj.get('message', {}).get('role') or obj.get('type')
        content = obj.get('message', {}).get('content', [])
        attachment = obj.get('attachment')
        types = [b.get('type') for b in content if isinstance(b, dict)] if isinstance(content, list) else []
        att_types = [b.get('type') for b in attachment['prompt'] if isinstance(b, dict)] if attachment and isinstance(attachment.get('prompt'), list) else []
        print(f"linha {i}: role={role} content_types={types} attachment_types={att_types}")
EOF
```

### Passo 4 — Tratamento cirúrgico (Python, NUNCA sed/awk)

Regras:
- `message.content` (lista): remover blocos `type=image`, manter `type=text`
- `attachment.prompt` (lista): remover blocos `type=image`, manter `type=text`. Se ficar vazio → dropar linha inteira
- `tool_result.content`: substituir bloco `image` por `{"type":"text","text":"[image removed]"}`. NUNCA dropa a linha (preserva `tool_use_id` pareado)
- `toolUseResult.file.base64` (metadata interna Claude Code): NÃO TOCAR

Script:

```python
python3 <<'EOF'
import json
src = '$SESSION_ID.jsonl'
dst = src + '.new'
removed_count = 0
dropped_lines = 0
total_in = 0
total_out = 0

with open(src) as fin, open(dst, 'w') as fout:
    for line in fin:
        total_in += 1
        try:
            obj = json.loads(line)
        except:
            fout.write(line)
            total_out += 1
            continue

        # message.content
        msg = obj.get('message')
        if msg and isinstance(msg.get('content'), list):
            new_content = []
            for b in msg['content']:
                if isinstance(b, dict) and b.get('type') == 'image':
                    # Em tool_result, substituir; em user message, remover
                    if msg.get('role') == 'user' and any(isinstance(x, dict) and x.get('type') == 'tool_result' for x in msg['content']):
                        # raro — fall-through
                        removed_count += 1
                        continue
                    removed_count += 1
                    continue
                if isinstance(b, dict) and b.get('type') == 'tool_result' and isinstance(b.get('content'), list):
                    new_tr_content = []
                    for tr in b['content']:
                        if isinstance(tr, dict) and tr.get('type') == 'image':
                            new_tr_content.append({"type": "text", "text": "[image removed]"})
                            removed_count += 1
                        else:
                            new_tr_content.append(tr)
                    b = dict(b)
                    b['content'] = new_tr_content
                new_content.append(b)
            msg['content'] = new_content

        # attachment.prompt
        att = obj.get('attachment')
        if att and isinstance(att.get('prompt'), list):
            new_prompt = [b for b in att['prompt'] if not (isinstance(b, dict) and b.get('type') == 'image')]
            removed = len(att['prompt']) - len(new_prompt)
            removed_count += removed
            if not new_prompt:
                dropped_lines += 1
                continue
            att['prompt'] = new_prompt

        fout.write(json.dumps(obj, ensure_ascii=False) + '\n')
        total_out += 1

print(f"linhas entrada: {total_in}")
print(f"linhas saida:   {total_out}")
print(f"linhas dropadas:{dropped_lines}")
print(f"imagens tratadas: {removed_count}")
EOF
```

### Passo 5 — Preview e gate manual

Reportar pro {{NOME_OPERADOR}} antes do `mv`:
- Linhas antes/depois
- Tamanho antes/depois
- `"type":"image"` antes/depois (alvo: 0)
- Validação JSONL: `python3 -c "import json; [json.loads(l) for l in open('$SESSION_ID.jsonl.new')]"`
- Amostra antes/depois por categoria (base64 truncado em 50 chars)

**PARAR. Aguardar "aprovado" explícito do {{NOME_OPERADOR}}.** Não executar `mv` sem aval.

### Passo 6 — Swap final

```bash
mv $SESSION_ID.jsonl.new $SESSION_ID.jsonl
ls -la $SESSION_ID.jsonl*
wc -l $SESSION_ID.jsonl
python3 -c "import json; [json.loads(l) for l in open('$SESSION_ID.jsonl')]; print('ok')"
```

### Passo 7 — Reabrir

Instruir {{NOME_OPERADOR}}:
1. Reload Window no Antigravity: `Cmd+Shift+P` → `Reload Window`
2. Reabrir a aba pelo histórico de conversas
3. Confirmar que nova mensagem responde sem erro 400

## Critérios de aceitação

- `.bak` original preservado (nunca sobrescrito)
- `.bak2` da rodada criado
- 0 imagens em `"type":"image"` no arquivo final
- 100% das linhas parseiam como JSON válido
- Contagem de linhas mantida (exceto dropagens explícitas de `attachment.prompt` vazio)
- Sessão volta a responder no Antigravity após reload

## Erros comuns

- **`.bak2` já existe sem renomear** → conflito com rodada anterior. Renomear pra `.bak2-pre-rodadaN` antes.
- **Sed/awk no JSONL** → quebra encoding base64 e UTF-8. SEMPRE Python `json.loads`/`json.dumps`.
- **`tool_result` com imagem dropado em vez de substituído** → quebra pareamento `tool_use_id` → API rejeita histórico inteiro.
- **Aba aberta durante edição** → handle aberto, write parcial, sessão pode corromper de vez.

## Tratamento de aprendizado (Regra §5)

Se procedimento falhar ou exigir adaptação nova: atualizar essa skill + memória `feedback_destravar_sessao_*.md` + registrar em `segundo-cerebro/03-operacao/antigravity-historico.md`.
