import sys
import os
import requests
import re
from bs4 import BeautifulSoup
import shutil
import tempfile
from urllib.parse import urlparse, urlunparse
import img2pdf
from PIL import Image

def sanitize_filename(filename):
    """Remove caracteres inválidos de um nome de arquivo para evitar erros."""
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def normalize_slideshare_url(url):
    """Garante que a URL use a versão '/mobile/', que é mais consistente."""
    parsed_url = urlparse(url)
    if not parsed_url.path.startswith('/mobile/'):
        new_path = '/mobile' + parsed_url.path
        url = urlunparse(parsed_url._replace(path=new_path))
    return url

def crop_white_bars(image_path):
    """Detecta e corta as barras brancas das bordas de uma imagem."""
    try:
        im = Image.open(image_path)
        im = im.convert("RGBA")
        bbox = im.getbbox()
        
        if bbox is None:
            return

        cropped_im = im.crop(bbox)
        final_image = cropped_im.convert("RGB")
        final_image.save(image_path)
        
    except Exception as e:
        print(f"\n   -> Erro ao tentar cortar a imagem {os.path.basename(image_path)}: {e}")

def download_slides_as_pdf(url):
    """
    Função principal que baixa, processa e cria o PDF para uma única URL.
    """
    target_url = normalize_slideshare_url(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }
    
    try:
        print(f"🌐 Conectando-se ao SlideShare em: {target_url}")
        response = requests.get(target_url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Falha na conexão ou erro ao acessar a página: {e}")
        return

    print("✅ Conexão bem-sucedida! Analisando o conteúdo...")
    soup = BeautifulSoup(response.text, 'html.parser')

    print("📄 Procurando o título da apresentação...")
    title_tag = soup.find('h1', class_='Metadata_title__aM3nZ')
    if title_tag:
        title = title_tag.get_text(strip=True)
        pdf_filename = sanitize_filename(title) + ".pdf"
        print(f"   - Título encontrado: '{title}'")
    else:
        pdf_filename = "slides.pdf"
        print(f"   - Título não encontrado. O PDF será salvo como '{pdf_filename}'.")

    print("🖼️  Analisando a página para encontrar as imagens dos slides...")
    image_tags = soup.find_all('img', class_='VerticalSlideImage_image__VtE4p')

    if not image_tags:
        print("\n❌ Não foi possível encontrar as imagens dos slides. O site pode ter mudado.")
        return

    print(f"   - Encontrei {len(image_tags)} slides!")
    image_urls = [
        srcset.strip().split(',')[-1].strip().split(' ')[0]
        for tag in image_tags if (srcset := tag.get('srcset'))
    ]
    
    temp_dir = tempfile.mkdtemp()
    print(f"📥 Baixando e processando {len(image_urls)} imagens...")
    image_paths = []
    try:
        for i, img_url in enumerate(image_urls):
            print(f"   - Processando imagem {i + 1}/{len(image_urls)}...", end='\r')
            try:
                img_response = requests.get(img_url, headers=headers, timeout=10)
                img_response.raise_for_status()
                extension = os.path.splitext(urlparse(img_url).path)[1] or '.jpg'
                img_path = os.path.join(temp_dir, f"slide_{i+1:03d}{extension}")
                
                with open(img_path, 'wb') as f:
                    f.write(img_response.content)
                
                crop_white_bars(img_path)
                image_paths.append(img_path)
            except requests.exceptions.RequestException:
                print(f"\n   -> Falha ao baixar a imagem {i + 1}. Pulando...")

        print("\n✅ Imagens baixadas e limpas.")

        if not image_paths:
            print("❌ Nenhuma imagem foi processada. Não é possível criar o PDF.")
            return

        print(f"⚙️  Montando o PDF '{pdf_filename}' com as imagens limpas...")
        pdf_bytes = img2pdf.convert(image_paths)
        with open(pdf_filename, "wb") as f:
            f.write(pdf_bytes)

        print(f"\n🎉 PDF '{pdf_filename}' criado com sucesso!")

    finally:
        print("🧹 Limpando arquivos temporários...")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

# --- NOVO BLOCO PRINCIPAL ---
if __name__ == "__main__":
    # Pega todos os argumentos passados depois do nome do script
    urls_to_download = sys.argv[1:]

    if not urls_to_download:
        print("\n❌ ERRO: Nenhum link foi fornecido.")
        print("\nCOMO USAR:")
        print("   python slidedownload.py <URL1> <URL2> ...")
        print("\nEXEMPLO:")
        print("   python slidedownload.py https://slideshare.net/link/para/apresentacao1")
        sys.exit(1) # Sai do script com um código de erro

    total_urls = len(urls_to_download)
    print(f"✨ Pronto para baixar {total_urls} apresentações. Começando...\n")
    
    for i, url in enumerate(urls_to_download, 1):
        print(f"==================================================")
        print(f"🚀 Processando link {i} de {total_urls}: {url}")
        print(f"==================================================")
        
        if "slideshare.net" not in url:
            print(f"⚠️ AVISO: A URL fornecida não parece ser do SlideShare. Pulando.")
            continue
            
        download_slides_as_pdf(url)
        print("\n")

    print("✅ Todos os links foram processados.")
