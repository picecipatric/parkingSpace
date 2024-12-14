import os
import ntpath
import cv2
import numpy as np

class FileFinder:    
    def get_filename_notype(file_path:str)->str:
        """
        Return name of file without the type/ending.

        Args:
            file_path (str): path of file

        Returns:
            str: file name
        """
        basename = ntpath.basename(file_path)
        reversed_basename = basename[::-1]
        _, reversed_filename = reversed_basename.split('.', 1)
        filename = reversed_filename[::-1]
        return filename
    
    def search_files_in_folder(folder_path:str, searchterm:str="")->list[str]:
        """
        Searches for files containing searchterm.
        If no searchterm is given, it returns all file paths
        
        Args:
            folder_path (str): path of folder with files
            searchterm (str): searchterm

        Returns:
            list[str]: sorted list (by length) of matching file paths
        """
        folder_items = os.listdir(folder_path)
        found_file_paths = []
        for item in folder_items:
            if searchterm in item:
                path = os.path.join(folder_path, item)
                found_file_paths.append(path)
                if not os.path.isfile(found_file_paths[-1]):
                    found_file_paths.pop()
        if not found_file_paths:
            print(f"ERROR: No matching file found with: \"{searchterm}\"")
            return []
        found_file_paths.sort(key=len)
        return found_file_paths
        
    def search_images_in_folder(folder_path:str, searchterm:str="")->list[str]:
        paths = FileFinder.search_files_in_folder(folder_path, searchterm)
        found_image_paths = []
        for path in paths:
            if FileTypeChecker.is_image(path):
                found_image_paths.append(path)
        return found_image_paths
    
    def search_videos_in_folder(folder_path:str, searchterm:str="")->list[str]:
        paths = FileFinder.search_files_in_folder(folder_path, searchterm)
        found_video_paths = []
        for path in paths:
            if FileTypeChecker.is_video(path):
                found_video_paths.append(path)
        return found_video_paths
    
class FileTypeChecker: 
    def is_image(file_path:str)->bool:
        """Check, if file is a image for openCV

        Args:
            file_path (str): path of file

        Returns:
            bool: True, if it is video. False, otherwise.
        """
        try: 
            image = cv2.imread(file_path)
            if type(image) == np.ndarray:
                del image
                return True
        except:
            return False
    
    
    def is_video(file_path:str) -> bool:
        """Check if file is a video for openCV

        Args:
            file_path (str): path of file

        Returns:
            bool: True, if it is video. False, otherwise.
        """
        try: 
            cap = cv2.VideoCapture(file_path)
            if cap.isOpened():
                cap.release()
                return True
        except:
            return False
        
        
if __name__ == "__main__":
    file = R"F:\.DEV\_Programming\_GitHub\BIDV2_ParkingSpaceDetection\parkingSpace\tests\test_videostream.py"
    mf = FileFinder
    name = mf.get_filename_notype(file)
    list_files = mf.search_files_in_folder("src", "")
    print(list_files)