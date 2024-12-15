from src.file_finder import FileFinder, get_filename_notype



class Selector: 
    """
    Selector of operating with user inputs. 
    """
    def __init__(self):
        self.folder_masks = "masks"
        self.folder_videos = "videos"
        self.duration_parking = 15.
        self.is_duration_limited = 0>self.duration_parking
    
      
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
            name = get_filename_notype(video)
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
    
    
    def select_duration_parking(self)->tuple[bool, float]:
        """
        Select allowed duration of parking.

        Returns:
            tuple[bool, float]: 
                is_duration_limited (bool): True, if duration is limited. False, otherwise (free parking).
                duration_parking (float): duration of allowed parking in [sec]
        """
        print()
        print(f"Select the allowed duration of parking")
        print(f"\tNOTE: If value is below 0 -> free parking!")
        duration = input("Enter duration in [sec]: ")
        try:
            duration = float(duration)
            self.duration_parking = duration
        except:
            print("ERROR: invalid input...")
        print()
        if self.duration_parking < 0:
            self.is_duration_limited = False
            print(f"Mode: Free parking")
        if self.duration_parking >= 0:
            self.is_duration_limited = True
            print(f"Mode: Limited parking ({self.duration_parking} sec)")
        return [self.is_duration_limited, self.duration_parking]
    
    
    def _get_searchterms(self)->dict:
        """
        Get searchterm for search of matching content. 

        Returns:
            dict: searchterms {searchterm : amount of matches}
        """
        paths_masks = FileFinder.search_images_in_folder(self.folder_masks)
        search_terms = []
        remove_string = "mask_"
        for path in paths_masks:
            name = get_filename_notype(path)
            search_terms.append(name.replace(remove_string,""))
        return search_terms
    
    
    def _find_matching_mask(self, selected_id:int, searchterms:dict)->str:
        """
        Find matching mask to video.

        Args:
            selected_id (int): selected ID of video
            searchterms (dict): searchterms {searchterm : amount of matches}

        Returns:
            str: path to mask. None, otherwise.
        """
        sum = 0
        for key, val in searchterms.items():
            sum+=val
            if sum>selected_id:
                return FileFinder.search_images_in_folder(self.folder_masks, key)[0]
        return None


if __name__ == "__main__":
    """
    Test of functions
    """
    sel = Selector()
    print(sel.select_video())