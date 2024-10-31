import urllib
from pytube import YouTube
from requests_html import HTMLSession
import cv2
import os
import glob


def get_urls(text, limit):
    """
    Busca URLs de vídeos no YouTube com base em um texto de pesquisa.

    Parâmetros:
    - text (str): O termo de pesquisa para buscar vídeos no YouTube.
    - limit (int): O número máximo de URLs de vídeos a serem retornadas.

    Retorna:
    - urls (list): Lista de URLs dos vídeos encontrados.
    """
    session = HTMLSession()
    try:
        # Cria a query para busca no YouTube
        query = urllib.parse.quote(text)
        url = f"https://www.youtube.com/results?search_query={query}"
        
        # Faz a requisição e renderiza a página
        response = session.get(url)
        response.html.render(sleep=1, keep_page=True, scrolldown=3)
        
        urls = []
        
        # Coleta os links dos vídeos e os anexa a uma lista
        for links in response.html.find('a#video-title'):
            link = next(iter(links.absolute_links))
            if link.startswith('https://www.youtube.com/watch'):
                urls.append(link)
                
                # Para se o número de URLs atingir o limite
                if len(urls) >= limit:
                    break

        print(f"Found {len(urls)} video links for {text}")
        print(urls)
        return urls  # Retorna a lista de URLs ao invés de apenas imprimir

    finally:
        # Garante que a sessão será fechada
        session.close()


def is_valid_duration(video_length, max_duration, min_duration):
    """
    Verifica se a duração de um vídeo está dentro dos limites especificados.

    Parâmetros:
    - video_length (int): A duração do vídeo em milissegundos.
    - max_duration (int): Duração máxima permitida do vídeo (em minutos).
    - min_duration (int): Duração mínima permitida do vídeo (em minutos).

    Retorna:
    - bool: `True` se a duração do vídeo estiver dentro dos limites, `False` caso contrário.
    """
    return min_duration * 60 * 1000 < video_length < max_duration * 60 * 1000


def download_video(url, path='./videos', max_duration=15, min_duration=2):
    """
    Faz o download de um vídeo do YouTube, se sua duração estiver dentro dos limites especificados.

    Parâmetros:
    - url (str): A URL do vídeo do YouTube a ser baixado.
    - path (str, opcional): O caminho para salvar o vídeo. Se `None`, será salvo no diretório atual.
    - max_duration (int): Duração máxima permitida do vídeo (em minutos). Padrão: 15 minutos.
    - min_duration (int): Duração mínima permitida do vídeo (em minutos). Padrão: 2 minutos.

    Retorna:
    - out_file (str ou None): O caminho do arquivo baixado, ou `None` se o download não for concluído.
    """
    try:
        yt = YouTube(url)
        duration = yt.length
        # Verifica se a duração do vídeo está dentro do limite especificado
        if is_valid_duration(duration, max_duration, min_duration):
            yt = yt.streams.filter(file_extension='mp4').first()
            out_file = yt.download(path)
            file_name = os.path.basename(out_file)
            print(f"Downloaded {file_name} correctly!")
            return out_file
        else:
            print(f"Video {url} is too long or too short.")
    except Exception as exc:
        print(f"Failed to download {url}: {exc}")
    return None


def download_videos(urls, path='./videos', max_duration=15, min_duration=2):
    """
    Faz o download de uma lista de vídeos do YouTube, respeitando as condições de duração.

    Parâmetros:
    - urls (list): Lista de URLs dos vídeos a serem baixados.
    - path (str, opcional): O caminho para salvar os vídeos. Se `None`, serão salvos no diretório atual.
    - max_duration (int): Duração máxima permitida dos vídeos (em minutos).
    - min_duration (int): Duração mínima permitida dos vídeos (em minutos).

    Retorna:
    - list: Lista de caminhos dos arquivos de vídeo baixados com sucesso.
    """
    downloaded_files = []
    for url in urls:
        video_file = download_video(url, path=path, max_duration=max_duration, min_duration=min_duration)
        if video_file:
            downloaded_files.append(video_file)
    return downloaded_files


