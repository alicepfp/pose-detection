from ultralytics import YOLO
from requests_html import HTMLSession
import pandas as pd
import os
import re
import cv2
import yt_dlp
import urllib
import random
import string
import torch

# Classe para gerenciar o download de vídeos do YouTube
class YouTubeDownloader:
    def __init__(self, session=None):
        # Inicializa a sessão, usando HTMLSession por padrão caso nenhuma seja fornecida
        self.session = session or HTMLSession()

    # Método para buscar vídeos no YouTube com base em uma consulta
    def get_video_urls(self, query, limit=10):
        try:
            encoded_query = urllib.parse.quote(query)  # Codifica a consulta para ser segura na URL
            search_url = f"https://www.youtube.com/results?search_query={encoded_query}"  # URL de busca no YouTube
            response = self.session.get(search_url)  # Realiza a requisição de busca
            response.html.render(sleep=1, keep_page=True, scrolldown=3)  # Renderiza o JavaScript e rola a página para carregar o conteúdo

            # Extrai os links dos vídeos e retorna os primeiros `limit` resultados
            urls = [link.absolute_links.pop() for link in response.html.find('a#video-title')
                    if link.absolute_links.pop().startswith('https://www.youtube.com/watch')][:limit]
            print(f"Videos found in search: {urls}")  # Exibe a lista de URLs encontradas
            return urls
        except Exception as exc:
            print(f"Error while searching videos: {exc}")
            return []

    # Método para baixar um vídeo a partir de uma URL
    def download_video(self, url, path='./videos', max_duration=15, min_duration=2):
        ydl_opts = {'format': 'mp4', 'outtmpl': os.path.join(path, '%(title)s.%(ext)s')}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)  # Extrai as informações do vídeo sem baixar
                duration = info.get("duration", 0)  # Obtém a duração do vídeo em segundos
                print(f"Video length ({url}): {duration / 60} minutes")  # Exibe a duração do vídeo
                if min_duration * 60 < duration < max_duration * 60:  # Verifica se a duração do vídeo está dentro do intervalo
                    ydl.download([url])  # Baixa o vídeo
                    return os.path.join(path, f"{info['title']}.mp4")  # Retorna o caminho do vídeo baixado
                print(f"Vídeo too long or too short.")
        except Exception as exc:
            print(f"Error downloading video {url}: {exc}")
        return None


# Classe para processar o vídeo baixado e extrair os frames
class VideoProcessor:
    def __init__(self, folder='./images'):
        # Inicializa a pasta para salvar as imagens extraídas
        self.folder = folder
        if not os.path.exists(folder):
            os.makedirs(folder)  # Cria a pasta caso não exista

    # Método para extrair frames de um vídeo e salvá-los como imagens
    def extract_images(self, video_path, max_images=20):
        vidcap = cv2.VideoCapture(video_path)  # Abre o arquivo de vídeo
        title_prefix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))  # Prefixo aleatório para o título
        count, fps, total_frames = 0, int(vidcap.get(cv2.CAP_PROP_FPS)), int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Loop através dos frames do vídeo
        while count < min(max_images, total_frames):  # Garante que não serão extraídos mais que `max_images` frames
            success, image = vidcap.read()
            if not success: break  # Sai do loop caso não consiga ler o frame
            path = os.path.join(self.folder, f"img_{title_prefix}_{count + 1}.jpg")  # Gera o caminho da imagem
            cv2.imwrite(path, image)  # Salva o frame como uma imagem
            if cv2.imread(path) is None: os.remove(path)  # Remove a imagem caso não tenha sido salva corretamente
            count += 1
        vidcap.release()  # Libera o objeto de captura do vídeo

