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

def draw_overdue(spot:ParkingSpot, frame:cv2.typing.MatLike):
    x1 = spot.geo.coord_x
    y1 = spot.geo.coord_y
    w = spot.geo.width
    h = spot.geo.height
    
    overlay = frame.copy()
    color = (0, 124, 255)
    alpha = 0.50 #transparency
    overdue = cv2.rectangle(overlay, (x1, y1), (x1 + w, y1 + h), color, -1)
    cv2.addWeighted(overdue, alpha, frame, 1 - alpha, 0, frame)
    