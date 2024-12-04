import sys
import cv2
import numpy as np
import math
from src.display_images import ImagePlotter
from src.parking_fields import *


def rescale_image(img, scale_percent):
    # Calculate new dimensions
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dimensions = (width, height)
    return cv2.resize(img, dimensions, interpolation=cv2.INTER_AREA)


if __name__ == "__main__":
    ip = ImagePlotter()
    filename = R"images/parkingLot.jpeg"

    # Load image
    try:
        img = cv2.imread(filename, cv2.IMREAD_COLOR)
    except:
        print("Error: Could not read image file", filename)
        sys.exit()
    img = rescale_image(img, scale_percent=40)
   
   
    cv2.imshow("Parkplatz", img)
    cv2.setMouseCallback("Parkplatz", paint_parkinglot, param=img)
    
    cv2.waitKey(0)
   
