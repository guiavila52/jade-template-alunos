---
description: Lista todas as paginas Astro do repo `Páginas Astro {{NOME_OPERADOR}}` com URLs de producao + status (publicada / em iteracao / draft).
---

# /listar-paginas

Skill operacional pra Jade ou subagent listar rapidamente todas as paginas do repo de producao.

## O que faz

1. Le `workspace/integracoes/paginas-astro.md` pra confirmar path canonico do repo.
2. Lista `src/pages/*/index.astro` dentro do repo.
3. Pra cada pagina, monta URL de producao: `sites.{{DOMINIO}}/{slug}`.
4. Marca status quando possivel (publicada confirmada via HTTP 200, ou em iteracao se so existe local).
5. Imprime tabela em markdown com 3 colunas: slug | URL | status.

## Execucao (deterministica)

```bash
REPO="$HOME/Documents/Projetos IA {{NOME_OPERADOR}}/Páginas Astro {{NOME_OPERADOR}}"
echo "| Slug | URL | Status |"
echo "|---|---|---|"
for dir in "$REPO/src/pages"/*/; do
  slug=$(basename "$dir")
  [[ "$slug" == "api" ]] && continue
  [[ "$slug" == *.preFix* ]] && continue
  [[ "$slug" == *.preMigracao* ]] && continue
  [[ -f "$dir/index.astro" ]] || continue
  url="https://sites.{{DOMINIO}}/$slug"
  status=$(curl -s -o /dev/null -w "%{http_code}" "$url" --max-time 5 2>/dev/null || echo "???")
  if [[ "$status" == "200" ]]; then
    badge="publicada"
  elif [[ "$status" == "404" ]]; then
    badge="em iteracao (404 prod)"
  else
    badge="status $status"
  fi
  echo "| $slug | $url | $badge |"
done
```

## Output

Tabela markdown impressa direto no chat. Jade usa pra mapear estado do funil quando {{NOME_OPERADOR_CURTO}} pedir "lista as paginas que temos".

## Quando usar

- {{NOME_OPERADOR_CURTO}} perguntar quais paginas existem
- Antes de criar pagina nova (verificar slug livre)
- Auditoria periodica de paginas publicadas vs em iteracao