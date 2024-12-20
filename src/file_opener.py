import cv2

from src.file_finder import FileTypeChecker as ftc

class FileOpener:
    def open_as_grayscale(file_path:str)->cv2.typing.MatLike:
        """open image as mask

        Args:
            file_path (str): path of image file

        Returns:
            cv2.typing.MatLike: openCV image as grayscale
        """
        if not ftc.is_image(file_path):
            return None
        gray = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE) 
        return gray
    
    
    def open_as_mask(file_path:str)->cv2.typing.MatLike:
        """
        Opens an image path as mask.

        Args:
            file_path (str): path of mask

        Returns:
            cv2.typing.MatLike: openCV image as mask
        """
        return FileOpener.open_as_grayscale(file_path)
    
    
    def open_as_video(file_path:str)->cv2.VideoCapture:
        """
        Opens an video path as VideoCapture.

        Args:
            file_path (str): path to video

        Returns:
            cv2.VideoCapture: capture of video
        """
        if not ftc.is_video(file_path):
            return None
        capture = cv2.VideoCapture(file_path)
        return capture