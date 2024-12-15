import cv2
import numpy as np
import ntpath


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