import cv2
from src.parking_spot_parameters import ParkingSpot


def draw_parking_field(spot:ParkingSpot, frame:cv2.typing.MatLike):
    x1 = spot.geo.coord_x
    y1 = spot.geo.coord_y
    w = spot.geo.width
    h = spot.geo.height
    
    color = (0, 255, 0) # GREEN
    if spot.time.is_parked:
        color = (0, 0, 255) # RED
    frame = cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), color, 2)
    frame = cv2.putText(frame, str(spot.lable_id), spot.geo.origin_text, 
                        cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, color=color, thickness=2)