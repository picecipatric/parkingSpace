from src.file_finder import FileFinder


class Selector: 
    def __init__(self):
        self.folder_masks = "masks"
        self.folder_videos = "videos"
        
    def select_video(self)->list[str, str]:
        """
        Selects video with matching mask

        Returns:
            list[str, str]: path of mask [0] and video [1]. None, otherwise.
        """
        searchterms_keys = self._get_searchterms()
        searchterms_counts = len(searchterms_keys) * [0]
        searchterms = dict(zip(searchterms_keys, searchterms_counts))
        paths_videos = []
        for term in searchterms.keys():
            paths = FileFinder.search_videos_in_folder(self.folder_videos, 
                                                       searchterm=term)
            searchterms[term] = len(paths)
            paths_videos += paths
        print()
        if not paths_videos:
            print("No matching video found...")
            return None
       
        print(f"Select one of the following videos with a number:")
        for i, video in enumerate(paths_videos):
            name = FileFinder.get_filename_notype(video)
            print(f"\t{i}.) {name}")
        selected_id = input("Enter video number: ")
        try: 
            selected_id = int(selected_id)
            if selected_id < 0:
                raise
            if selected_id >= len(paths_videos):
                raise
        except:
            print("ERROR: invalid input...")
            return None
        
        mask_path = self._find_matching_mask(selected_id, searchterms)
        video_path = paths_videos[selected_id]
        return [mask_path, video_path]
        
        
    def _get_searchterms(self):
        paths_masks = FileFinder.search_images_in_folder(self.folder_masks)
        search_terms = []
        remove_string = "mask_"
        for path in paths_masks:
            name = FileFinder.get_filename_notype(path)
            search_terms.append(name.replace(remove_string,""))
        return search_terms
    
    def _find_matching_mask(self, selected_id:int, searchterms:dict)->str:
        sum = 0
        for key, val in searchterms.items():
            sum+=val
            if sum>selected_id:
                return FileFinder.search_images_in_folder(self.folder_masks, key)[0]
        return None
if __name__ == "__main__":
    sel = Selector()
    print(sel.select_video())