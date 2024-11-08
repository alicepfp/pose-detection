import os
import re
import cv2
import yt_dlp
from requests_html import HTMLSession
import urllib
import glob

class YouTubeVideoImageExtractor:
    def __init__(self):
        self.session = HTMLSession()

    def get_urls(self, text, limit=10):
        """
        Busca URLs de vídeos no YouTube com base em um texto de pesquisa.

        Parâmetros:
        - text (str): O termo de pesquisa para buscar vídeos no YouTube.
        - limit (int): O número máximo de URLs de vídeos a serem retornadas.

        Retorna:
        - urls (list): Lista de URLs dos vídeos encontrados.
        """
        try:
            query = urllib.parse.quote(text)
            url = f"https://www.youtube.com/results?search_query={query}"

            # Faz a requisição e renderiza a página
            response = self.session.get(url)
            response.html.render(sleep=1, keep_page=True, scrolldown=3)

            urls = []
            for links in response.html.find('a#video-title'):
                link = next(iter(links.absolute_links))
                if link.startswith('https://www.youtube.com/watch'):
                    urls.append(link)
                
                if len(urls) >= limit:
                    break

            return urls
        except Exception as exc:
            print(f"Error while fetching videos: {exc}")
            return []


    def is_valid_duration(self, video_length, max_duration, min_duration):
        """
        Verifica se a duração do vídeo está dentro dos limites de tempo.

        Parâmetros:
        - video_length (int): A duração do vídeo em segundos.
        - max_duration (int): Duração máxima permitida (em minutos).
        - min_duration (int): Duração mínima permitida (em minutos).
        """
        return min_duration * 60 < video_length < max_duration * 60

    def download_video(self, url, path='./videos', max_duration=15, min_duration=2):
        """
        Faz o download de um vídeo do YouTube, se sua duração estiver dentro dos limites especificados.
    
        Parâmetros:
        - url (str): A URL do vídeo do YouTube.
        - path (str): O caminho onde o vídeo será salvo.
        - max_duration (int): Duração máxima permitida (em minutos).
        - min_duration (int): Duração mínima permitida (em minutos).
        """
        ydl_opts = {
            'format': 'mp4',
            'outtmpl': os.path.join(path, '%(title)s.%(ext)s')
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                duration = info_dict.get("duration", 0)  # A duração do vídeo em segundos
            
                # Converte a duração para minutos
                duration_minutes = duration / 60
                print(f"Video {url} duration: {duration_minutes:.2f} minutes")
            
                if self.is_valid_duration(duration, max_duration, min_duration):
                    ydl.download([url])
                    return os.path.join(path, f"{info_dict['title']}.mp4")
                else:
                    print(f"Video {url} has invalid duration.")
        except Exception as exc:
            print(f"Error while downloading video {url}: {exc}")
    
        return None


    def max_label(self, name, folder):
        """
        Encontra o maior índice numérico de arquivos existentes no formato `name_*.jpg`.

        Parâmetros:
        - name (str): O prefixo do nome dos arquivos.
        - folder (str): O diretório onde os arquivos são procurados.

        Retorna:
        - int: O maior índice encontrado ou 0 se não houver arquivos.
        """
        path_pattern = os.path.join(folder, f"{name}_*.jpg")
        existing_files = glob.glob(path_pattern)
        if not existing_files:
            return 0
        existing_labels = map(lambda s: int(s.split('_')[-1].split('.')[0]), existing_files)
        return max(existing_labels)

    def extract_images_from_video(self, video, folder=None, name="file", max_images=20, silent=False):
        """
        Extrai frames de um vídeo e salva como imagens em um diretório específico, respeitando o limite de imagens.

        Parâmetros:
        - video (str): O caminho do arquivo de vídeo.
        - folder (str, opcional): O diretório onde as imagens serão salvas. Se `None`, será o diretório atual.
        - name (str): O prefixo do nome de arquivo para as imagens.
        - max_images (int): Número máximo de imagens a serem extraídas do vídeo.
        - silent (bool): Se `True`, suprime as mensagens de sucesso. Padrão: `False`.
        """
        vidcap = cv2.VideoCapture(video)
        count = 0
        if not folder:
            folder = os.getcwd()
    
        # Cria a pasta de imagens se não existir
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Calcula o FPS (frames por segundo)
        fps = int(vidcap.get(cv2.CAP_PROP_FPS))
    
        # Verifica o número total de frames disponíveis no vídeo
        total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Caso o número total de frames seja menor que o limite, ajusta max_images
        max_images = min(max_images, total_frames)

        # Extrai frames até atingir o limite de max_images
        while count < max_images:
            ret, image = vidcap.read()
            if not ret:
                break  # Se o vídeo terminou, sai do loop

            # Gera o nome do arquivo da imagem com o prefixo e número sequencial
            file_name = f"{name}_{count + 1}.jpg"
            path = os.path.join(folder, file_name)

            try:
                # Grava a imagem
                cv2.imwrite(path, image)
            
                # Verifica se a imagem foi gravada corretamente
                if cv2.imread(path) is None:
                    os.remove(path)  # Remove a imagem se não foi gravada corretamente
                else:
                    if not silent:
                        print(f"Image successfully written at {path}")
                count += 1
            except Exception as e:
                print(f"Failed to write image: {e}")

        vidcap.release()  # Fecha a captura de vídeo corretamente

    def extract_images_from_search(self, search_query, num_urls=10, delete_video=False, image_delay=30, max_images=20, name="file", silent=False, max_duration=15, min_duration=2):
        """
        Extrai imagens de vídeos baixados após buscar vídeos no YouTube.

        Parâmetros:
        - search_query (str): Termo de pesquisa no YouTube.
        - num_urls (int): Número de vídeos a serem baixados.
        - delete_video (bool): Se True, exclui os vídeos após extração das imagens.
        - image_delay (int): Atraso entre cada frame extraído.
        - max_images (int): Máximo de imagens a extrair por vídeo.
        - name (str): Prefixo do nome das imagens extraídas.
        - silent (bool): Se True, suprime as mensagens de sucesso.
        - max_duration (int): Duração máxima do vídeo (em minutos).
        - min_duration (int): Duração mínima do vídeo (em minutos).
        """
        # Verifica se os diretórios existem, caso contrário cria
        if not os.path.exists(name):
            os.makedirs(name)

        # Obtém URLs dos vídeos com base na pesquisa
        urls = self.get_urls(search_query, num_urls)
        
        # Inicializa o label sequencial
        label = 1
        
        for url in urls:
            video_file = self.download_video(url, max_duration=max_duration, min_duration=min_duration)

            if video_file:
                # Cria uma subpasta chamada "extraction{label}" para cada vídeo
                video_title = os.path.basename(video_file)
                image_folder = os.path.join(name, f"extraction{label}")
                if not os.path.exists(image_folder):
                    os.makedirs(image_folder)

                # Extraí as imagens
                self.extract_images_from_video(video_file, folder=image_folder, name=f"img{label}", max_images=max_images, silent=silent)

                # Exclui o vídeo se necessário
                if delete_video:
                    os.remove(video_file)

                # Incrementa o label para o próximo vídeo
                label += 1

    def safe_filename(self, title):
        """
        Limpa o título do vídeo para ser usado como nome de diretório ou arquivo.
        """
        safe_title = re.sub(r'[<>:"/\\|?*]', '', title)  # Remove caracteres inválidos
        safe_title = safe_title.replace(" ", "_")  # Substitui espaços por underscores
        return safe_title


