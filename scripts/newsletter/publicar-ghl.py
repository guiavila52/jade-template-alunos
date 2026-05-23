#!/usr/bin/env python3
"""
publicar-ghl.py — Cria campanha no GHL e envia email de teste para aprovação.

Uso:
  python3 scripts/newsletter/publicar-ghl.py \
    --html workspace/output/newsletter/YYYY-MM-DD-slug-preview.html \
    --md   workspace/output/newsletter/YYYY-MM-DD-slug.md

Fluxo:
  1. Lê HTML renderizado + frontmatter do .md
  2. Cria campanha no GHL como draft
  3. Envia email de teste via Resend para {{EMAIL_OPERADOR}}
  4. Retorna URL GHL + instrução de OK para agendar
"""

import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error

# ─── Config ──────────────────────────────────────────────────────────────────

LOCATION_ID   = os.environ.get("GHL_LOCATION_ID", "CsiBUbUirVZnXWpyDivf")
USER_ID       = "NOOTHv2vbo1S52MK00Dm"
FROM_NAME     = "{{NOME_OPERADOR}}"
FROM_EMAIL    = "{{EMAIL_OPERADOR}}"
TEST_EMAIL    = "{{EMAIL_OPERADOR}}"
TIMEZONE      = "America/Sao_Paulo"
GHL_BASE      = f"https://services.leadconnectorhq.com/emails/public/v2/locations/{LOCATION_ID}"
RESEND_URL    = "https://api.resend.com/emails"

GHL_HEADERS = lambda key: {
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json",
    "Version": "2023-02-21",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

# ─── Helpers ─────────────────────────────────────────────────────────────────

def load_env():
    env_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "../../app/.env.local"))
    if not os.path.exists(env_path):
        return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


def parse_frontmatter(md_path: str) -> dict:
    with open(md_path, encoding="utf-8") as f:
        content = f.read()
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            v = v.strip().strip('"\'\' ')  # remove aspas YAML
            fm[k.strip()] = v
    return fm


def read_html(html_path: str) -> str:
    with open(html_path, encoding="utf-8") as f:
        return f.read()


def wrap_html_for_email(fragment: str, title: str) -> str:
    """Envolve o fragment HTML num wrapper email-safe completo."""
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title}</title>
</head>
<body style="margin:0;padding:0;background-color:#f5f5f5;font-family:Arial,Helvetica,sans-serif;">
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color:#f5f5f5;">
<tr><td style="padding:32px 16px;">
<table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" align="center"
  style="max-width:600px;width:100%;margin:0 auto;background-color:#ffffff;border-radius:8px;overflow:hidden;">
<tr><td style="padding:40px;">
{fragment}
</td></tr>
</table>
</td></tr>
</table>
</body>
</html>"""


def post_json(url: str, payload: dict, headers: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"❌ HTTP {e.code}: {body}")
        sys.exit(1)


def create_ghl_campaign(name: str, subject: str, html_body: str, ghl_key: str) -> dict:
    payload = {
        "name": name,
        "subject": subject,
        "fromName": FROM_NAME,
        "fromAddress": FROM_EMAIL,
        "editorType": "html",
        "editorContent": html_body,
        "timeZone": TIMEZONE,
        "userId": USER_ID,
    }
    return post_json(f"{GHL_BASE}/campaigns/email-campaign", payload, GHL_HEADERS(ghl_key))


def send_test_email(subject: str, html_full: str, campaign_url: str, resend_key: str):
    """Envia email de teste via Resend com banner de identificação."""
    test_banner = f"""
<div style="background:#fef3c7;border:2px solid #f59e0b;padding:12px 16px;margin-bottom:24px;border-radius:6px;font-family:Arial,sans-serif;font-size:13px;color:#92400e;">
  <strong>⚠️ TESTE — não é o disparo real</strong><br>
  Campanha criada no GHL: <a href="{campaign_url}" style="color:#92400e;">{campaign_url}</a><br>
  Se estiver tudo certo, responda OK no chat da Jade para agendar.
</div>
"""
    # Inserir banner no topo do body (primeira célula de conteúdo = padding:40px)
    html_with_banner = html_full.replace(
        '<td style="padding:40px;">',
        f'<td style="padding:40px;">{test_banner}',
        1
    )

    payload = {
        "from": f"{FROM_NAME} <gui@email.{{DOMINIO}}>",
        "to": [TEST_EMAIL],
        "subject": f"[TESTE] {subject}",
        "html": html_with_banner,
    }
    headers = {
        "Authorization": f"Bearer {resend_key}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    result = post_json(RESEND_URL, payload, headers)
    return result


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--html",    required=True)
    parser.add_argument("--md",      required=False)
    parser.add_argument("--name",    help="Nome da campanha (substitui frontmatter)")
    parser.add_argument("--subject", help="Assunto (substitui frontmatter)")
    args = parser.parse_args()

    load_env()
    ghl_key    = os.environ.get("GHL_API_KEY", "")
    resend_key = os.environ.get("RESEND_API_KEY", "")

    if not ghl_key:
        print("❌ GHL_API_KEY não encontrado.")
        sys.exit(1)
    if not resend_key:
        print("❌ RESEND_API_KEY não encontrado.")
        sys.exit(1)

    if not os.path.exists(args.html):
        print(f"❌ HTML não encontrado: {args.html}")
        sys.exit(1)

    html_fragment = read_html(args.html)
    fm = parse_frontmatter(args.md) if args.md else {}
    campaign_name = args.name    or fm.get("title",         os.path.basename(args.html).replace(".html", ""))
    subject       = args.subject or fm.get("email_subject") or fm.get("title", campaign_name)

    # 1. Criar campanha no GHL
    print(f"📧 Criando campanha no GHL...")
    print(f"   Nome: {campaign_name}")
    print(f"   Assunto: {subject}")
    result = create_ghl_campaign(campaign_name, subject, html_fragment, ghl_key)
    campaign_id  = result.get("id", "")
    campaign_url = f"https://highlevel.{{DOMINIO}}/location/{LOCATION_ID}/emails/campaigns/create/{campaign_id}"
    print(f"   ✅ Criada! ID: {campaign_id}")

    # 2. Enviar email de teste via Resend
    print(f"\n📨 Enviando teste para {TEST_EMAIL}...")
    html_full = wrap_html_for_email(html_fragment, campaign_name)
    test_result = send_test_email(subject, html_full, campaign_url, resend_key)
    test_id = test_result.get("id", "?")
    print(f"   ✅ Teste enviado! (Resend ID: {test_id})")

    # 3. Resumo final
    print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Newsletter pronta para aprovação

Campanha GHL (draft):
{campaign_url}

Teste enviado para: {TEST_EMAIL}

👉 Verifique o email e diga OK no chat para agendar.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━""")


if __name__ == "__main__":
    main()
