#!/usr/bin/env python3
"""
Script determinístico para renderização de newsletters em HTML.
Gera fragmento HTML (sem DOCTYPE/html/body wrapper) a partir de config JSON.

Uso:
  python3 renderizar-html.py --input config.json --output output.html
  python3 renderizar-html.py --input config.json --output output.html --editable
  ou
  cat config.json | python3 renderizar-html.py --output output.html
"""

import sys
import json
import argparse
import re
from pathlib import Path

# Template canônico de estilos inline (extraído de 62bec9ff)
STYLE_PARAGRAFO = "margin:0 0 16px; line-height:1.6; font-size:16px; color:#1a1a1a; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;"
STYLE_HEADING2 = "font-size:22px; line-height:1.3; font-weight:700; margin:32px 0 16px; color:#1a1a1a; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;"
STYLE_LINK = "color:#2563eb; text-decoration:underline; font-size:inherit;"
STYLE_UL = "margin:0 0 16px; padding-left:24px; font-size:16px; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;"
STYLE_LI = "margin-bottom:8px; line-height:1.6; font-size:16px; color:#1a1a1a;"
STYLE_STRONG = "font-weight:700; color:#1a1a1a;"
STYLE_HR = "border:none; border-top:1px solid #e5e5e5; margin:32px 0;"

def renderizar_inline_markdown(texto):
    """
    Converte sintaxe markdown inline para HTML:
    - [texto](url) → <a href="url" style="...">texto</a>
    - **texto** → <strong style="...">texto</strong>
    - *texto* → <em>texto</em>
    
    Preserva {{contact.first_name}} e outros placeholders intactos.
    """
    # Links: [texto](url)
    texto = re.sub(
        r'\[([^\]]+)\]\(([^\)]+)\)',
        rf'<a href="\2" style="{STYLE_LINK}">\1</a>',
        texto
    )
    
    # Bold: **texto**
    texto = re.sub(
        r'\*\*([^\*]+)\*\*',
        rf'<strong style="{STYLE_STRONG}">\1</strong>',
        texto
    )
    
    # Italic: *texto* (apenas se não faz parte de **texto**)
    # Usa negative lookbehind/lookahead para evitar pegar ** já processado
    texto = re.sub(
        r'(?<!\*)\*(?!\*)([^\*]+)\*(?!\*)',
        r'<em>\1</em>',
        texto
    )
    
    return texto

def renderizar_paragrafo(texto, is_first=False):
    """Renderiza parágrafo com possíveis links inline."""
    texto_processado = renderizar_inline_markdown(texto)
    style = STYLE_PARAGRAFO
    if is_first:
        # Primeiro parágrafo: zerar padding/margin topo explicitamente
        style = "margin:0 0 16px; padding:0; line-height:1.6; font-size:16px; color:#1a1a1a; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;"
    return f'<p style="{style}">{texto_processado}</p>\n'

def renderizar_heading2(texto):
    """Renderiza H2."""
    texto_processado = renderizar_inline_markdown(texto)
    return f'<h2 style="{STYLE_HEADING2}">{texto_processado}</h2>\n'

def renderizar_bullets(items):
    """Renderiza lista de bullets."""
    html = f'<ul style="{STYLE_UL}">\n'
    for item in items:
        item_processado = renderizar_inline_markdown(item)
        html += f'<li style="{STYLE_LI}">{item_processado}</li>\n'
    html += '</ul>\n'
    return html

