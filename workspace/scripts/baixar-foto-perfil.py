#!/usr/bin/env python3
"""
Baixa a foto de perfil do Gui do Google Drive e salva em cache local.
Roda quando a foto precisar ser atualizada.

Pasta no Drive: {{NOME_OPERADOR}} - Business > Materiais para Time de Marketing
             > Fotos e imagens (público) > Fotos de rosto quadrada
"""

# Para usar: este script precisa do token do Google Drive.
# Por enquanto, copie manualmente o arquivo /tmp/gui_barcelona.png
# para /tmp/gui_foto_perfil.png:
#
#   cp /tmp/gui_barcelona.png /tmp/gui_foto_perfil.png
#
# Quando o MCP do Google Drive estiver integrado via CLI,
# este script fará o download automaticamente.

import shutil
from pathlib import Path

src = Path("/tmp/gui_barcelona.png")
dst = Path("/tmp/gui_foto_perfil.png")

if src.exists():
    shutil.copy(src, dst)
    print(f"✅ Foto copiada para {dst}")
else:
    print("❌ Arquivo fonte não encontrado. Baixe a foto manualmente.")
