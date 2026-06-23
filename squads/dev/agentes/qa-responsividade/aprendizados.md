# Aprendizados — @qa-responsividade (squad-dev)

> Append-only. Cada falha detectada ou apontada pelo operador vira entrada permanente aqui (Regra §5).
> Formato: data, contexto, falha, correção, regra incorporada.

---

<!-- agente criado em 2026-06-09 por demanda explícita do operador -->
<!-- "Quero agente de QA que vê a qualidade de uma página no celular. Criterioso. Ver se nada está quebrando, hero section boa no celular, carregamento correto." -->

### 2026-06-09 — Primeira execução: /[sua-pagina] — tap targets insuficientes no header mobile

**Contexto:** QA mobile de estreia numa página de vendas após redesign de pricing e top bar.

**O que aconteceu:** Botões do header ("Comprar agora" e "Login na plataforma") mediam 38px de altura e 12.48px de font-size no mobile. Abaixo dos 44px mínimos (Apple HIG / WCAG). Botão menor era difícil de tocar com precisão.

**Correção aplicada:**
```css
@media (max-width: 768px) {
  .btn-header-cta, .btn-login {
    min-height: 44px !important;
    font-size: 0.875rem !important;
    padding: 10px 12px !important;
    display: inline-flex !important;
    align-items: center !important;
  }
}
```

**Padrão identificado:** Todo botão interativo em mobile deve ter `min-height: 44px` explícito. `padding` sozinho não garante — usar `min-height` explícito sempre que o botão for um link/CTA em header ou hero.

**Como evitar:** Antes de emitir QA-MOBILE-APROVADO, verificar `getBoundingClientRect().height` de TODOS os botões em todos os viewports. Height < 44px = reprovação automática.

**Status final:** QA-MOBILE-APROVADO após correção. Deploy em produção.
