import cv2

from src.parking_spot_parameters import ParkingSpot

def detection(spot:ParkingSpot, frame_dilated, min_count:int=500)->ParkingSpot: 
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