def renderizar_video_embed(youtube_id, gancho, titulo=None, cta="▶ Assistir no YouTube", url_destino=None):
    """
    Renderiza embed de vídeo do YouTube com BOTÃO CTA PROEMINENTE:
    - Título opcional (hyperlink centralizado, bold, acima do thumbnail)
    - Capa maxresdefault.jpg (clicável)
    - Botão CTA estilo pílula sólida embaixo (padding generoso, cor marca)

    Args:
        youtube_id: ID do vídeo do YouTube (usado apenas para a thumbnail)
        gancho: Texto de gancho antes do vídeo (pode ser vazio)
        titulo: Título opcional do vídeo (default: None)
        cta: Texto do botão CTA (default: "▶ Assistir no YouTube")
        url_destino: URL de destino dos cliques (default: URL do YouTube)
    """
    youtube_url = f"https://www.youtube.com/watch?v={youtube_id}"
    url_clique = url_destino if url_destino else youtube_url

    html = ""

    # Gancho (se houver)
    if gancho:
        gancho_processado = renderizar_inline_markdown(gancho)
        html += f'<p style="{STYLE_PARAGRAFO}">{gancho_processado}</p>\n'

    html += '<table style="width:100%; max-width:600px; margin:24px auto; border-collapse:collapse;">\n'

    # Título (se houver) — ANTES do thumbnail
    if titulo and titulo.strip():
        html += '  <tr>\n'
        html += '    <td style="padding:0 0 20px 0; text-align:center;">\n'
        html += f'      <a href="{url_clique}" target="_blank" style="color:#1a1a1a; text-decoration:none; font-size:18px; font-weight:700; line-height:1.3; font-family:-apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, Helvetica, Arial, sans-serif; display:inline-block;">{titulo}</a>\n'
        html += '    </td>\n'
        html += '  </tr>\n'

    # Thumbnail
    html += '  <tr>\n'
    html += '    <td style="padding:0;">\n'
    html += f'      <a href="{url_clique}" target="_blank" style="display:block; text-decoration:none;">\n'
    html += f'        <img src="https://img.youtube.com/vi/{youtube_id}/maxresdefault.jpg" alt="Assistir o vídeo no YouTube" width="600" style="width:100%; max-width:600px; height:auto; display:block; border-radius:12px; border:0;">\n'
    html += '      </a>\n'
    html += '    </td>\n'
    html += '  </tr>\n'

    # Botão CTA
    html += '  <tr>\n'
    html += '    <td style="padding:24px 0 0 0; text-align:center;">\n'
    html += f'      <a href="{url_clique}" target="_blank" style="display:inline-block; background-color:#dc2626; color:#ffffff; text-decoration:none; padding:16px 40px; border-radius:10px; font-size:16px; font-weight:600; font-family:-apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, Helvetica, Arial, sans-serif; line-height:1.2;">{cta}</a>\n'
    html += '    </td>\n'
    html += '  </tr>\n'
    html += '</table>\n'
    return html

def renderizar_cta_botao_link(texto, url):
    """Renderiza CTA como link inline (não botão separado)."""
    texto_processado = renderizar_inline_markdown(texto)
    return f'<p style="{STYLE_PARAGRAFO}"><a href="{url}" style="{STYLE_LINK}">{texto_processado}</a></p>\n'

def renderizar_assinatura():
    """Renderiza assinatura canônica (4 linhas literais, foto circular via sites.{{DOMINIO}})."""
    html = f'<hr style="{STYLE_HR}">\n'
    html += '<table style="width:100%; border-spacing:0; border-collapse:collapse; font-family:-apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, Helvetica, Arial, sans-serif;">\n'
    html += '<tr>\n'
    html += '<td style="width:96px; vertical-align:top; padding-right:16px;"><img src="https://sites.{{DOMINIO}}/assets-gui/foto-gui-barcelona-circular.png" alt="Gui Ávila" width="96" height="96" style="width:96px; height:96px; border-radius:50%; object-fit:cover; object-position:center 25%; display:block; border:0;"></td>\n'
    html += '<td style="vertical-align:top; font-size:14px; line-height:1.5; color:#4a4a4a;">\n'
    html += '<strong style="color:#1a1a1a; font-size:16px; font-weight:700; display:block; margin-bottom:4px;">Gui Ávila</strong>\n'
    html += '<span style="display:block; font-size:14px; line-height:1.5; color:#4a4a4a;">Fundador e CEO da <a href="https://{{DOMINIO}}/{{lms_slug}}" style="color:#2563eb; text-decoration:underline; font-size:inherit;">{{LMS}}</a></span>\n'
    html += '<span style="display:block; font-size:14px; line-height:1.5; color:#4a4a4a;">Autor do Sistema Reverso, Automações PRO e ClickUp 8x</span>\n'
    html += '<span style="display:block; font-size:14px; line-height:1.5; color:#4a4a4a;">Fundador do {{EMPRESA_NEGOCIO}}</span>\n'
    html += '<span style="display:block; font-size:14px; line-height:1.5; color:#4a4a4a;">Site: <a href="https://{{DOMINIO}}" style="color:#2563eb; text-decoration:underline; font-size:inherit;">{{DOMINIO}}</a></span>\n'
    html += '</td>\n'
    html += '</tr>\n'
    html += '</table>\n'
    return html

