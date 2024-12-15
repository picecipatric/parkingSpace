import cv2
from src.parking_spot_parameters import ParkingSpot


def draw_parking_field(spot:ParkingSpot, frame:cv2.typing.MatLike):
    x1 = spot.geo.coord_x
    y1 = spot.geo.coord_y
    w = spot.geo.width
    h = spot.geo.height

    if spot.time.is_parked:
        frame = cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), (0, 0, 255), 2)
    else:
        frame = cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), (0, 255, 0), 2)