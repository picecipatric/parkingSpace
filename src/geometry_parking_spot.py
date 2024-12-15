import cv2


from dataclasses import dataclass



def get_parking_spot_geometry(connected_components:list)->list[list]:
    """
    Get geometry of parking spot

    Args:
        connected_components (list): parameters of mask

    Returns:
        list[list]: list of parking spot geometry
    """
    (totalLabels, label_ids, values, centroid) = connected_components

    slots = []
    coef = 1
    for i in range(1, totalLabels):

        # Now extract the coordinate points
        x1 = int(values[i, cv2.CC_STAT_LEFT] * coef)
        y1 = int(values[i, cv2.CC_STAT_TOP] * coef)
        w = int(values[i, cv2.CC_STAT_WIDTH] * coef)
        h = int(values[i, cv2.CC_STAT_HEIGHT] * coef)

        slots.append([x1, y1, w, h])
    return slots


@dataclass
class ParkingGeometry:
    """
    Stores geometry of a parking spot.
    """
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