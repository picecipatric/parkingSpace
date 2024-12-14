import pytube 
import os

class VideoDownloader:
    def __init__(self, folder_path:str):
        self.folder_path = folder_path
    
    def set_folder_path(self, new_folder_path:str) -> bool:
        if not os.path.exists(new_folder_path):
            print("ERROR: Path invalid")
            return False
        self.folder_path = new_folder_path
        return True
    
    def download_video(self, url:str) -> bool: 
        command = "pytube " + url
        try: 
            os.system(command)
        except: 
            print("ERROR: Cannot download video!")
            return False
        VideoPathHandler().move_all_videos_to_folder(self.folder_path)
        return True


class VideoPathHandler: 
    def __init__(self):
        valid_types = [".mp3", ".mp4"]
    
    def get_all_videos(self) -> list[str]:
        path_abs_dir = os.getcwd()
        path_videos = []
        for file in os.listdir(path_abs_dir):
            file_path = os.join(path_abs_dir, file)
            if os.isfile(file_path):
                if self.check_videotype():
                    path_videos.append(file_path)
        return path_videos
    
    def check_videotype(self, file_path:str) -> bool:
        for type in self.valid_types:
            if file_path.lower().endswith(type):
                return True
        return False
    
    def move_all_videos_to_folder(self, folder_path:str):
        path_videos = self.get_all_videos()

