#!/usr/bin/env python3
"""Helper para migração pixel perfect de páginas estáticas Squad → Astro.

Uso:
  python3 migrate_page.py <slug> <title> <description> [extra_fonts_link]

Lê /tmp/<slug>-orig.html, gera src/pages/<slug>/index.astro pixel perfect.
"""
import sys, re, os

if len(sys.argv) < 4:
    print("usage: migrate_page.py <slug> <title> <description> [fonts_link_or_NONE]")
    sys.exit(1)

slug = sys.argv[1]
title = sys.argv[2]
desc = sys.argv[3]
fonts_link = sys.argv[4] if len(sys.argv) > 4 else "NONE"

src_html = f'/tmp/{slug}-orig.html'
src = open(src_html).read()

m_style = re.search(r'<style>(.*?)</style>', src, re.S)
css = m_style.group(1) if m_style else ''

m_body = re.search(r'<body[^>]*>(.*?)</body>', src, re.S)
body = m_body.group(1) if m_body else ''

# Extrair scripts inline (preserve em ordem)
scripts = []
def grab_script(m):
    content = m.group(1)
    if not content.strip():
        return ''
    scripts.append(content)
    return f'<!-- SCRIPT_PLACEHOLDER_{len(scripts)-1} -->'

body_temp = re.sub(r'<script>(.*?)</script>', grab_script, body, flags=re.S)

# Extrair scripts externos
external_scripts = re.findall(r'<script\s+src="([^"]+)"[^>]*></script>', body)
body_temp = re.sub(r'<script\s+src="[^"]+"[^>]*></script>', '', body_temp)

# Remover GTM noscript (já vem do Base)
body_temp = re.sub(r'<noscript><iframe src="https://www\.googletagmanager\.com/ns\.html\?id=GTM-NN36ZRZ"[^>]*></iframe></noscript>', '', body_temp, flags=re.S)
body_temp = re.sub(r'<!-- Google Tag Manager \(noscript\) -->', '', body_temp)
body_temp = re.sub(r'<!-- End Google Tag Manager \(noscript\) -->', '', body_temp)

# Reescrever asset paths para URLs absolutas em sites.{{DOMINIO}}
body_temp = re.sub(r'src="/([^"]+\.(?:png|jpg|jpeg|svg|webp|gif|ico|mp4))', r'src="https://sites.{{DOMINIO}}/\1', body_temp)
# href para imagens (raro)
body_temp = re.sub(r'href="/(images/[^"]+)"', r'href="https://sites.{{DOMINIO}}/\1"', body_temp)

def esc(s):
    return s.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')

# Reinserir placeholders como ASTRO_SCRIPT_N (substitui depois pelo template)
body_html = body_temp

# Astro template
fonts_block = ''
if fonts_link != "NONE":
    fonts_block = f'''  <link
    slot="head"
    href="{fonts_link}"
    rel="stylesheet"
  />\n'''

ext_scripts_block = ''
for u in external_scripts:
    ext_scripts_block += f'  <script is:inline src="{u}"></script>\n'

inline_scripts_block = ''
for s in scripts:
    s_safe = s.replace('</script>', '<\\/script>')
    inline_scripts_block += '  <script is:inline>{`' + esc(s_safe) + '`}</script>\n'

# Substituir placeholders no body por nada (scripts vão pro fim do <Base>)
body_html = re.sub(r'<!-- SCRIPT_PLACEHOLDER_\d+ -->', '', body_html)

template = f'''---
// /{slug} — migração pixel perfect (Onda 6)
//
// Origem: https://sites.{{DOMINIO}}/{slug} (HTML estático)
// Data migração: 2026-05-06
// Diretiva: PIXEL PERFECT — clone visual idêntico da original.
//
// Notas:
//   • CSS da página é injetado via <style is:global> NO BODY pra ficar APÓS
//     o global.css do design system (que define h1/h2/h3 com Syne).
//   • Aurora própria (não a do Base): aurora={{false}}.
//   • Footer original próprio (não global): footer={{false}}.
//   • Imagens apontam pra URLs absolutas em sites.{{DOMINIO}} (asset fonte único).

import Base from "../../layouts/Base.astro";

const meta = {{
  title: "{title}",
  description:
    "{desc}",
  slug: "{slug}",
  canonical: "https://sites.{{DOMINIO}}/{slug}",
}};

const bodyHtml = `{esc(body_html)}`;
const pageStyles = `{esc(css)}`;
---

<Base
  title={{meta.title}}
  description={{meta.description}}
  slug={{meta.slug}}
  canonical={{meta.canonical}}
  aurora={{false}}
  footer={{false}}
  bodyClass=""
>
{fonts_block}  {{/* Reset prévio: zera regras `body` herdadas do global.css que conflitam
      com o body da página migrada (line-height/font-family genéricos do
      design system). A página redefine o que precisa logo abaixo. */}}
  <style is:global set:html={{`body {{ line-height: normal; font-family: inherit; }} body::after {{ content: none; }}`}}></style>

  <style is:global set:html={{pageStyles}}></style>

  <Fragment set:html={{bodyHtml}} />

{ext_scripts_block}{inline_scripts_block}</Base>
'''

out_dir = f'~/Documents/Projetos IA {{NOME_OPERADOR}}/Páginas Astro {{NOME_OPERADOR}}/src/pages/{slug}'
os.makedirs(out_dir, exist_ok=True)
out = f'{out_dir}/index.astro'
open(out, 'w').write(template)
print(f"Wrote {out}")
print(f"  CSS: {len(css)} chars, body: {len(body_html)} chars, inline scripts: {len(scripts)}, ext scripts: {len(external_scripts)}")
