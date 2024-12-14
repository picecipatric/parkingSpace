# import pickle
# from skimage.transform import resize
import numpy as np
import cv2

i = 0

def availability(space,videoDilate):
    #status = True -> Parkplatz frei
    #status = False -> Parkplatz besetzt
    
    x1, y1, w, h = space
    
    space_checked = videoDilate[y1:y1 + h, x1:x1 + w]
    count = cv2.countNonZero(space_checked)
    
    if count > 450:
        status = False
    else:
        status = True
        
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