def max_label(name, folder):
    """
    Encontra o maior índice numérico de arquivos existentes no formato `name_*.jpg`.

    Parâmetros:
    - name (str): O prefixo do nome dos arquivos.
    - folder (str): O diretório onde os arquivos são procurados.

    Retorna:
    - int: O maior índice encontrado, ou 0 se nenhum arquivo existir.
    """
    path_pattern = os.path.join(folder, f"{name}_*.jpg")
    existing_files = glob.glob(path_pattern)
    if not existing_files:
        return 0
    existing_labels = map(lambda s: int(s.split('_')[-1].split('.')[0]), existing_files)
    return max(existing_labels)


def extract_images_from_video(video, folder=None, delay=30, name="file", max_images=20, silent=False):
    """
    Extrai frames de um vídeo e salva como imagens em um diretório específico.

    Parâmetros:
    - video (str): O caminho do arquivo de vídeo.
    - folder (str, opcional): O diretório onde as imagens serão salvas. Se `None`, será o diretório atual.
    - delay (int): O tempo de atraso (em segundos) entre cada frame extraído.
    - name (str): O prefixo do nome de arquivo para as imagens.
    - max_images (int): Número máximo de imagens a serem extraídas do vídeo.
    - silent (bool): Se `True`, suprime as mensagens de sucesso. Padrão: `False`.
    """
    vidcap = cv2.VideoCapture(video)
    count = 0
    num_images = 0
    if not folder:
        folder = os.getcwd()
    label = max_label(name, folder)
    success = True
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))
    
    while success and num_images < max_images:
        success, image = vidcap.read()
        if not success:
            break
        
        label += 1
        file_name = f"{name}_{label}.jpg"
        path = os.path.join(folder, file_name)
        try:
            cv2.imwrite(path, image)
            # Verifica se a imagem foi gravada corretamente
            if cv2.imread(path) is None:
                os.remove(path)
            else:
                if not silent:
                    print(f'Image successfully written at {path}')
            num_images += 1
        except Exception as e:
            print(f"Failed to write image: {e}")
        count += delay * fps
        vidcap.set(1, count)

    vidcap.release()  # Fecha a captura de vídeo adequadamente


def extract_images_from_word(text, delete_video=False, image_delay=30, num_urls=10, max_images=20, name="file", max_duration=15, silent=False, urls=None):
    """
    Extrai imagens de vídeos baseados em uma pesquisa de texto no YouTube.

    Parâmetros:
    - text (str): O termo de pesquisa no YouTube para encontrar vídeos.
    - delete_video (bool): Se `True`, apaga os vídeos após a extração de imagens.
    - image_delay (int): O tempo de atraso (em segundos) entre cada frame extraído do vídeo.
    - num_urls (int): O número de URLs de vídeos a serem baixados.
    - max_images (int): O número máximo de imagens a serem extraídas por vídeo.
    - name (str): O prefixo dos arquivos de imagem gerados.
    - max_duration (int): A duração máxima dos vídeos a serem baixados (em minutos).
    - silent (bool): Se `True`, suprime as mensagens de sucesso. Padrão: `False`.
    - urls (list, opcional): Uma lista de URLs de vídeos para processar. Se `None`, os vídeos serão buscados a partir do texto de pesquisa.
    """
    if not os.path.exists(name):
        os.mkdir(name)
        
    # Obtém URLs se não forem passados
    if not urls:
        urls = get_urls(text, num_urls)
        
    downloaded_videos = download_videos(urls, max_duration=max_duration)
    
    for video in downloaded_videos:
        extract_images_from_video(video, folder=name, delay=image_delay, name=name, max_images=max_images, silent=silent)
        if delete_video:
            os.remove(video)


search_term = input('Search query: ')
urls = get_urls(search_term, limit=15)
download_videos(urls)
