import sys
import cv2
import numpy as np
import csv
import math


# url = "jenfjnw.oei"
filename = "images/parkingLot.jpeg"

# Bild einlesen mit Farben
img = cv2.imread(filename, cv2.IMREAD_COLOR)

# Überprüfen, ob das Bild erfolgreich eingelesen wurde
if img is None:
    print("Error: Could not read image file", filename)
    sys.exit(1)

cv2.imshow("Image", img)



cv2.waitKey(0)