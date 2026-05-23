#!/usr/bin/env python3
"""
Corta primeiro minuto de vídeo YouTube e converte pra vertical 9:16 com gancho no final.

Uso:
    python scripts/video/cortar-youtube.py \
        --url "https://youtube.com/watch?v=..." \
        --duracao 60 \
        --gancho-texto "Curtiu? Ver vídeo completo no YouTube — link na bio" \
        --output-name "meu-video"

Dependências:
    - yt-dlp (brew install yt-dlp)
    - ffmpeg + ffprobe (brew install ffmpeg)
"""

import argparse
import subprocess
import sys
import os
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

def check_dependencies():
    """Valida se yt-dlp e ffmpeg estão instalados."""
    try:
        subprocess.run(['yt-dlp', '--version'], capture_output=True, check=True, timeout=5)
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        print("❌ yt-dlp não encontrado. Instale com: brew install yt-dlp", file=sys.stderr)
        sys.exit(1)
    
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True, timeout=5)
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        print("❌ ffmpeg não encontrado. Instale com: brew install ffmpeg", file=sys.stderr)
        sys.exit(1)
    
    try:
        subprocess.run(['ffprobe', '-version'], capture_output=True, check=True, timeout=5)
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        print("❌ ffprobe não encontrado. Instale com: brew install ffmpeg", file=sys.stderr)
        sys.exit(1)

def download_video(url, duracao, temp_dir):
    """Baixa vídeo YouTube (apenas trecho especificado)."""
    output_path = os.path.join(temp_dir, 'downloaded.%(ext)s')
    end_time = f"0:{duracao}"
    
    cmd = [
        'yt-dlp',
        '--download-sections', f'*0:00-{end_time}',
        '--force-keyframes-at-cuts',
        '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        '--merge-output-format', 'mp4',
        '-o', output_path,
        url
    ]
    
    print(f"🔽 Baixando primeiros {duracao}s do vídeo...")
    
    # Retry até 2x
    for attempt in range(2):
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,
                check=True
            )
            
            # Encontra arquivo baixado
            downloaded_files = list(Path(temp_dir).glob('downloaded.*'))
            if not downloaded_files:
                raise FileNotFoundError("Nenhum arquivo baixado encontrado")
            
            downloaded = downloaded_files[0]
            print(f"✅ Download concluído: {downloaded.name}")
            return str(downloaded)
            
        except subprocess.TimeoutExpired:
            print(f"⏱️ Timeout no download (tentativa {attempt + 1}/2)", file=sys.stderr)
            if attempt == 1:
                raise
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro no download (tentativa {attempt + 1}/2): {e.stderr}", file=sys.stderr)
            if attempt == 1:
                raise

def get_video_dimensions(video_path):
    """Retorna largura e altura do vídeo."""
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height',
        '-of', 'csv=s=x:p=0',
        video_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=10)
    width, height = map(int, result.stdout.strip().split('x'))
    return width, height

def crop_to_vertical(input_path, output_path, gancho_texto):
    """Converte vídeo pra 9:16 vertical com gancho no final."""
    print("🎬 Processando vídeo (crop vertical + gancho)...")
    
    # Get dimensões originais
    width, height = get_video_dimensions(input_path)
    
    # Calcula crop centrado pra 9:16
    # Novo width = height * 9/16
    new_width = int(height * 9 / 16)
    x_offset = int((width - new_width) / 2)
    
    # Filter complex: crop + scale + text overlay nos últimos 5s
    filter_complex = (
        f"[0:v]crop={new_width}:{height}:{x_offset}:0,scale=1080:1920,setsar=1[cropped];"
        f"[cropped]drawtext="
        f"text='{gancho_texto}':"
        f"fontfile=/System/Library/Fonts/Helvetica.ttc:"
        f"fontsize=48:"
        f"fontcolor=white:"
        f"borderw=3:"
        f"bordercolor=black:"
        f"x=(w-text_w)/2:"
        f"y=h-th-100:"
        f"enable='gte(t,n_frames-150/30)'"  # últimos ~5s (assumindo 30fps)
        f"[final]"
    )
    
    cmd = [
        'ffmpeg',
        '-i', input_path,
        '-filter_complex', filter_complex,
        '-map', '[final]',
        '-map', '0:a?',  # áudio se existir
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-movflags', '+faststart',
        '-y',
        output_path
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,
            check=True
        )
        print(f"✅ Vídeo processado: {output_path}")
        return output_path
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no ffmpeg: {e.stderr}", file=sys.stderr)
        raise
    except subprocess.TimeoutExpired:
        print("❌ Timeout no processamento ffmpeg", file=sys.stderr)
        raise

def validate_output(video_path):
    """Valida dimensões e duração do output final."""
    try:
        # Dimensões
        width, height = get_video_dimensions(video_path)
        if width != 1080 or height != 1920:
            print(f"⚠️ Dimensões inesperadas: {width}x{height} (esperado 1080x1920)", file=sys.stderr)
        
        # Duração
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            video_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=10)
        duracao = float(result.stdout.strip())
        
        print(f"📐 Dimensões: {width}x{height}")
        print(f"⏱️ Duração: {duracao:.1f}s")
        
        return True
        
    except Exception as e:
        print(f"⚠️ Falha na validação: {e}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description='Corta YouTube → vídeo vertical 9:16 com gancho')
    parser.add_argument('--url', required=True, help='URL do vídeo YouTube')
    parser.add_argument('--duracao', type=int, default=60, help='Duração em segundos (padrão: 60)')
    parser.add_argument('--gancho-texto', default='Curtiu? Vídeo completo no YouTube — link na bio', 
                        help='Texto do gancho final')
    parser.add_argument('--output-name', help='Nome do arquivo final (sem extensão)')
    
    args = parser.parse_args()
    
    # Valida dependências
    check_dependencies()
    
    # Prepara output path
    base_dir = Path(__file__).resolve().parent.parent.parent
    output_dir = base_dir / 'squad' / 'output' / 'videos-verticais'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if args.output_name:
        output_filename = f"{args.output_name}.mp4"
    else:
        timestamp = datetime.now().strftime('%Y-%m-%d-%H%M%S')
        output_filename = f"vertical-{timestamp}.mp4"
    
    output_path = output_dir / output_filename
    
    # Processa com temp dir
    temp_dir = tempfile.mkdtemp(prefix='youtube_vertical_')
    
    try:
        # 1. Download
        downloaded_path = download_video(args.url, args.duracao, temp_dir)
        
        # 2. Crop + gancho
        crop_to_vertical(downloaded_path, str(output_path), args.gancho_texto)
        
        # 3. Valida
        validate_output(str(output_path))
        
        print(f"\n🎉 Concluído: {output_path}")
        
        # Abre no visualizador (macOS)
        try:
            subprocess.run(['open', str(output_path)], timeout=5)
        except:
            pass
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}", file=sys.stderr)
        return 1
        
    finally:
        # Limpa temp files
        try:
            shutil.rmtree(temp_dir)
        except:
            pass

if __name__ == '__main__':
    sys.exit(main())
