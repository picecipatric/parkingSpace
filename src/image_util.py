import cv2
import numpy as np


def dilate_frame(frame:np.ndarray)->np.ndarray:
    """
    Dilates and returns frame.

    Args:
        frame (np.ndarray): frame as image

    Returns:
        np.ndarray: dilated frame as image
    """
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_blur = cv2.GaussianBlur(frame_gray, (3, 3),1)
    frame_thresh = cv2.adaptiveThreshold(frame_blur, 
                                         255,
                                         cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
        
    frame_median = cv2.medianBlur(frame_thresh, 5)
    kernel = np.ones((3,3), np.uint8)
    frame_dilate = cv2.dilate(frame_median, kernel, iterations=1)
    return frame_dilate

    
def rescale_image(img:np.ndarray, scale_percent:int=100)->np.ndarray:
    """
    Rescales input image

    Args:
        img (np.ndarray): _description_
        scale_percent (int, optional): Scale of image in percetage. Defaults to 100 %.

    Returns:
        np.ndarray: rescaled image
    """
    # Calculate new dimensions
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dimensions = (width, height)
    return cv2.resize(img, dimensions, interpolation=cv2.INTER_AREA)