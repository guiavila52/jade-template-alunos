# /qa-video

Roda o agente de QA no vídeo FINAL editado. Detecta problemas antes de passar pro operador validar.

## Quando usar

- Sempre após `/editar-video` exportar o `*_FINAL.mp4`
- Quando operador pede pra checar um vídeo editado antes de validar

## Input

```
/qa-video <numero_ou_path>
```

Exemplos:
- `/qa-video 175` → analisa `/Users/{{USERNAME_MAC}}/Desktop/yt-editados/yt175_FINAL.mp4`
- `/qa-video 175 v3` → analisa `yt175_FINAL_v3.mp4`
- `/qa-video "/path/completo/video.mp4"` → path direto

## O que o agente detecta

1. **Retomadas remanescentes** — "Peraí", "Ops", "Vamos lá" órfão, "retomando"
2. **Gaps audíveis** — silêncio >0.5s entre palavras em pontos de corte
3. **Repetição de frases** — >70% overlap entre segmentos consecutivos
4. **Fim sujo** — câmera desligando ou >1s silêncio após última palavra
5. **Início sujo** — >0.5s respiração/silêncio antes da primeira palavra

## Fluxo

Jade despacha `@analista-qa-video` com:
- Path do FINAL
- Instrução pra salvar relatório em `/Users/{{USERNAME_MAC}}/Desktop/yt-editados/ytNNN_QA.txt`

Agente entrega relatório com timestamps no formato `[MM:SS] PROBLEMA — descrição`.

## Output para operador

Jade reporta:
- Se ❌ problemas: lista com timestamps + "Corrijo antes de você validar?"
- Se ✅ tudo OK: "QA limpo. Pode abrir o QuickTime e conferir em [timestamps das emendas]."

## Integração com /editar-video

A skill `/editar-video` deve chamar `/qa-video` automaticamente após gerar o FINAL, antes de reportar pro operador.

## Histórico

- 06/06/2026 — criada com aval explícito do operador. Motivo: automatizar detecção de problemas nas emendas antes da validação humana.
