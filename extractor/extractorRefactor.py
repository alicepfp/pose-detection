from ultralytics import YOLO
from requests_html import HTMLSession
import pandas as pd
import os
import re
import cv2
import yt_dlp
import urllib
import glob
import random
import string
import torch

class YouTubeVideoImageExtractor:
    def __init__(self):
        """
        Inicializa a classe YouTubeVideoImageExtractor com uma sessão HTML e um modelo YOLOv8.

        A classe utiliza o modelo YOLO para extração de poses e o yt_dlp para baixar vídeos do YouTube.
        """
        self.session = HTMLSession()
        self.model = YOLO('yolov8s-pose.pt')

    def get_urls(self, text, limit=10):
        """
        Pesquisa no YouTube por um texto e retorna uma lista de URLs de vídeos.

        Parâmetros:
        - text (str): O texto de pesquisa para encontrar vídeos no YouTube.
        - limit (int): O número máximo de URLs a serem retornadas.

        Retorna:
        - list: Lista de URLs de vídeos encontrados.
        """
        try:
            query = urllib.parse.quote(text)
            url = f"https://www.youtube.com/results?search_query={query}"
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
        Verifica se a duração do vídeo está dentro do intervalo especificado.

        Parâmetros:
        - video_length (int): Duração do vídeo em segundos.
        - max_duration (int): Duração máxima permitida em minutos.
        - min_duration (int): Duração mínima permitida em minutos.

        Retorna:
        - bool: True se a duração estiver dentro do intervalo, caso contrário, False.
        """
        return min_duration * 60 < video_length < max_duration * 60

    def download_video(self, url, path='./videos', max_duration=15, min_duration=2):
        """
        Baixa um vídeo do YouTube e retorna o caminho do arquivo salvo.

        Parâmetros:
        - url (str): URL do vídeo no YouTube.
        - path (str): Caminho onde o vídeo será salvo.
        - max_duration (int): Duração máxima permitida em minutos.
        - min_duration (int): Duração mínima permitida em minutos.

        Retorna:
        - str: Caminho do vídeo baixado ou None se o vídeo não for válido.
        """
        ydl_opts = {
            'format': 'mp4',
            'outtmpl': os.path.join(path, '%(title)s.%(ext)s')
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                duration = info_dict.get("duration", 0)
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
        Retorna o maior número de label já utilizado para o nome fornecido.

        Parâmetros:
        - name (str): O nome base para o arquivo de imagem.
        - folder (str): O diretório onde as imagens estão armazenadas.

        Retorna:
        - int: O maior número de label encontrado.
        """
        path_pattern = os.path.join(folder, f"{name}_*.jpg")
        existing_files = glob.glob(path_pattern)
        if not existing_files:
            return 0
        existing_labels = map(lambda s: int(s.split('_')[-1].split('.')[0]), existing_files)
        return max(existing_labels)

    def extract_images_from_video(self, video, folder, max_images=20, silent=False):
        """
        Extrai imagens de um vídeo e salva em um diretório especificado.

        Parâmetros:
        - video (str): O caminho do vídeo a ser processado.
        - folder (str): O diretório onde as imagens serão salvas.
        - max_images (int): O número máximo de imagens a serem extraídas.
        - silent (bool): Se True, suprime as mensagens de sucesso.
        """
        vidcap = cv2.VideoCapture(video)
        count = 0
        if not os.path.exists(folder):
            os.makedirs(folder)
        r = string.ascii_lowercase + string.digits
        title_prefix = ''.join(random.sample(r, 5))
        fps = int(vidcap.get(cv2.CAP_PROP_FPS))
        total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
        max_images = min(max_images, total_frames)
        while count < max_images:
            ret, image = vidcap.read()
            if not ret:
                break
            file_name = f"img_{title_prefix}_{count + 1}.jpg"
            path = os.path.join(folder, file_name)
            try:
                cv2.imwrite(path, image)
                if cv2.imread(path) is None:
                    os.remove(path)
                else:
                    if not silent:
                        print(f"Image successfully written at {path}")
                count += 1
            except Exception as e:
                print(f"Failed to write image: {e}")
        vidcap.release()

    def yolo_person_extraction(self, folder, silent, batch_size=10):
        """
        Extrai pessoas das imagens usando o modelo YOLOv8 em lotes.

        Parâmetros:
        - folder (str): O diretório contendo as imagens a serem processadas.
        - batch_size (int): O número de imagens a serem processadas por vez.
        """
        model = self.model
        img_folder = folder
        all_data = []
        a = 1
        # Lista todas as imagens no diretório
        images = [os.path.join(img_folder, file) for file in os.listdir(img_folder)
                    if file.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        # Divide as imagens em lotes
        batches = [images[i:i + batch_size] for i in range(0, len(images), batch_size)]
        
        for batch in batches:
            # Carrega as imagens do lote
            loaded_images = [cv2.imread(img_path) for img_path in batch]
            
            # Executa o modelo YOLOv8 para detectar pessoas
            results = model(loaded_images)

            # Limpa a memória CUDA após o processamento de cada lote
            torch.cuda.empty_cache()

            # Processa os resultados das imagens
            for r in results:
                bound_box = r.boxes.xyxy  # Obtém as caixas delimitadoras
                conf = r.boxes.conf.tolist()  # Confiança das detecções
                keypoints = r.keypoints.xyn.tolist()  # Pontos chave das pessoas detectadas
                
                # Para cada detecção, verifica se a confiança é maior que 0.75
                for index, box in enumerate(bound_box):
                    if conf[index] > 0.75:
                        x1, y1, x2, y2 = box.tolist()
                        frame = r.orig_img  # A imagem original do resultado
                        pict = frame[int(y1):int(y2), int(x1):int(x2)] # Recorta a pessoa detectada
                        path = './persons'
                        if not os.path.exists(path):
                            os.makedirs(path)
                        file_name = f'person_{a}.jpg'
                        output_path = os.path.join(path, file_name)
                        
                        # Cria um dicionário com as coordenadas dos pontos chave
                        data = {'image_name': f'person_{a}.jpg'}
                        for j in range(len(keypoints[index])):
                            data[f'x{j}'] = keypoints[index][j][0]
                            data[f'y{j}'] = keypoints[index][j][1]
                            
                        try:
                            cv2.imwrite(output_path, pict)
                            if cv2.imread(output_path) is None:
                                os.remove(output_path)
                            else:
                                if not silent:
                                    print(f"Image successfully written at {output_path}")
                        except Exception as e:
                            print(f"Failed to write image: {e}")
                        
                        all_data.append(data)
                        a += 1

        # Salva os dados dos pontos chave em um arquivo CSV
        df = pd.DataFrame(all_data)
        csv_file_path = './keypoints.csv'
        df.to_csv(csv_file_path, index=False)

    def extract_images_from_search(self, search_query, num_urls=10, delete_video=False, max_images=20, silent=False, max_duration=15, min_duration=2, output_folder='./images'):
        """
        Extrai imagens de vídeos encontrados no YouTube com base em uma pesquisa.

        Parâmetros:
        - search_query (str): O termo de pesquisa a ser usado no YouTube.
        - num_urls (int): O número de vídeos a serem processados.
        - delete_video (bool): Se True, exclui o vídeo após o processamento.
        - max_images (int): O número máximo de imagens a serem extraídas de cada vídeo.
        - silent (bool): Se True, suprime as mensagens de sucesso.
        - max_duration (int): A duração máxima permitida dos vídeos em minutos.
        - min_duration (int): A duração mínima permitida dos vídeos em minutos.
        - output_folder (str): O diretório onde as imagens extraídas serão salvas.
        """
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        urls = self.get_urls(search_query, num_urls)
        count = 1
        for url in urls:
            video_file = self.download_video(url, max_duration=max_duration, min_duration=min_duration)
            if video_file:
                self.extract_images_from_video(video_file, folder=output_folder, max_images=max_images, silent=silent)
                if delete_video:
                    os.remove(video_file)
                count += 1
        self.yolo_person_extraction(folder=output_folder, silent=silent)

    def safe_filename(self, title):
        """
        Gera um nome seguro para um arquivo a partir do título fornecido.

        Parâmetros:
        - title (str): O título a ser convertido em nome de arquivo seguro.

        Retorna:
        - str: O nome do arquivo seguro.
        """
        safe_title = re.sub(r'[<>:"/\\|?*]', '', title)
        safe_title = safe_title.replace(" ", "_")
        return safe_title
