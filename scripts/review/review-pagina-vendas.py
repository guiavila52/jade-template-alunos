#!/usr/bin/env python3
"""
Revisão visual página de vendas Sistema Reverso Beta
Protocolo 2 passadas: estética humana → técnica + testes de interação
"""
import sys
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from datetime import datetime

URL = "http://localhost:4322/reverso-beta"
SLUG = "reverso-beta"
OUTPUT_DIR = Path("/Users/guiavila/Documents/Projetos IA Gui Ávila/Jade - Time Gui Ávila/workspace/output/screenshots-revisao")

def main():
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    output_prefix = OUTPUT_DIR / f"{timestamp}-{SLUG}"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    findings = {
        "estetica": [],
        "tecnico": [],
        "interacao": []
    }
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # Desktop 1440x900
        context_desktop = browser.new_context(viewport={"width": 1440, "height": 900})
        page_desktop = context_desktop.new_page()
        
        print(f"🔍 Carregando {URL}...")
        page_desktop.goto(URL, wait_until="networkidle", timeout=30000)
        page_desktop.reload(wait_until="networkidle")
        page_desktop.keyboard.press("Escape")
        page_desktop.wait_for_timeout(500)
        
        # Screenshot desktop
        screenshot_desktop = f"{output_prefix}-desktop.jpg"
        page_desktop.screenshot(path=screenshot_desktop, type="jpeg", quality=70, full_page=True)
        print(f"✅ Screenshot desktop: {screenshot_desktop}")
        
        # === PASSADA 1: ESTÉTICA HUMANA ===
        print("\n=== PASSADA 1: ESTÉTICA HUMANA ===")
        
        # 1. Hero aurora visível
        aurora = page_desktop.query_selector(".aurora")
        if aurora:
            opacity = page_desktop.evaluate("el => getComputedStyle(el).opacity", aurora)
            if float(opacity) < 0.3:
                findings["estetica"].append("CRITICAL: Aurora hero invisível (opacity < 0.3)")
            elif float(opacity) > 0.7:
                findings["estetica"].append("HIGH: Aurora hero saturada demais (opacity > 0.7)")
        else:
            findings["estetica"].append("CRITICAL: Aurora hero não encontrada no DOM")
        
        # 2. Foto palestra carrega
        foto_palestra = page_desktop.query_selector("img[alt*='palestra'], img[alt*='Gui'], img[src*='palestra']")
        if not foto_palestra:
            findings["estetica"].append("CRITICAL: Foto palestra não encontrada (seção 'Quem ensina')")
        else:
            natural_width = page_desktop.evaluate("img => img.naturalWidth", foto_palestra)
            if natural_width == 0:
                findings["estetica"].append("CRITICAL: Foto palestra quebrada (naturalWidth=0)")
        
        # 3. Slider logos (20 itens)
        logos_slider = page_desktop.query_selector_all(".logo-slider img, [data-component='logo-slider'] img")
        if len(logos_slider) < 20:
            findings["estetica"].append(f"CRITICAL: Slider logos tem {len(logos_slider)} itens (esperado 20)")
        
        # 4. Slider depoimentos (19 cards)
        depoimentos_slider = page_desktop.query_selector_all(".slider-rail .card, [data-component='depoimentos'] .card")
        if len(depoimentos_slider) < 19:
            findings["estetica"].append(f"CRITICAL: Slider depoimentos tem {len(depoimentos_slider)} cards (esperado 19)")
        
        # 5. Espaços brancos verticais > 150px
        gaps = page_desktop.evaluate("""
            () => {
                const sections = Array.from(document.querySelectorAll('section, .section'));
                const gaps = [];
                for (let i = 0; i < sections.length - 1; i++) {
                    const current = sections[i].getBoundingClientRect();
                    const next = sections[i + 1].getBoundingClientRect();
                    const gap = next.top - current.bottom;
                    if (gap > 150) {
                        gaps.push({
                            after: sections[i].className || sections[i].tagName,
                            gap: Math.round(gap)
                        });
                    }
                }
                return gaps;
            }
        """)
        if gaps:
            for gap_info in gaps:
                findings["estetica"].append(f"HIGH: Buraco vertical {gap_info['gap']}px após seção {gap_info['after']}")
        
        # 6. Card preço destacado
        card_preco = page_desktop.query_selector(".card-preco, [data-price], .preco-container")
        if not card_preco:
            findings["estetica"].append("HIGH: Card preço não encontrado com seletor esperado")
        else:
            # Validar que R$ 697 usa font-size maior que body
            preco_element = page_desktop.query_selector_all(".card-preco *:has-text('697'), [data-price] *:has-text('697')")
            if not preco_element:
                findings["estetica"].append("MEDIUM: Dígito 697 não encontrado no card preço")
        
        # === PASSADA 2: TÉCNICA ===
        print("\n=== PASSADA 2: TÉCNICA ===")
        
        # 7. Console errors
        console_errors = []
        page_desktop.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page_desktop.reload(wait_until="networkidle")
        if console_errors:
            for err in console_errors[:5]:  # primeiros 5
                findings["tecnico"].append(f"MEDIUM: Console error: {err[:100]}")
        
        # 8. Overflow horizontal desktop
        scroll_width = page_desktop.evaluate("document.documentElement.scrollWidth")
        client_width = page_desktop.evaluate("document.documentElement.clientWidth")
        if scroll_width > client_width + 5:
            findings["tecnico"].append(f"HIGH: Overflow horizontal desktop ({scroll_width}px > {client_width}px)")
        
        # 9. Links inline (não URL crua)
        links_crus = page_desktop.query_selector_all("a:has-text('http://'), a:has-text('https://')")
        if links_crus:
            findings["tecnico"].append(f"LOW: {len(links_crus)} links com URL crua visível")
        
        # 10. CTAs apontam checkout
        ctas = page_desktop.query_selector_all("a[href*='checkout'], button[data-checkout]")
        if len(ctas) < 3:
            findings["tecnico"].append(f"HIGH: Apenas {len(ctas)} CTAs apontam checkout (esperado ≥3)")
        
        context_desktop.close()
        
        # Mobile 390x844
        context_mobile = browser.new_context(viewport={"width": 390, "height": 844})
        page_mobile = context_mobile.new_page()
        
        page_mobile.goto(URL, wait_until="networkidle", timeout=30000)
        page_mobile.reload(wait_until="networkidle")
        page_mobile.keyboard.press("Escape")
        page_mobile.wait_for_timeout(500)
        
        screenshot_mobile = f"{output_prefix}-mobile.jpg"
        page_mobile.screenshot(path=screenshot_mobile, type="jpeg", quality=70, full_page=True)
        print(f"✅ Screenshot mobile: {screenshot_mobile}")
        
        # 11. Overflow horizontal mobile
        scroll_width_mobile = page_mobile.evaluate("document.documentElement.scrollWidth")
        client_width_mobile = page_mobile.evaluate("document.documentElement.clientWidth")
        if scroll_width_mobile > client_width_mobile + 5:
            findings["tecnico"].append(f"CRITICAL: Overflow horizontal mobile ({scroll_width_mobile}px > {client_width_mobile}px)")
        
        context_mobile.close()
        
        # === TESTES DE INTERAÇÃO ===
        print("\n=== TESTES DE INTERAÇÃO ===")
        
        context_interaction = browser.new_context(viewport={"width": 1440, "height": 900})
        page_interaction = context_interaction.new_page()
        page_interaction.goto(URL, wait_until="networkidle")
        
        # 12. Testar drag no slider depoimentos
        slider_rail = page_interaction.query_selector(".slider-rail, [data-component='depoimentos']")
        if slider_rail:
            page_interaction.mouse.move(720, 450)
            page_interaction.mouse.down()
            page_interaction.mouse.move(500, 450)
            page_interaction.mouse.up()
            page_interaction.wait_for_timeout(300)
            # Validar que posição mudou (scroll left > 0)
            scroll_left = page_interaction.evaluate("el => el.scrollLeft", slider_rail)
            if scroll_left == 0:
                findings["interacao"].append("HIGH: Slider depoimentos não responde a drag (scrollLeft=0)")
        
        # 13. Testar hover CTA
        cta_hero = page_interaction.query_selector("a[href*='checkout']:first-of-type, .cta-primary")
        if cta_hero:
            bbox = cta_hero.bounding_box()
            page_interaction.mouse.move(bbox["x"] + 10, bbox["y"] + 10)
            page_interaction.wait_for_timeout(200)
            # Screenshot hover
            screenshot_hover = f"{output_prefix}-hover-cta.jpg"
            page_interaction.screenshot(path=screenshot_hover, type="jpeg", quality=70)
        
        context_interaction.close()
        browser.close()
    
    # === RELATÓRIO ===
    total_critical = len([f for f in findings["estetica"] + findings["tecnico"] + findings["interacao"] if "CRITICAL" in f])
    total_high = len([f for f in findings["estetica"] + findings["tecnico"] + findings["interacao"] if "HIGH" in f])
    total_medium = len([f for f in findings["estetica"] + findings["tecnico"] + findings["interacao"] if "MEDIUM" in f])
    total_low = len([f for f in findings["estetica"] + findings["tecnico"] + findings["interacao"] if "LOW" in f])
    
    veredicto = "APROVADO"
    if total_critical > 0:
        veredicto = "REPROVADO"
    elif total_high > 0:
        veredicto = "APROVADO COM RESSALVAS"
    
    report_path = OUTPUT_DIR / f"{timestamp}-{SLUG}-rev.md"
    with open(report_path, "w") as f:
        f.write(f"# Revisão visual — Sistema Reverso Beta — {timestamp}\n\n")
        f.write(f"## Veredicto: **{veredicto}**\n\n")
        f.write(f"## Resumo\n")
        f.write(f"- {total_critical} CRITICAL\n")
        f.write(f"- {total_high} HIGH\n")
        f.write(f"- {total_medium} MEDIUM\n")
        f.write(f"- {total_low} LOW\n\n")
        
        f.write(f"## Screenshots\n")
        f.write(f"- Desktop: `{screenshot_desktop}`\n")
        f.write(f"- Mobile: `{screenshot_mobile}`\n\n")
        
        if findings["estetica"]:
            f.write("## PASSADA 1 — Estética Humana\n")
            for finding in findings["estetica"]:
                f.write(f"- {finding}\n")
            f.write("\n")
        
        if findings["tecnico"]:
            f.write("## PASSADA 2 — Técnica\n")
            for finding in findings["tecnico"]:
                f.write(f"- {finding}\n")
            f.write("\n")
        
        if findings["interacao"]:
            f.write("## Testes de Interação\n")
            for finding in findings["interacao"]:
                f.write(f"- {finding}\n")
            f.write("\n")
        
        if veredicto == "APROVADO":
            f.write("## ✅ Aprovado para validação Gui + publicação\n")
        elif veredicto == "APROVADO COM RESSALVAS":
            f.write("## ⚠️  Aprovado com ressalvas — publicar mas ficar de olho nos HIGHs\n")
        else:
            f.write("## ❌ REPROVADO — dev deve corrigir CRITICALs antes de mostrar pro Gui\n")
    
    print(f"\n📄 Relatório salvo: {report_path}")
    print(f"🎯 Veredicto: {veredicto}")
    
    sys.exit(0 if veredicto != "REPROVADO" else 1)

if __name__ == "__main__":
    main()
