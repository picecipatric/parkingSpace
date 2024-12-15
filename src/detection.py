import cv2
import numpy as np

from src.parking_spot_parameters import ParkingSpot

def dilate_frame(frame:np.ndarray):
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

def detection(spot:ParkingSpot, frame_dilated, min_count:int=450)->ParkingSpot: 
    x1 = spot.geo.coord_x
    y1 = spot.geo.coord_y
    w = spot.geo.width
    h = spot.geo.height
    
    space_checked = frame_dilated[y1:y1 + h, x1:x1 + w]
    count = cv2.countNonZero(space_checked)
    
    if count > min_count:
        spot.time.update_parking_spot(is_empty=False)
    else:
        spot.time.update_parking_spot(is_empty=True)