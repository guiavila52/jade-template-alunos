---
name: ver-agenda
description: Consolida agenda do dia do Google Calendar (4 calendarios em paralelo), remove duplicatas e calcula blocos livres.
type: skill
---

# /ver-agenda — Agenda do Dia

Ao ser chamado, execute em sequência sem pedir confirmação:

## 1. Puxe a agenda do dia

Use o MCP do Google Calendar. Busque eventos de hoje nos seguintes calendários em paralelo:
- `{{EMAIL_OPERADOR}}` — agenda principal
- `{{CALENDAR_ID_OPERADOR}}@group.calendar.google.com` — {{NOME_OPERADOR}}
- `{{CALENDAR_ID_PLATAFORMA}}@group.calendar.google.com` — {{PLATAFORMA_CURSOS}}
- `{{SLUG_OPERADOR}}@{{plataforma_cursos}}.com` — {{PLATAFORMA_CURSOS}}

**Ignorar sempre:** "Semana ideal", "Semana ideal 2", "Agenda (teste)", "Conteúdos | {{PRODUTO_PARCERIA}}".

Após buscar, consolide todos os eventos numa única linha do tempo, remova duplicatas e calcule os blocos livres entre compromissos.

## 2. Entregue o cockpit

Formato obrigatório:

```
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
AGENDA — [dia da semana], [data completa]
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

📅 HOJE
[HH:MM] ▪▪ [evento] ([duração])
[HH:MM] ░░░ livre ([duração])
...

⚡ FOCO
[Com base na agenda, qual é o bloco mais importante do dia? 1 frase.]
```

## Regras

- Não narre. Execute e entregue.
- Blocos livres são tão importantes quanto os compromissos — sempre calcule e mostre.
- Foco: uma opinião direta. Não "depende".
- Se a integração falhar, sinalize.

## Fluxo

```
[ {{NOME_OPERADOR_CURTO}} pede /ver-agenda ]
        ↓
[ 1. Buscar eventos de hoje em PARALELO ] → @jade
   - {{EMAIL_OPERADOR}} (principal)
   - {{CALENDAR_ID_OPERADOR}}@group ({{NOME_OPERADOR}})
   - {{CALENDAR_ID_PLATAFORMA}}@group ({{PLATAFORMA_CURSOS}})
   - {{SLUG_OPERADOR}}@{{plataforma_cursos}}.com ({{PLATAFORMA_CURSOS}})
   ignorar: Semana ideal, Semana ideal 2,
            Agenda (teste), Conteúdos | {{PRODUTO_PARCERIA}}
        ↓
[ 2. Consolidar timeline ] → @jade
   - dedup
   - calcular blocos LIVRES entre compromissos
   - bloco livre = compromisso (nunca ignorar)
        ↓
[ 3. Eleger FOCO do dia ] → @jade
   1 frase, opinião direta (não "depende")
        ↓
[ 4. Entregar cockpit ASCII ] → @jade
   AGENDA — [dia], [data]
   📅 HOJE  +  ⚡ FOCO
        ↓
   ⟶ FIM (se Calendar falhar: sinalizar, não inventar)
```