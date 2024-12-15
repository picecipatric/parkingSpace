import os

from src.file_util import FileTypeChecker, get_filename_notype


class FileFinder:        
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
    

if __name__ == "__main__":
    file = R"src\file_finder.py"
    name = get_filename_notype(file)
    print(name)
    list_files = FileFinder.search_files_in_folder("src", "")
    print(list_files)