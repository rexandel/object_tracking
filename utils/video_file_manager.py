import os
import shutil

class VideoFileManager:
    VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v']
    
    @staticmethod
    def get_video_files(folder_path):
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
        print(f"Найдено видеофайлов: {len(video_files)}\n")
        for i, video_path in enumerate(video_files, 1):
            filename = os.path.basename(video_path)
            print(f"{i:2d}. {filename}")
        print()
    
    @staticmethod
    def save_processed_video(input_path, output_dir, tracker_name, processed_video_path):
        if not os.path.exists(processed_video_path):
            print(f"Ошибка: файл {processed_video_path} не существует")
            return None
        
        os.makedirs(output_dir, exist_ok=True)
        
        input_filename = os.path.basename(input_path)
        input_name, input_ext = os.path.splitext(input_filename)

        output_filename = f"{input_name}_{tracker_name}{input_ext}"
        output_path = os.path.join(output_dir, output_filename)
        
        try:
            shutil.copy2(processed_video_path, output_path)
            print(f"Обработанное видео сохранено: {output_path}")
            return output_path
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")
            return None
    
    @staticmethod
    def create_tracker_output_dir(base_dir, tracker_name):
        output_dir = os.path.join(base_dir, f"{tracker_name}_videos")
        os.makedirs(output_dir, exist_ok=True)
        return output_dir
    
    @staticmethod
    def get_video_info(video_path):
        if not os.path.exists(video_path):
            return None
        
        filename = os.path.basename(video_path)
        size = os.path.getsize(video_path) / (1024 * 1024)
        return {
            'filename': filename,
            'size_mb': round(size, 2),
            'full_path': video_path
        }
