import sys
import cv2
import numpy as np
import csv
import math

from src.display_images import ImagePlotter



if __name__ == "__main__": 
    ip = ImagePlotter()
    # url = "jenfjnw.oei"
    filename = R"images/parkingLot.jpeg"

    # Input image
    try: 
        img = cv2.imread(filename, cv2.IMREAD_COLOR)
    except: 
        print("Error: Could not read image file", filename)
        sys.exit()
    ip.add_image_to_plot("input", img)
    
    # grayscale image
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ip.add_image_to_plot("grayscale", img_gray)
    
    # blur image
    img_blur = cv2.GaussianBlur(img_gray, (5,5), cv2.BORDER_DEFAULT)
    ip.add_image_to_plot("blur", img_blur)
    
    # canny edge detection
    low_threshold = 15
    ratio = 3
    kernel_size = 5
    detected_edges = cv2.Canny(img_blur, low_threshold, low_threshold*ratio, kernel_size)
    mask = detected_edges != 0
    img_canny = img_gray * (mask[:].astype(img.dtype))
    ip.add_image_to_plot("canny", img_canny)
    
    # plot/display the images
    ip.plot_images()
    




