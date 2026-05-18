---
name: gerar-imagem
description: Gera imagens via OpenRouter API (Flux, SDXL, Imagen). Output PNG local em workspace/output/imagens/.
type: skill
---


# /gerar-imagem

Gera imagens via OpenRouter API (Flux, SDXL, Imagen). Output: PNG local.


## Fluxo

```
Input (prompt + model + size + output path)
  ↓
1. Validar credenciais (OPENROUTER_API_KEY em app/.env.local)
2. Montar payload JSON (prompt, model, size, negative-prompt, seed)
3. POST OpenRouter API /images/generations
4. Aguardar resposta (base64 ou URL da imagem gerada)
5. Salvar PNG em path de output
6. Validar arquivo (file command → PNG image data)
  ↓
Output (path absoluto do PNG + estatísticas stderr)
```

## Uso

```bash
/gerar-imagem \
  --prompt "minimalist photo of entrepreneur in home office" \
  --model black-forest-labs/flux-schnell-free \
  --size 1024x1024 \
  --output workspace/output/imagens/teste.png
```

## Parâmetros

- `--prompt` (obrigatório): descrição da imagem em inglês
- `--model` (opcional): modelo OpenRouter
  - `black-forest-labs/flux-schnell-free` (default, rápido, grátis, boa qualidade)
  - `black-forest-labs/flux-pro` (qualidade premium, pago ~$0.05/img)
  - `stability-ai/stable-diffusion-xl` (SDXL, clássico, ~$0.03/img)
  - `google/imagen-3` (Imagen 3, fotorrealismo, ~$0.04/img)
  - `midjourney/v6` (se disponível, ~$0.08/img)
- `--size` (opcional): tamanho da imagem (default: 1024x1024)
  - Opções comuns: 1024x1024 (quadrado), 1024x1792 (9:16 vertical), 1792x1024 (16:9 horizontal)
- `--output` (obrigatório): caminho completo do PNG de saída
- `--negative-prompt` (opcional): o que NÃO incluir na imagem
- `--seed` (opcional): número inteiro para reprodutibilidade

## Credenciais

API key em `app/.env.local`:
```
OPENROUTER_API_KEY=sk-or-v1-...
```

Se faltar, script abre TextEdit automaticamente.

## Output

Script retorna caminho absoluto do PNG salvo.
Stderr: progresso + estatísticas.
Exit code: 0 sucesso, 1 erro.

## Exemplos

```bash
# Foto minimalista para carrossel
/gerar-imagem \
  --prompt "minimalist black-and-white portrait of young Brazilian entrepreneur in modern home office, natural lighting, Canon EOS R5" \
  --model black-forest-labs/flux-schnell-free \
  --size 1024x1024 \
  --output workspace/output/imagens/perfil-gui-2026-05-12.png

# Arte conceitual com Flux Pro
/gerar-imagem \
  --prompt "abstract visualization of AI agents working in harmony, cyberpunk aesthetic, purple and blue tones" \
  --model black-forest-labs/flux-pro \
  --size 1792x1024 \
  --output workspace/output/imagens/hero-squad-ai.png \
  --negative-prompt "text, watermark, people, faces"

# Produto fotorrealista com Imagen
/gerar-imagem \
  --prompt "sleek MacBook Pro on minimalist desk with coffee, morning light, product photography, 8K" \
  --model google/imagen-3 \
  --size 1024x1024 \
  --output workspace/output/imagens/setup-trabalho.png \
  --seed 42
```

## Integração com carrosséis

Fluxo típico:
1. Estrategista define conceito visual
2. Copywriter escreve prompt descritivo
3. `/gerar-imagem` gera 3-5 variações (seeds diferentes)
4. Squad-conteudo escolhe melhor
5. Triple-check visual + branding
6. Sobe no carrossel

## Custos (aproximados, 2026)

- Flux schnell free: $0.00/img (rápido, boa qualidade)
- Flux Pro: ~$0.05/img (premium)
- SDXL: ~$0.03/img
- Imagen 3: ~$0.04/img

Ver pricing atualizado: https://openrouter.ai/models

## Limitações

- Prompts em inglês geram melhor resultado
- Modelos grátis têm rate limit (checar doc OpenRouter)
- Rostos específicos ({{OPERADOR}}) = melhor usar foto real editada
- Texto em imagem (logos, frases) = adicionar depois no Figma/Canva

## Bateria de testes (Regra #24)

Antes de marcar 🟢:
- [ ] Teste real com prompt simples + Flux schnell
- [ ] Validar PNG (`file` command retorna PNG image data)
- [ ] Retry funciona (simular timeout)
- [ ] Erro sem key (remover OPENROUTER_API_KEY temporariamente)
- [ ] Negative prompt funciona
- [ ] Seed reproduz mesma imagem

## Próximos passos

- Integrar em `/criar-carrossel` (geração automática de elementos visuais)
- Galeria de prompts reutilizáveis (backgrounds, texturas, ícones)
- Upscale automático pra resoluções maiores
- A/B test visual (gerar 3 variações, escolher melhor)
