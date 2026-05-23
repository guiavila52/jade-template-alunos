#!/usr/bin/env python3
"""
Script de revisão visual de newsletters via Playwright.
Renderiza HTML fragment em contexto completo, tira screenshots, detecta problemas.

Uso:
  python3 render-and-screenshot.py --input fragment.html --slug cadc4df0
  python3 render-and-screenshot.py --input fragment.html --slug cadc4df0 --{{plataforma_conteudo}}-url https://...
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
import subprocess

# Verificar se Playwright está instalado
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("ERRO: Playwright não está instalado.", file=sys.stderr)
    print("Instalando Playwright...", file=sys.stderr)
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "playwright"], check=True, timeout=120)
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True, timeout=300)
        from playwright.sync_api import sync_playwright
        print("Playwright instalado com sucesso.", file=sys.stderr)
    except Exception as e:
        print(f"ERRO ao instalar Playwright: {e}", file=sys.stderr)
        sys.exit(1)

def wrapper_html(fragment):
    """Wrappa fragment em HTML completo para renderização."""
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Preview Newsletter</title>
</head>
<body style="max-width:600px; margin:40px auto; background:#f5f5f5; padding:20px; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
  <div style="background:white; padding:40px; border-radius:8px;">
{fragment}
  </div>
</body>
</html>"""

def detectar_espacos_brancos(page):
    """
    Detecta espaços brancos verticais > 60px.
    Retorna lista de problemas encontrados.
    """
    problemas = []
    
    # JavaScript para detectar gaps verticais grandes
    js_code = """
    () => {
      const body = document.body;
      const height = body.scrollHeight;
      const width = body.scrollWidth;
      
      // Amostragem vertical a cada 10px
      let gaps = [];
      let lastNonWhite = 0;
      let gapStart = null;
      
      for (let y = 0; y < height; y += 10) {
        // Sample middle column
        const pixel = document.elementFromPoint(width/2, y);
        const bgColor = pixel ? window.getComputedStyle(pixel).backgroundColor : 'rgb(255, 255, 255)';
        
        // Considera branco se rgb(255,255,255) ou rgb(245,245,245) ou transparent
        const isWhite = bgColor === 'rgb(255, 255, 255)' || 
                        bgColor === 'rgba(0, 0, 0, 0)' ||
                        bgColor === 'rgb(245, 245, 245)';
        
        if (isWhite) {
          if (gapStart === null) gapStart = y;
        } else {
          if (gapStart !== null && (y - gapStart) > 60) {
            gaps.push({start: gapStart, end: y, size: y - gapStart});
          }
          gapStart = null;
        }
      }
      
      return gaps;
    }
    """
    
    try:
        gaps = page.evaluate(js_code)
        for gap in gaps:
            problemas.append(f"Espaço branco vertical detectado: {gap['size']}px (posição {gap['start']}px - {gap['end']}px)")
    except Exception as e:
        print(f"AVISO: não foi possível detectar espaços brancos: {e}", file=sys.stderr)
    
    return problemas

def detectar_imagens_quebradas(page):
    """Detecta imagens com src 404 ou alt mostrando."""
    problemas = []
    
    js_code = """
    () => {
      const imgs = Array.from(document.querySelectorAll('img'));
      return imgs.map(img => ({
        src: img.src,
        alt: img.alt,
        naturalWidth: img.naturalWidth,
        naturalHeight: img.naturalHeight,
        complete: img.complete
      }));
    }
    """
    
    try:
        imgs = page.evaluate(js_code)
        for img in imgs:
            if not img['complete'] or img['naturalWidth'] == 0:
                problemas.append(f"Imagem quebrada: {img['src']} (alt: {img['alt']})")
    except Exception as e:
        print(f"AVISO: não foi possível detectar imagens quebradas: {e}", file=sys.stderr)
    
    return problemas

def tirar_screenshots(html_content, slug, output_dir):
    """
    Renderiza HTML e tira screenshots desktop + mobile.
    Retorna dict com paths e problemas detectados.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    screenshot_desktop = output_dir / f"{timestamp}-{slug}-desktop.png"
    screenshot_mobile = output_dir / f"{timestamp}-{slug}-mobile.png"
    
    problemas = []
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            
            # Screenshot desktop (600x viewport)
            page_desktop = browser.new_page(viewport={"width": 800, "height": 1200})
            page_desktop.set_content(html_content, timeout=60000)
            page_desktop.wait_for_load_state("networkidle", timeout=60000)
            
            # Detectar problemas
            problemas.extend(detectar_espacos_brancos(page_desktop))
            problemas.extend(detectar_imagens_quebradas(page_desktop))
            
            # Screenshot full page
            page_desktop.screenshot(path=str(screenshot_desktop), full_page=True, timeout=30000)
            print(f"Screenshot desktop salvo: {screenshot_desktop}", file=sys.stderr)
            
            page_desktop.close()
            
            # Screenshot mobile (375x viewport)
            page_mobile = browser.new_page(viewport={"width": 375, "height": 900})
            page_mobile.set_content(html_content, timeout=60000)
            page_mobile.wait_for_load_state("networkidle", timeout=60000)
            page_mobile.screenshot(path=str(screenshot_mobile), full_page=True, timeout=30000)
            print(f"Screenshot mobile salvo: {screenshot_mobile}", file=sys.stderr)
            
            page_mobile.close()
            browser.close()
    
    except Exception as e:
        print(f"ERRO ao tirar screenshots: {e}", file=sys.stderr)
        return None
    
    return {
        "desktop": str(screenshot_desktop),
        "mobile": str(screenshot_mobile),
        "problemas": problemas,
        "timestamp": timestamp
    }

def main():
    parser = argparse.ArgumentParser(description="Renderiza e tira screenshots de newsletter para revisão visual")
    parser.add_argument("--input", required=True, help="Path do HTML fragment")
    parser.add_argument("--slug", required=True, help="Slug da newsletter (ex: cadc4df0)")
    parser.add_argument("--{{plataforma_conteudo}}-url", help="URL do painel {{Plataforma_Conteudo}} (opcional)")
    parser.add_argument("--output-dir", default="{{PATH_LOCAL}} IA {{NOME_OPERADOR}}/Squad Empresa {{NOME_OPERADOR}}/workspace/output/screenshots-revisao", help="Diretório de saída")
    
    args = parser.parse_args()
    
    # Ler fragment
    try:
        fragment = Path(args.input).read_text(encoding='utf-8')
    except FileNotFoundError:
        print(f"ERRO: arquivo não encontrado: {args.input}", file=sys.stderr)
        sys.exit(1)
    
    # Wrapper HTML completo
    html_content = wrapper_html(fragment)
    
    # Tirar screenshots
    resultado = tirar_screenshots(html_content, args.slug, args.output_dir)
    
    if resultado is None:
        sys.exit(1)
    
    # Output JSON
    resultado["input"] = args.input
    resultado["slug"] = args.slug
    if args.gimmick_url:
        resultado["gimmick_url"] = args.gimmick_url
    
    print(json.dumps(resultado, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
