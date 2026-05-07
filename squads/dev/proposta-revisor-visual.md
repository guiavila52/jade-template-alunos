# Proposta — Upgrade do `/revisar-codigo-pagina` para validação visual headless

> Data: 2026-05-06
> Origem: REGRA INVIOLÁVEL #14 — rejeição do {{NOME_OPERADOR}} em /consultoria expôs que o revisor
> atual aprova com base em leitura de código, sem nunca abrir a página renderizada.
> Resultado: passou batido um iframe que cortava os últimos campos do formulário.
> Status: PROPOSTA — não implementar agora, registrar como pendência para Onda 3+.

---

## Problema

O `revisor-pagina-dev` lê o `.astro`, valida tokens, semântica, reuso de componentes,
proibições (Cormorant em números, !important). É **revisão estática** — nunca abre a página
no navegador. Falhas que só aparecem no rendering visual passam:

- Iframe cortado por wrapper com `min-height` insuficiente
- Texto invisível porque a fonte fica fina demais em mobile
- Sobreposição de elementos em viewport pequena
- CTA fora da fold no iPhone 14
- Aurora/glass não renderizando por bug de CSS
- Reveal-on-scroll travado

## Proposta

Adicionar etapa headless de validação visual ao revisor:

```
[3] Aplicar checklist textual
       │
       ▼
[3.5] Validação visual headless (NOVO)
   - Subir dev server (se não estiver de pé)
   - Playwright headless abre /[slug] em 2 viewports:
       • mobile : iPhone 14 (390×844, dpr 3)
       • desktop: 1440×900 (dpr 2)
   - Para cada viewport:
       • screenshot full-page
       • detecta elementos com bounding box fora da viewport horizontal (overflow-x)
       • detecta elementos com `display: none` no caminho de iframes/forms
       • detecta iframes com `scrollHeight > offsetHeight`
       • verifica se #form contém campo `[name=submit]` ou button[type=submit]
         visível no mobile
   - Anexa screenshots + relatório à revisão
       │
       ▼
[4] Decisão final (textual + visual)
```

## Stack proposta

- **Playwright** (`@playwright/test`) — já roda em CI Vercel, suporte oficial.
- Script Node em `Páginas Astro {{NOME_OPERADOR}}/scripts/visual-review.mjs`.
- Saída: 2 PNGs (`mobile.png`, `desktop.png`) + JSON com diagnostics.

## Esboço do script

```js
import { chromium, devices } from "playwright";

const URL = process.argv[2] || "http://localhost:4321/consultoria";
const browser = await chromium.launch();

for (const [name, ctxOpts] of Object.entries({
  mobile: devices["iPhone 14"],
  desktop: { viewport: { width: 1440, height: 900 } },
})) {
  const context = await browser.newContext(ctxOpts);
  const page = await context.newPage();
  await page.goto(URL, { waitUntil: "networkidle" });
  await page.screenshot({ path: `./review-${name}.png`, fullPage: true });

  const diag = await page.evaluate(() => {
    const out = { overflowX: [], iframeIssues: [], submitVisible: null };
    document.querySelectorAll("*").forEach((el) => {
      const r = el.getBoundingClientRect();
      if (r.right > window.innerWidth + 1)
        out.overflowX.push(el.tagName + "." + el.className);
    });
    document.querySelectorAll("iframe").forEach((f) => {
      if (f.scrollHeight > f.offsetHeight + 1)
        out.iframeIssues.push({ id: f.id, cut: f.scrollHeight - f.offsetHeight });
    });
    const submit = document.querySelector(
      'button[type=submit], input[type=submit]'
    );
    out.submitVisible = submit
      ? submit.getBoundingClientRect().bottom <= window.innerHeight + 200
      : null;
    return out;
  });
  console.log(name, JSON.stringify(diag, null, 2));
  await context.close();
}
await browser.close();
```

## Critérios de reprovação automática

- `overflowX.length > 0` em mobile
- `iframeIssues.length > 0` (qualquer iframe com scrollHeight > offsetHeight)
- `submitVisible === false` em mobile
- Diferença de > 200px entre `document.documentElement.scrollHeight` em mobile e desktop
  (sinal de layout colapsado)

## Estimativa de complexidade

| Etapa | Complexidade | Tempo estimado |
|-------|--------------|----------------|
| Adicionar Playwright ao projeto Astro | baixa | 15min (`npm i -D playwright && npx playwright install chromium`) |
| Script base de screenshots + diagnostics | baixa | 30min |
| Integrar ao `/revisar-codigo-pagina` (chamada Bash + parse) | média | 45min |
| Teste E2E em /consultoria validando que o revisor agora pega o iframe cortado | baixa | 15min |
| **Total** | **baixa-média** | **~2h** |

## Próximos passos (quando aprovado)

1. Adicionar tarefa nova em `squads/dev/tarefas.md`: "T_x — Implementar validação visual headless no revisor".
2. Instalar Playwright + Chromium no projeto Astro.
3. Criar `Páginas Astro {{NOME_OPERADOR}}/scripts/visual-review.mjs`.
4. Atualizar `.claude/commands/revisar-codigo-pagina.md` chamando o script via Bash antes do checklist final.
5. Validar em /consultoria, /reverso (já existe), nova migração.

## Riscos

- Tempo de execução: ~10s por viewport. Aceitável.
- Headless Chromium consome memória — mas roda local, sem impacto em produção.
- Playwright pesa ~200MB de browser. Adicionar `.gitignore` para `~/.cache/ms-playwright` e
  documentar instalação no `MAPA.md`.

## Observação

Enquanto não implementado, o checklist do `/revisar-codigo-pagina` (atualizado em 2026-05-06)
inclui item explícito de validação visual MANUAL — abrir a página em http://localhost:4321/[slug],
testar em DevTools mobile e desktop, antes de aprovar.