def renderizar_newsletter(config):
    """
    Renderiza newsletter completa a partir de config JSON.

    Formato esperado:
    {
      "saudacao": "Oi {{contact.first_name}}!",
      "corpo_secoes": [
        {"tipo": "paragrafo", "texto": "..."},
        {"tipo": "heading2", "texto": "..."},
        {"tipo": "bullets", "items": ["...", "..."]},
        {"tipo": "video_embed", "youtube_id": "...", "gancho": "...", "titulo": "...", "cta": "..."},
        {"tipo": "cta_botao_link", "texto": "...", "url": "..."}
      ],
      "assinatura_padrao": true
    }

    Nota: campos opcionais em video_embed:
      - "titulo": título do vídeo (hyperlink acima do thumbnail)
      - "cta": texto do botão (default: "▶ Assistir no YouTube")
      - "gancho": texto antes do vídeo (pode ser "")
    """
    html = ""

    # Saudação (sempre primeiro elemento)
    if "saudacao" in config:
        html += renderizar_paragrafo(config["saudacao"], is_first=True)
        html += "\n"  # Linha em branco entre seções
    
    # Corpo
    for secao in config.get("corpo_secoes", []):
        tipo = secao["tipo"]

        if tipo == "paragrafo":
            html += renderizar_paragrafo(secao["texto"])
        elif tipo == "heading2":
            html += renderizar_heading2(secao["texto"])
        elif tipo == "bullets":
            html += renderizar_bullets(secao["items"])
        elif tipo == "video_embed":
            titulo = secao.get("titulo", None)
            gancho = secao.get("gancho", "")
            cta = secao.get("cta", "▶ Assistir no YouTube")
            url_destino = secao.get("url_destino", None)
            html += renderizar_video_embed(secao["youtube_id"], gancho, titulo=titulo, cta=cta, url_destino=url_destino)
        elif tipo == "cta_botao_link":
            html += renderizar_cta_botao_link(secao["texto"], secao["url"])
        else:
            print(f"AVISO: tipo de seção desconhecido: {tipo}", file=sys.stderr)

        html += "\n"  # Linha em branco entre seções
    
    # Assinatura
    if config.get("assinatura_padrao", True):
        html += renderizar_assinatura()
    
    return html