# Classe para extrair poses (pontos chave) das imagens usando YOLOv11
class PoseExtractor:
    def __init__(self, model_path='yolo11n-pose.pt', output_folder='./persons', batch_size=10):
        # Carrega o modelo YOLO para detecção de poses\
        self.model = YOLO(model_path)
        self.output_folder = output_folder
        self.batch_size = batch_size
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)  # Cria a pasta para salvar as imagens das pessoas, caso não exista

    # Método para extrair poses (pontos chave) das imagens de uma pasta
    def extract_poses(self, image_folder, silent=True):
        images = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(('jpg', 'jpeg', 'png'))]
        batches = [images[i:i + self.batch_size] for i in range(0, len(images), self.batch_size)]  # Processa em lotes
        all_data, a = [], 1

        # Loop através dos lotes de imagens
        for batch in batches:
            results = self.model([cv2.imread(img) for img in batch])  # Detecta as poses no lote de imagens
            torch.cuda.empty_cache()  # Limpa a memória da GPU após cada lote

            # Processa os resultados de cada imagem do lote
            for result in results:
                for index, box in enumerate(result.boxes.xyxy):
                    if result.boxes.conf[index] > 0.75:  # Filtra as caixas com base no score de confiança
                        self.save_person_image(result, box, a, all_data)  # Salva a imagem da pessoa detectada
                        a += 1
        
        # Salva os dados de pontos chave extraídos em um arquivo CSV
        pd.DataFrame(all_data).to_csv(os.path.join(self.output_folder, 'keypoints.csv'), index=False)

    # Método para salvar a imagem recortada da pessoa e registrar os pontos chave
    def save_person_image(self, result, box, count, data):
        x1, y1, x2, y2 = map(int, box.tolist())  # Extrai as coordenadas da caixa delimitadora
        person_img = result.orig_img[y1:y2, x1:x2]  # Recorta a imagem para a caixa delimitadora da pessoa
    
        title_prefix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))  # Prefixo aleatório para o título
        file_name = f'person_{title_prefix}_{count}.jpg'
        path = os.path.join(self.output_folder, file_name)
    
        cv2.imwrite(path, person_img)  # Salva a imagem recortada

        if cv2.imread(path) is None:  # Verifica se a imagem foi salva corretamente
            print(f"Error saving image {file_name}, removing file.")
            os.remove(path)  # Remove o arquivo caso a imagem não tenha sido salva corretamente
        else:
            # Acessa os dados dos pontos chave da detecção
            keypoints_data = result.keypoints.xyn.tolist()
            max_keypoints = 17  # Define o número máximo de pontos chave (ajuste conforme o modelo YOLO usado)
        
            if len(keypoints_data) > 0:
                for person_idx, keypoints in enumerate(keypoints_data):
                    # Cria um dicionário para cada pessoa, com valores padronizados de 0.0
                    person_data = {'image_name': file_name}
                    for i in range(max_keypoints):
                        if i < len(keypoints):
                            person_data[f'x{i}'] = keypoints[i][0]
                            person_data[f'y{i}'] = keypoints[i][1]
                        else:
                            person_data[f'x{i}'] = 0.0
                            person_data[f'y{i}'] = 0.0
                    data.append(person_data)
            else:
                print(f"Warning: No key points detected for image {file_name}")


# Classe que integra o download de vídeos, processamento e extração de poses
class Extractor:
    def __init__(self, search_query, num_urls=10, max_images=20, max_duration=15, min_duration=2, delete_video=False,
                output_folder='./images', video_folder='./videos', person_folder='./persons', 
                yolo_model_path='yolo11n-pose.pt', yolo_batch_size=10):
        
        # Inicializa parâmetros para extração de vídeos e extração de poses
        self.search_query = search_query
        self.num_urls = num_urls
        self.max_images = max_images
        self.max_duration = max_duration
        self.min_duration = min_duration
        self.delete_video = delete_video
        self.output_folder = output_folder
        self.video_folder = video_folder
        self.person_folder = person_folder
        self.yolo_batch_size = yolo_batch_size
        self.yolo_model_path = yolo_model_path

        # Inicializa as classes para baixar vídeos, processar vídeos e extrair poses
        self.downloader = YouTubeDownloader()
        self.video_processor = VideoProcessor(self.output_folder)
        self.pose_extractor = PoseExtractor(model_path=self.yolo_model_path, output_folder=self.person_folder, batch_size=self.yolo_batch_size)

    # Método para baixar vídeos, extrair imagens e extrair poses
    def extract_images_from_search(self):
        if not os.path.exists(self.video_folder):
            os.makedirs(self.video_folder)  # Cria a pasta de vídeos, se não existir
        
        # Obtém URLs dos vídeos relacionados à consulta
        urls = self.downloader.get_video_urls(self.search_query, self.num_urls)
        
        for url in urls:
            # Baixa o vídeo e extrai imagens dele
            video_path = self.downloader.download_video(url, path=self.video_folder,
                                                        max_duration=self.max_duration,
                                                        min_duration=self.min_duration)
            if video_path:
                self.video_processor.extract_images(video_path, max_images=self.max_images)  # Extrai imagens do vídeo
                if self.delete_video:
                    os.remove(video_path)  # Remove o vídeo se a opção for ativada
        
        # Extrai poses das imagens salvas
        self.pose_extractor.extract_poses(self.output_folder)
