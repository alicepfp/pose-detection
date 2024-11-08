from extractorRefactor import YouTubeVideoImageExtractor

if __name__ == "__main__":
    extractor = YouTubeVideoImageExtractor()

    # Solicita parâmetros do usuário
    search_term = input("Enter the search term for YouTube: ")
    num_urls = int(input("How many videos would you like to download ? "))
    max_duration = int(input("What is the maximum video duration (in minutes) ? "))
    min_duration = int(input("What is the minimum video duration (in minutes) ? "))
    max_images = int(input("How many images would you like to extract from each video ? "))
    delete_video = input("Do you want to delete the videos after extracting images ? (y/n) ").lower() == "y"
    output_folder = input("Where would you like to save the images (videos will be saved at ./videos) ? ")

    # Executa a extração
    extractor.extract_images_from_search(
        search_query=search_term,
        num_urls=num_urls,
        delete_video=delete_video,
        max_images=max_images,
        name=output_folder,
        silent=False,
        max_duration=max_duration,
        min_duration=min_duration
    )
