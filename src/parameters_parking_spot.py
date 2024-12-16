import cv2
from numpy import ndarray
from dataclasses import dataclass


from src.time_measurement_parking_spot import ParkingTime
from src.geometry_parking_spot import get_parking_spot_geometry, ParkingGeometry



@dataclass
class ParkingSpot:
    """
    Stores ID, geometry and times of a parking spot.
    """
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

        
def setup_parking_spots(mask_image:ndarray)->list[ParkingSpot]:
    """
    Creates parking spots from a mask.

    Args:
        mask_image (ndarray): mask as image

    Returns:
        list[ParkingSpot]: list of parking spots
    """
    connected_lines = cv2.connectedComponentsWithStats(mask_image, 4, cv2.CV_32S)
    parking_spots_geometric = get_parking_spot_geometry(connected_lines)
    
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

