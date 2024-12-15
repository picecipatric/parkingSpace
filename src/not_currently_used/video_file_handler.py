import pytube 
import os
import cv2
import ntpath
from file_finder import FileTypeChecker as ftc

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
        VideoPathHandler().move_all_videos_to_folder(video_folder=self.folder_path)
        return True


class VideoPathHandler: 
    def get_all_video_paths(self, video_folder:str="") -> list[str]:
        if not video_folder: 
            video_folder = os.getcwd()
        folder_items = os.listdir(video_folder)
        video_paths = []
        for ele in folder_items: 
            path = os.path.join(video_folder, ele)
            if os.path.isfile(path): 
                if ftc.is_video(path):
                    video_paths.append(path)
        return video_paths
    
    
    def move_all_videos_to_folder(self, video_folder:str="", folder_path:str="videos/"):
        paths_videos = self.get_all_video_paths(video_folder)
        if not os.path.exists(folder_path):
            print(f"ERROR: Path doesn't exist {folder_path}")
            return False
        try: 
            for old_path in paths_videos:
                file_name = ntpath.basename(old_path)
                new_path = os.path.join(folder_path, file_name)
                os.rename(old_path, new_path)
        except:
            return False
        return True

if __name__ == "__main__":
    SAVE_PATH = "videos" 
    url = "https://www.youtube.com/shorts/XJhgdVv3130"
    url = "https://www.youtube.com/watch?v=yojapmOkIfg"
    url = "https://www.youtube.com/shorts/_0svnbYgckA"

    # NOTE: YouTube can block your IP and downloads won't work
    vdown = VideoDownloader(SAVE_PATH)
    vdown.download_video(url)
