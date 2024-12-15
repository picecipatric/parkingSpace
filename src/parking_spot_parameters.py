from dataclasses import dataclass
from src.parking_time_measurement import ParkingTime
@dataclass
class ParkingSpot:
    def __init__(self, 
                 lable_id:int,
                 coord_x:int,
                 coord_y:int, 
                 width:int, 
                 height:int):
        self.lable_id = lable_id
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.width = width
        self.height = height
    
        self.is_parked = False
        self.time = ParkingTime()
        
        self.origin_text:tuple[int, int]= (int(self.coord_x+self.width/2), 
                                           int(self.coord_y+self.height/2))