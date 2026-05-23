#!/usr/bin/env python3
"""
Script canônico de envio de email via Resend API.
Usa RESEND_API_KEY de app/.env.local
Suporta attachments inline com CID reference.
"""

import argparse
import sys
import time
import base64
from pathlib import Path
import requests
import os

# Carregar .env.local manualmente (sem dependência dotenv)
env_path = Path(__file__).parent.parent.parent / "app" / ".env.local"
if env_path.exists():
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

def send_email(to: str, subject: str, html: str, from_email: str, preheader: str = None, reply_to: str = None, attachments_inline: list = None) -> dict:
    """Envia email via Resend API com retry. Suporta attachments inline para CID reference."""

    api_key = os.getenv("RESEND_API_KEY")
    if not api_key:
        print("ERRO: RESEND_API_KEY não encontrada em app/.env.local", file=sys.stderr)
        sys.exit(1)

    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "from": from_email,
        "to": [to],
        "subject": subject,
        "html": html
    }

    if preheader:
        # Adiciona preheader invisível no início do HTML
        preheader_html = f'<div style="display:none;max-height:0px;overflow:hidden;">{preheader}</div>'
        payload["html"] = preheader_html + html

    if reply_to:
        payload["reply_to"] = [reply_to]

    if attachments_inline:
        # Processa attachments inline (path:cid format)
        attachments = []
        for item in attachments_inline:
            if ':' not in item:
                print(f"ERRO: Attachment inline inválido (use path:cid): {item}", file=sys.stderr)
                sys.exit(1)

            file_path, cid = item.split(':', 1)
            file_path = Path(file_path).expanduser()

            if not file_path.exists():
                print(f"ERRO: Arquivo não encontrado: {file_path}", file=sys.stderr)
                sys.exit(1)

            # Ler e encodar em base64
            with open(file_path, 'rb') as f:
                content_b64 = base64.b64encode(f.read()).decode('utf-8')

            attachments.append({
                "filename": file_path.name,
                "content": content_b64,
                "content_id": cid
            })
            print(f"  Attachment inline: {file_path.name} → cid:{cid}")

        payload["attachments"] = attachments

    # Retry logic (2 tentativas)
    for attempt in range(2):
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)

            if response.status_code == 200:
                data = response.json()
                print(f"✓ Email enviado com sucesso")
                print(f"  Status: {response.status_code}")
                print(f"  Message ID: {data.get('id', 'N/A')}")
                print(f"  Destinatário: {to}")
                return data
            else:
                print(f"ERRO HTTP {response.status_code}: {response.text}", file=sys.stderr)
                if attempt == 0:
                    print("Tentando novamente em 2s...", file=sys.stderr)
                    time.sleep(2)
                else:
                    sys.exit(1)

        except requests.exceptions.RequestException as e:
            print(f"ERRO na requisição: {e}", file=sys.stderr)
            if attempt == 0:
                print("Tentando novamente em 2s...", file=sys.stderr)
                time.sleep(2)
            else:
                sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Envia email via Resend API")
    parser.add_argument("--to", default="{{EMAIL_OPERADOR}}", help="Destinatário")
    parser.add_argument("--subject", required=True, help="Assunto do email")
    parser.add_argument("--preheader", help="Preview text (opcional)")
    parser.add_argument("--html", help="Path do arquivo HTML")
    parser.add_argument("--body", help="HTML inline (alternativa a --html)")
    parser.add_argument("--from", dest="from_email", default="gui@email.{{DOMINIO}}", help="Remetente")
    parser.add_argument("--reply-to", dest="reply_to", help="Reply-to (opcional)")
    parser.add_argument("--attachment-inline", dest="attachments_inline", action="append", help="Attachment inline (formato: path:cid)")

    args = parser.parse_args()

    # Ler HTML do arquivo ou inline
    if args.html:
        html_path = Path(args.html)
        if not html_path.exists():
            print(f"ERRO: Arquivo HTML não encontrado: {args.html}", file=sys.stderr)
            sys.exit(1)
        html = html_path.read_text(encoding="utf-8")
    elif args.body:
        html = args.body
    else:
        print("ERRO: Forneça --html (arquivo) ou --body (inline)", file=sys.stderr)
        sys.exit(1)

    send_email(
        to=args.to,
        subject=args.subject,
        html=html,
        from_email=args.from_email,
        preheader=args.preheader,
        reply_to=args.reply_to,
        attachments_inline=args.attachments_inline
    )

if __name__ == "__main__":
    main()
