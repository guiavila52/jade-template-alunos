#!/usr/bin/env python3
"""
Gerador de slides de carrossel — tweet card style.
Lê roteiro.md, gera slide-01.png, slide-02.png... em formato 1080x1350.

Uso:
    python3 gerar-carrossel.py --roteiro PATH/roteiro.md --output PATH/pasta/

Formato do roteiro.md:
    Cada slide separado por "---"
    Palavras em **negrito** ficam em bold na imagem
    Primeira linha de cada bloco = texto do slide
"""

import argparse
import base64
import subprocess
import re
import os
import sys
from pathlib import Path
from datetime import date

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FOTO_PERFIL_DRIVE_ID = "1hqoDrRVFMVfbMxla4U8QikRkD6Tg_t-W"
FOTO_CACHE = Path("/tmp/gui_foto_perfil.png")

NOME = "Gui Ávila"
HANDLE = "@{{GITHUB_USER}}"


def get_foto_base64():
    """Carrega foto do cache local ou baixa do Drive."""
    if not FOTO_CACHE.exists():
        print("Foto não encontrada em cache. Baixe manualmente para /tmp/gui_foto_perfil.png")
        print("Ou rode: python3 workspace/scripts/baixar-foto-perfil.py")
        sys.exit(1)
    with open(FOTO_CACHE, "rb") as f:
        return base64.b64encode(f.read()).decode()


def texto_para_html(texto):
    """Converte **negrito** para <strong> e \n para <br>."""
    texto = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', texto)
    texto = texto.replace('\n', '<br>')
    return texto


def gerar_slide_html(texto, img_b64, slide_num, total_slides):
    texto_html = texto_para_html(texto)
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    width: 1080px;
    height: 1350px;
    background: #ffffff;
    font-family: -apple-system, 'Helvetica Neue', Arial, sans-serif;
    padding: 140px 90px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    position: relative;
  }}
  .profile {{
    display: flex;
    align-items: center;
    gap: 24px;
    margin-bottom: 72px;
  }}
  .avatar {{
    width: 96px;
    height: 96px;
    border-radius: 50%;
    object-fit: cover;
    flex-shrink: 0;
  }}
  .name-row {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 6px;
  }}
  .name {{
    font-size: 34px;
    font-weight: 700;
    color: #000;
    letter-spacing: -0.4px;
  }}
  .verified {{
    width: 34px;
    height: 34px;
    background: #1D9BF0;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
  }}
  .verified svg {{ width: 19px; height: 19px; }}
  .handle {{
    font-size: 28px;
    color: #536471;
  }}
  .content {{
    font-size: 76px;
    line-height: 1.3;
    color: #0f1419;
    font-weight: 400;
    letter-spacing: -1.5px;
  }}
  .content strong {{ font-weight: 700; }}
  .slide-number {{
    position: absolute;
    bottom: 90px;
    right: 90px;
    font-size: 28px;
    color: #536471;
    font-weight: 400;
  }}
</style>
</head>
<body>
  <div class="profile">
    <img class="avatar" src="data:image/png;base64,{img_b64}" />
    <div>
      <div class="name-row">
        <span class="name">{NOME}</span>
        <div class="verified">
          <svg viewBox="0 0 24 24" fill="white"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>
        </div>
      </div>
      <span class="handle">{HANDLE}</span>
    </div>
  </div>
  <div class="content">{texto_html}</div>
  <span class="slide-number">{slide_num}/{total_slides}</span>
</body>
</html>"""


def screenshot_html(html_path, png_path):
    subprocess.run([
        CHROME,
        "--headless=new",
        f"--screenshot={png_path}",
        "--window-size=1080,1350",
        "--hide-scrollbars",
        "--disable-gpu",
        f"file://{html_path}"
    ], capture_output=True, check=True)


def parse_roteiro(path):
    """Lê roteiro.md e retorna lista de textos por slide."""
    content = Path(path).read_text(encoding="utf-8")
    # Remove frontmatter e cabeçalho
    slides = []
    for bloco in content.split("---"):
        bloco = bloco.strip()
        if not bloco:
            continue
        # Ignora blocos que são só cabeçalho markdown
        if bloco.startswith("#") and len(bloco.split("\n")) == 1:
            continue
        # Remove linhas de cabeçalho do bloco
        linhas = [l for l in bloco.split("\n") if not l.startswith("#")]
        texto = "\n".join(linhas).strip()
        if texto:
            slides.append(texto)
    return slides


def main():
    parser = argparse.ArgumentParser(description="Gerar slides de carrossel")
    parser.add_argument("--roteiro", required=True, help="Caminho para roteiro.md")
    parser.add_argument("--output", required=True, help="Pasta de output para os PNGs")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Carregando foto de perfil...")
    img_b64 = get_foto_base64()

    print("Lendo roteiro...")
    slides = parse_roteiro(args.roteiro)
    print(f"{len(slides)} slide(s) encontrado(s).")

    tmp_html = Path("/tmp/slide_atual.html")

    total = len(slides)
    for i, texto in enumerate(slides, 1):
        nome = f"slide-{i:02d}"
        html = gerar_slide_html(texto, img_b64, i, total)
        tmp_html.write_text(html, encoding="utf-8")

        png_path = output_dir / f"{nome}.png"
        print(f"Gerando {nome}.png...")
        screenshot_html(str(tmp_html.absolute()), str(png_path.absolute()))

    print(f"\n✅ {len(slides)} slide(s) gerado(s) em: {output_dir}")
    print("Abrir pasta:", f"open '{output_dir}'")


if __name__ == "__main__":
    main()
