from script import Extractor
import os

if __name__ == "__main__":
    # Solicita parâmetros do usuário
    search_term = input("Enter the search term for YouTube: ")
    num_urls = int(input("How many videos would you like to download ? "))
    max_duration = int(input("What is the maximum video duration (in minutes) ? "))
    min_duration = int(input("What is the minimum video duration (in minutes) ? "))
    max_images = int(input("How many images would you like to extract from each video ? "))
    delete_video = input("Do you want to delete the videos after extracting images ? (y/n) ").lower() == "y"
    output_folder = input("Where would you like to save the images ? (e.g., './images'): ")
    video_folder = input("Where would you like to save the videos ? (e.g., './videos'): ")
    person_folder = input("Where would you like to save the person images ? (e.g., './persons'): ")
    yolo_model_path = input("Enter the path to the YOLO model file (e.g., 'yolo11m-pose.pt'): ")
    yolo_batch_size = int(input("Enter the batch size for YOLO processing: "))

    # Cria diretórios se não existirem
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(video_folder, exist_ok=True)
    os.makedirs(person_folder, exist_ok=True)
    
    # Executa a extração
    extractor = Extractor(
        search_query=search_term,
        num_urls=num_urls,
        max_images=max_images,
        max_duration=max_duration,
        min_duration=min_duration,
        delete_video=delete_video,
        output_folder=output_folder,
        video_folder=video_folder,
        person_folder=person_folder,
        yolo_model_path=yolo_model_path,
        yolo_batch_size=yolo_batch_size
    )
    extractor.extract_images_from_search()
