# Memória — @desenvolvedor-frontend (squad-dev)

> Memória específica do agente paginas-dev. Lições reincidentes ficam em `squads/dev/aprendizados.md`, em `aprendizados.md` desta pasta e/ou nas memórias persistentes do user.

---

## Contexto operacional

- Squad: dev
- Função: implementação de páginas Astro a partir de copy aprovada
- Implementa em `Páginas Astro Gui Ávila/src/pages/`
- Usa Slider canônico (`Páginas Astro Gui Ávila/src/components/Slider.astro`) — modos `marquee` e `rail`
- Backup `.preFix{tarefa}` obrigatório antes de mudar arquivo existente (AGENTS.md #18)
- Deploy via `vercel --prod --yes` na pasta `Páginas Astro Gui Ávila/`

## Skills associadas

| Skill | Função |
|---|---|
| `/codar-pagina` | produção (gera componente Astro a partir do markdown aprovado) |
| `/revisar-codigo-pagina` | revisor de código + UX |
| `/migrar-pagina` | migração GHL/Framer → Astro pixel-perfect |
| `/testar-pagina` | bateria #15 (12 pontos + diff visual em migração) |
| `/publicar-pagina` | build → preview localhost → OK Gui → `vercel --prod` |

## Source of truth

- `Páginas Astro Gui Ávila/DESIGN-SYSTEM.md` — fonte única visual
- `Páginas Astro Gui Ávila/mapa.md` — estrutura do projeto Astro
- `workspace/output/paginas/mapa.md` — lista de páginas produzidas

## Regras críticas vivas

- GTM-NN36ZRZ obrigatório em toda página (`feedback_gtm_obrigatorio.md`)
- Favicon canônico (`feedback_favicon_padrao.md`)
- Sliders rail = drag fluido sem scroll-snap (`feedback_drag_fluido_obrigatorio.md`)
- Cursor grab/grabbing em sliders drag (`feedback_cursor_grab_sliders.md`)
- Snapshot externo (Framer/Webflow) substitui sliders pelo Slider.astro (`feedback_snapshot_externo_substituir_sliders.md`)
- Migração clona TODOS assets externos pra `public/` (`feedback_assets_externos_obrigatorios.md`)
- Logos de ferramentas/parceiros = SVG/PNG oficial (`feedback_logomarcas_ferramentas.md`)
- NUNCA exclui repos/projetos/deploys (`feedback_proibido_excluir_repos.md`)
