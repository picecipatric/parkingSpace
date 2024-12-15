import cv2


from parameters_parking_spot import ParkingSpot



def detection(spot:ParkingSpot, frame_dilated:cv2.typing.MatLike, 
              min_count:int=500)->None: 
    """
    Detects status of parking spot and updates it.

    Args:
        spot (ParkingSpot): parking spot
        frame_dilated (cv2.typing.MatLike): image
        min_count (int, optional): Miniumum count, which needs to be exceeded
                                   to detect empty parking spot. Defaults to 500.
    """
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