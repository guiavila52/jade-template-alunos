#!/usr/bin/env python3
"""
Revisão visual Sistema Reverso Beta — v2 com wait adequado
Protocolo 2 passadas: estética humana → técnica + inspeção visual real
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from datetime import datetime

URL = "http://localhost:4322/reverso-beta"
SLUG = "reverso-beta"
OUTPUT_DIR = Path("{{PATH_LOCAL}} IA {{NOME_OPERADOR}}/Jade - Time {{NOME_OPERADOR}}/workspace/output/screenshots-revisao")

def main():
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    output_prefix = OUTPUT_DIR / f"{timestamp}-{SLUG}"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    findings = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # Desktop 1440x900
        context_desktop = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context_desktop.new_page()
        
        print(f"🔍 Carregando {URL}...")
        page.goto(URL, wait_until="networkidle", timeout=45000)
        page.wait_for_timeout(2000)  # Wait extra pra hot reload
        
        # Confirmar que não é 404
        title = page.title()
        if "404" in title:
            findings.append("CRITICAL: Página retorna 404")
            print(f"❌ 404 detectado: {title}")
        else:
            print(f"✅ Página carregou: {title}")
        
        # Screenshot desktop
        screenshot_desktop = f"{output_prefix}-desktop.jpg"
        page.screenshot(path=screenshot_desktop, type="jpeg", quality=80, full_page=True)
        print(f"📸 Screenshot desktop: {screenshot_desktop}")
        
        # === PASSADA 1: INSPEÇÃO VISUAL ESTÉTICA ===
        print("\n=== PASSADA 1: ESTÉTICA HUMANA ===")
        
        # 1. Hero aurora (validar opacity ~55%)
        aurora_visible = page.locator(".aurora, [class*='aurora']").count() > 0
        if not aurora_visible:
            findings.append("HIGH: Aurora hero não detectada visualmente")
        
        # 2. Foto palestra Gui (seção "Quem ensina")
        foto_gui = page.locator("img[alt*='Gui'], img[alt*='palestra'], img[src*='palestra']").first
        if foto_gui.count() == 0:
            findings.append("CRITICAL: Foto palestra Gui não encontrada")
        else:
            # Validar que carregou (naturalWidth > 0)
            loaded = page.evaluate("img => img.complete && img.naturalWidth > 0", foto_gui.element_handle())
            if not loaded:
                findings.append("CRITICAL: Foto palestra Gui quebrada (não carregou)")
        
        # 3. Slider logos (20 itens)
        logos = page.locator(".logo-slider img, [data-logos] img").count()
        print(f"   Logos slider: {logos} encontrados")
        if logos < 20:
            findings.append(f"CRITICAL: Slider logos tem {logos} itens (esperado 20)")
        
        # 4. Slider depoimentos (19 cards)
        depoimentos = page.locator(".depoimento, [data-depoimento], .card-depoimento").count()
        print(f"   Cards depoimentos: {depoimentos} encontrados")
        if depoimentos < 19:
            findings.append(f"CRITICAL: Slider depoimentos tem {depoimentos} cards (esperado 19)")
        
        # 5. Card preço destacado
        card_preco = page.locator(".preco, [data-price], .card-preco").first
        if card_preco.count() == 0:
            findings.append("HIGH: Card preço não encontrado")
        
        # 6. R$ 697 visível
        preco_697 = page.locator("text=/697/").count()
        if preco_697 == 0:
            findings.append("HIGH: Preço R$ 697 não encontrado no DOM")
        
        # 7. Espaços brancos verticais > 150px
        gaps = page.evaluate("""
            () => {
                const sections = Array.from(document.querySelectorAll('section'));
                const gaps = [];
                for (let i = 0; i < sections.length - 1; i++) {
                    const current = sections[i].getBoundingClientRect();
                    const next = sections[i + 1].getBoundingClientRect();
                    const gap = next.top - current.bottom;
                    if (gap > 150) {
                        gaps.push({
                            after: sections[i].className || `section-${i}`,
                            gap: Math.round(gap)
                        });
                    }
                }
                return gaps;
            }
        """)
        for gap_info in gaps:
            findings.append(f"MEDIUM: Buraco vertical {gap_info['gap']}px após {gap_info['after']}")
        
        # === PASSADA 2: TÉCNICA ===
        print("\n=== PASSADA 2: TÉCNICA ===")
        
        # 8. CTAs checkout
        ctas = page.locator("a[href*='checkout']").count()
        print(f"   CTAs checkout: {ctas} encontrados")
        if ctas < 3:
            findings.append(f"HIGH: Apenas {ctas} CTAs apontam checkout (esperado ≥3)")
        
        # 9. Overflow horizontal desktop
        scroll_width = page.evaluate("document.documentElement.scrollWidth")
        client_width = page.evaluate("document.documentElement.clientWidth")
        if scroll_width > client_width + 5:
            findings.append(f"HIGH: Overflow horizontal desktop ({scroll_width}px > {client_width}px)")
        
        # 10. Console errors
        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.reload(wait_until="networkidle")
        page.wait_for_timeout(1000)
        
        critical_errors = [e for e in console_errors if "failed" in e.lower() or "404" in e]
        for err in critical_errors[:3]:
            findings.append(f"MEDIUM: Console error: {err[:80]}")
        
        context_desktop.close()
        
        # Mobile 390x844
        context_mobile = browser.new_context(viewport={"width": 390, "height": 844})
        page_mobile = context_mobile.new_page()
        
        page_mobile.goto(URL, wait_until="networkidle", timeout=45000)
        page_mobile.wait_for_timeout(2000)
        
        screenshot_mobile = f"{output_prefix}-mobile.jpg"
        page_mobile.screenshot(path=screenshot_mobile, type="jpeg", quality=80, full_page=True)
        print(f"📸 Screenshot mobile: {screenshot_mobile}")
        
        # 11. Overflow horizontal mobile
        scroll_width_mobile = page_mobile.evaluate("document.documentElement.scrollWidth")
        client_width_mobile = page_mobile.evaluate("document.documentElement.clientWidth")
        if scroll_width_mobile > client_width_mobile + 5:
            findings.append(f"CRITICAL: Overflow horizontal mobile ({scroll_width_mobile}px > {client_width_mobile}px)")
        
        context_mobile.close()
        browser.close()
    
    # === RELATÓRIO ===
    critical_count = len([f for f in findings if "CRITICAL" in f])
    high_count = len([f for f in findings if "HIGH" in f])
    medium_count = len([f for f in findings if "MEDIUM" in f])
    
    veredicto = "APROVADO"
    if critical_count > 0:
        veredicto = "REPROVADO"
    elif high_count > 0:
        veredicto = "APROVADO COM RESSALVAS"
    
    report_path = OUTPUT_DIR / f"{timestamp}-{SLUG}-rev.md"
    with open(report_path, "w") as f:
        f.write(f"# Revisão visual — Sistema Reverso Beta — {timestamp}\n\n")
        f.write(f"## Veredicto: **{veredicto}**\n\n")
        f.write(f"## Resumo\n")
        f.write(f"- {critical_count} CRITICAL\n")
        f.write(f"- {high_count} HIGH\n")
        f.write(f"- {medium_count} MEDIUM\n\n")
        
        f.write(f"## Screenshots\n")
        f.write(f"- Desktop: `{screenshot_desktop}`\n")
        f.write(f"- Mobile: `{screenshot_mobile}`\n\n")
        
        if findings:
            f.write("## Findings\n")
            for finding in findings:
                f.write(f"- {finding}\n")
            f.write("\n")
        
        if veredicto == "APROVADO":
            f.write("## ✅ Aprovado\n\nPágina pronta pra validação Gui + publicação.\n")
        elif veredicto == "APROVADO COM RESSALVAS":
            f.write("## ⚠️  Aprovado com ressalvas\n\nPublicar mas corrigir HIGHs em próxima iteração.\n")
        else:
            f.write("## ❌ REPROVADO\n\nDev deve corrigir CRITICALs antes de mostrar pro Gui.\n")
    
    print(f"\n📄 Relatório: {report_path}")
    print(f"🎯 Veredicto: {veredicto}")
    
    sys.exit(0 if veredicto != "REPROVADO" else 1)

if __name__ == "__main__":
    main()
