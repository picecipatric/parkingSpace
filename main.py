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
   

    current_img = img.copy()

    while True:
        
        punkte.clear()
        temp_img = current_img.copy()
        
        cv2.imshow("Parkplatz", temp_img)
        cv2.setMouseCallback("Parkplatz", paint_parkinglot, param=temp_img)

        key = cv2.waitKey(0) & 0xFF
        if key == ord('q'):
            break

        if len(punkte) == 4:
            zuschneiden(temp_img)

        current_img = temp_img

    cv2.destroyAllWindows()