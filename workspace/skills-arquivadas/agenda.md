# /agenda — Agenda do Dia

Ao ser chamado, execute em sequência sem pedir confirmação:

## 1. Puxe a agenda do dia

Use o MCP do Google Calendar. Busque eventos de hoje nos seguintes calendários em paralelo:
- `{{EMAIL_OPERADOR}}` — agenda principal
- `c_5kb045kajbgk1mfe0if3uvs5ds@group.calendar.google.com` — {{NOME_OPERADOR}}
- `c_itvko53jtjt2dug34cjmc5qeu0@group.calendar.google.com` — {{LMS}}
- `{{EMAIL_LMS}}` — {{LMS}}

**Ignorar sempre:** "Semana ideal", "Semana ideal 2", "Agenda (teste)", "Conteúdos | {{EMPRESA_NEGOCIO}}".

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
[ Gui pede /agenda ]
        ↓
[ NOTA: skill canônica é /ver-agenda ] → @jade
   /agenda mantida como alias histórico (Regra #17)
        ↓
[ 1. Buscar eventos de hoje em PARALELO ] → @jade
   - {{EMAIL_OPERADOR}} (principal)
   - c_5kb045kajbgk1mfe0if3uvs5ds@group ({{NOME_OPERADOR}})
   - c_itvko53jtjt2dug34cjmc5qeu0@group ({{LMS}})
   - {{EMAIL_LMS}} ({{LMS}})
   ignorar: Semana ideal, Semana ideal 2,
            Agenda (teste), Conteúdos | {{EMPRESA_NEGOCIO}}
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
