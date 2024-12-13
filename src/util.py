import pickle
from skimage.transform import resize
import numpy as np
import cv2

i = 0

def availability(space, i=0 ):
    #status = True -> Parkplatz frei
    #status = False -> Parkplatz besetzt
    
    i = 0
    
    if i == 0:
        i = 1
        status = True
    else:
        i = 0
        status = False
        
    return status


def get_parking_lines(connected_components):
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

