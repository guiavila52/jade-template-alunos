#!/usr/bin/env python3
"""
Gerador de imagens via OpenRouter API
Suporta múltiplos modelos (Flux, SDXL, Imagen)
"""
import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv


def main():
    parser = argparse.ArgumentParser(description="Gera imagens via OpenRouter API")
    parser.add_argument("--prompt", required=True, help="Prompt de geração")
    parser.add_argument(
        "--model",
        default="black-forest-labs/flux-schnell-free",
        help="Modelo OpenRouter (default: flux-schnell-free)",
    )
    parser.add_argument(
        "--size", default="1024x1024", help="Tamanho da imagem (default: 1024x1024)"
    )
    parser.add_argument(
        "--output", required=True, help="Caminho do arquivo PNG de saída"
    )
    parser.add_argument("--negative-prompt", help="Prompt negativo (opcional)")
    parser.add_argument("--seed", type=int, help="Seed para reprodutibilidade (opcional)")
    args = parser.parse_args()

    # Carregar .env.local do app/
    env_path = Path(__file__).parent.parent.parent / "app" / ".env.local"
    if not env_path.exists():
        print(f"❌ Arquivo {env_path} não encontrado", file=sys.stderr)
        sys.exit(1)

    load_dotenv(env_path)
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        print(
            "❌ OPENROUTER_API_KEY não encontrada em app/.env.local",
            file=sys.stderr,
        )
        print(
            f"\n🔧 Abra o arquivo no TextEdit e adicione:\nOPENROUTER_API_KEY=sk-or-v1-...",
            file=sys.stderr,
        )
        os.system(f'open -a TextEdit "{env_path}"')
        sys.exit(1)

    # Parse tamanho
    try:
        width, height = map(int, args.size.lower().split("x"))
    except ValueError:
        print(f"❌ Tamanho inválido: {args.size}. Use formato WIDTHxHEIGHT", file=sys.stderr)
        sys.exit(1)

    # Construir payload
    payload = {
        "model": args.model,
        "prompt": args.prompt,
        "width": width,
        "height": height,
    }

    if args.negative_prompt:
        payload["negative_prompt"] = args.negative_prompt
    if args.seed is not None:
        payload["seed"] = args.seed

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://{{DOMINIO}}",
        "X-Title": "Squad Gui Avila - Image Generator",
    }

    url = "https://openrouter.ai/api/v1/images/generations"

    print(f"🎨 Gerando imagem com {args.model}...", file=sys.stderr)
    print(f"   Prompt: {args.prompt[:80]}...", file=sys.stderr)

    # Retry logic
    max_retries = 2
    for attempt in range(max_retries + 1):
        try:
            response = requests.post(
                url, headers=headers, json=payload, timeout=90
            )
            response.raise_for_status()
            break
        except requests.exceptions.RequestException as e:
            if attempt < max_retries:
                print(f"⚠️  Tentativa {attempt + 1} falhou, retry em 3s...", file=sys.stderr)
                time.sleep(3)
            else:
                print(f"❌ Falha após {max_retries + 1} tentativas: {e}", file=sys.stderr)
                sys.exit(1)

    data = response.json()

    # OpenRouter pode retornar diferentes estruturas
    if "data" in data and len(data["data"]) > 0:
        image_data = data["data"][0]
        if "b64_json" in image_data:
            b64_string = image_data["b64_json"]
        elif "url" in image_data:
            # Alguns modelos retornam URL em vez de base64
            img_url = image_data["url"]
            print(f"🔗 Baixando de {img_url}...", file=sys.stderr)
            img_response = requests.get(img_url, timeout=30)
            img_response.raise_for_status()
            img_bytes = img_response.content
            # Salvar direto
            output_path = Path(args.output).resolve()
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(img_bytes)
            print(f"✅ Imagem salva em {output_path}", file=sys.stderr)
            print(str(output_path))
            sys.exit(0)
        else:
            print(f"❌ Estrutura inesperada: {json.dumps(image_data)}", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"❌ Resposta sem imagem: {json.dumps(data)}", file=sys.stderr)
        sys.exit(1)

    # Decodificar base64
    try:
        img_bytes = base64.b64decode(b64_string)
    except Exception as e:
        print(f"❌ Falha ao decodificar base64: {e}", file=sys.stderr)
        sys.exit(1)

    # Salvar PNG
    output_path = Path(args.output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        output_path.write_bytes(img_bytes)
    except Exception as e:
        print(f"❌ Falha ao salvar arquivo: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"✅ Imagem salva em {output_path}", file=sys.stderr)
    print(str(output_path))


if __name__ == "__main__":
    main()
