import os

class VideoFileManager:
    """
    Класс для управления видеофайлами
    """
    VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v']
    
    @staticmethod
    def get_video_files(folder_path):
        """
        Получает список всех видеофайлов в папке
        """
        if not os.path.exists(folder_path):
            print(f"Папка {folder_path} не существует!")
            return []
        
        video_files = []
        for file in os.listdir(folder_path):
            if any(file.lower().endswith(ext) for ext in VideoFileManager.VIDEO_EXTENSIONS):
                video_files.append(os.path.join(folder_path, file))
        
        return sorted(video_files)
    
    @staticmethod
    def print_video_list(video_files):
        """
        Красиво выводит список видеофайлов
        """
        print(f"Найдено видеофайлов: {len(video_files)}\n")
        for i, video_path in enumerate(video_files, 1):
            filename = os.path.basename(video_path)
            print(f"{i:2d}. {filename}")
        print()