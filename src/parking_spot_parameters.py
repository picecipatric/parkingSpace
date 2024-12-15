from dataclasses import dataclass
from numpy import ndarray
import cv2

from src.time_measurement import ParkingTime
from src.util import get_parking_lines


@dataclass
class ParkingSpot:
    def __init__(self, 
                 lable_id:int,
                 coord_x:int,
                 coord_y:int, 
                 width:int, 
                 height:int):
        self.lable_id = lable_id
        
        self.geo = ParkingGeometry(coord_x=coord_x,
                                   coord_y = coord_y,
                                   width = width,
                                   height = height)
        self.time = ParkingTime()
        
        
        

@dataclass
class ParkingGeometry:
    def __init__(self, 
                 coord_x:int,
                 coord_y:int, 
                 width:int, 
                 height:int):
        
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.width = width
        self.height = height
        self.origin_text:tuple[int, int]= (int(self.coord_x+5), 
                                           int(self.coord_y+self.height-5))

        
def setup_parking_spots(mask_image:ndarray)->list[ParkingSpot]:
    connected_lines = cv2.connectedComponentsWithStats(mask_image, 4, cv2.CV_32S)
    parking_spots_geometric = get_parking_lines(connected_lines)
    parking_spots = []
    for i, spot_geo in enumerate(parking_spots_geometric):
        x1, y1, w, h = spot_geo
        spot = ParkingSpot(lable_id=i+1,
                           coord_x=x1,
                           coord_y=y1,
                           width=w,
                           height=h)
        parking_spots.append(spot)
    return parking_spots