def wrap_editable_mode(html_content):
    """
    Envolve HTML de newsletter em modo editável.
    
    Args:
        html_content: HTML fragmento gerado pelo renderizar_newsletter()
    
    Returns:
        HTML completo com DOCTYPE, contenteditable, botão copy e scripts
    """
    
    edit_css = """
    <style>
        /* Estilos específicos do modo editável */
        .edit-container {
            max-width: 600px;
            margin: 40px auto;
            padding: 20px;
            background: #ffffff;
            position: relative;
        }
        
        .edit-container[contenteditable="true"]:hover {
            outline: 1px solid rgba(37, 99, 235, 0.3);
        }
        
        .edit-container[contenteditable="true"]:focus {
            outline: 2px solid rgba(37, 99, 235, 0.5);
            outline-offset: 2px;
        }
        
        /* Botão flutuante */
        #copy-button {
            position: fixed;
            top: 20px;
            right: 20px;
            background-color: #1a1a1a;
            color: #ffffff;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            cursor: pointer;
            z-index: 9999;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            transition: background-color 0.2s ease, transform 0.1s ease;
        }
        
        #copy-button:hover {
            background-color: #2a2a2a;
            transform: translateY(-1px);
        }
        
        #copy-button:active {
            transform: translateY(0);
        }
        
        #copy-button.copied {
            background-color: #16a34a;
        }
        
        /* Tornar elementos editáveis visualmente detectáveis */
        .edit-container p:hover,
        .edit-container h2:hover,
        .edit-container li:hover {
            background-color: rgba(37, 99, 235, 0.05);
        }
        
        /* Prevenir quebra visual ao editar */
        .edit-container * {
            outline-offset: 2px;
        }
    </style>
    """
    
    edit_js = """
    <script>
        // Script de cópia para clipboard
        (function() {
            const button = document.getElementById('copy-button');
            const container = document.querySelector('.edit-container');
            
            button.addEventListener('click', function() {
                // Clonar o container
                const clone = container.cloneNode(true);
                
                // Remover atributos de edição
                clone.removeAttribute('contenteditable');
                clone.removeAttribute('spellcheck');
                clone.classList.remove('edit-container');
                
                // Limpar todos os atributos de edição recursivamente
                const allElements = clone.querySelectorAll('*');
                allElements.forEach(el => {
                    el.removeAttribute('contenteditable');
                    el.removeAttribute('spellcheck');
                    // Remover classes edit-only se houver
                    if (el.classList.contains('edit-container')) {
                        el.classList.remove('edit-container');
                    }
                });
                
                // Pegar HTML limpo
                const cleanHtml = clone.innerHTML;
                
                // Envelopar num documento HTML completo (necessário para GHL preservar charset UTF-8)
                const fullDocument = `<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Newsletter</title>
</head>
<body style="margin:0;padding:0;background-color:#ffffff;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">
${cleanHtml}
</body>
</html>`;
                
                // Copiar para clipboard
                // Tentar API moderna primeiro, fallback para execCommand
                if (navigator.clipboard && navigator.clipboard.writeText) {
                    navigator.clipboard.writeText(fullDocument)
                        .then(() => {
                            showSuccess();
                        })
                        .catch(() => {
                            // Fallback
                            fallbackCopy(cleanHtml);
                        });
                } else {
                    fallbackCopy(fullDocument);
                }
            });
            
            function fallbackCopy(text) {
                // Criar textarea temporário
                const textarea = document.createElement('textarea');
                textarea.value = text;
                textarea.style.position = 'fixed';
                textarea.style.top = '0';
                textarea.style.left = '0';
                textarea.style.opacity = '0';
                document.body.appendChild(textarea);
                textarea.focus();
                textarea.select();
                
                try {
                    document.execCommand('copy');
                    showSuccess();
                } catch (err) {
                    alert('Erro ao copiar. Tente selecionar manualmente e usar Cmd+C.');
                } finally {
                    document.body.removeChild(textarea);
                }
            }
            
            function showSuccess() {
                button.textContent = '✓ Copiado!';
                button.classList.add('copied');
                
                setTimeout(() => {
                    button.textContent = '📋 Copiar HTML final';
                    button.classList.remove('copied');
                }, 2000);
            }
        })();
    </script>
    """
    
    # Montar HTML completo
    full_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Newsletter - Modo Editável</title>
    {edit_css}
</head>
<body style="margin: 0; padding: 0; background-color: #f5f5f5; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
    <button id="copy-button">📋 Copiar HTML final</button>
    
    <div class="edit-container" contenteditable="true" spellcheck="false">
{html_content}
    </div>
    
    {edit_js}
</body>
</html>"""
    
    return full_html

def main():
    parser = argparse.ArgumentParser(description="Renderiza newsletter em HTML a partir de config JSON")
    parser.add_argument("--input", help="Path do arquivo JSON de config (ou stdin se omitido)")
    parser.add_argument("--output", required=True, help="Path do arquivo HTML de saída")
    parser.add_argument("--editable", action="store_true", help="Gera HTML em modo editável (contenteditable + botão copy)")
    
    args = parser.parse_args()
    
    # Ler config
    try:
        if args.input:
            with open(args.input, 'r', encoding='utf-8') as f:
                config = json.load(f)
        else:
            config = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"ERRO: JSON inválido: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"ERRO: arquivo não encontrado: {args.input}", file=sys.stderr)
        sys.exit(1)
    
    # Renderizar
    html = renderizar_newsletter(config)
    
    # Aplicar modo editável se solicitado
    if args.editable:
        html = wrap_editable_mode(html)
    
    # Escrever output
    try:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html, encoding='utf-8')
        print(f"HTML gerado: {args.output} ({len(html)} chars)", file=sys.stderr)
    except Exception as e:
        print(f"ERRO ao escrever output: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
