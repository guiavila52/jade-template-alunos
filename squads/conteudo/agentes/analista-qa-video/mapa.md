# MAPA — squads/conteudo/agentes/analista-qa-video/

> Última atualização: 2026-06-10

## Propósito

Agente **analista-qa-video** (squad-conteudo) — QA de vídeo editado. Analisa o arquivo final exportado pelo editor, transcreve com mlx-whisper, detecta retomadas remanescentes, gaps audíveis, repetições, inícios/fins sujos, e emite lista de timestamps com problemas para o editor corrigir.

Despachado SEMPRE após `/editar-video` exportar o FINAL, antes de qualquer upload para YouTube.

## Arquivos

| Arquivo | Conteúdo |
|---------|----------|
| `aprendizados.md` | Lições do agente — padrões de erro detectados em revisões reais. |
| `mapa.md` | Este arquivo. |

## Skills relacionadas

- `/qa-video` — skill principal que despacha este agente
- `/editar-video` — skill que produz o FINAL que este agente revisa

## Ferramentas

Bash (transcrição mlx-whisper), Read, Write.

## Histórico

Criado em 2026-06-06. Especializado em QA de áudio — detecta problemas invisíveis na edição de vídeo (retomadas ("peraí", "vou refazer"), hesitações nos cortes, gaps de silêncio, repetição de conteúdo entre clips).
