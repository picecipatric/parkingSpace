import cv2

from src.parking_time_measurement import ParkingTime
from src.parking_spot_parameters import ParkingSpotParameters

class ParkingTimeDisplay:
    def __init__(self, image:cv2.typing.MatLike, parameters:ParkingSpotParameters) -> None:
        parameters.lable_id
        self.image = image
        # self.coord_x = spot[1]
        # self.coord_y = spot[2]
        # self.spot_width = spot[3]
        # self.spot_height = spot[4]
        
        
    def update_time_display(self, parameters:ParkingSpotParameters) -> None: 
        coord_x = parameters.spot_coord_x
        coord_y = parameters.spot_coord_y
        spot_width = parameters.spot_width
        spot_height = parameters.spot_height
        origin = (coord_y, coord_x)
        
        time = parameters.time_delta_parked
        time = str(time)
        color = (0,0,0)
        cv2.putText(self.image, time, origin, cv2.FONT_HERSHEY_PLAIN, 1, color, 1, cv2.LINE_AA)