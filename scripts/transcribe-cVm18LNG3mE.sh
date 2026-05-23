#!/bin/bash
# Transcrição do vídeo https://www.youtube.com/watch?v=cVm18LNG3mE

cd "{{PATH_LOCAL}} IA {{NOME_OPERADOR}}/Squad Empresa {{NOME_OPERADOR}}"

python3 /tmp/transcribe_video.py "https://www.youtube.com/watch?v=cVm18LNG3mE" "$(pwd)"
