import sys
import cv2
import numpy as np
import math
from src.display_images import ImagePlotter


def enhance_contrast(img_gray):
    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) to enhance contrast
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(img_gray)


def detect_parking_lines(img, canny_img, min_length=100, max_length=600):
    # Use Hough Line Transform to detect lines in the image
    lines = cv2.HoughLinesP(canny_img, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)

    parking_lines = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # Calculate length of the line
            length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

            # Filter lines based on length
            if min_length <= length <= max_length:
                # Calculate the angle of the line
                angle = math.degrees(math.atan2(y2 - y1, x2 - x1))

                # Filter lines based on angle: horizontal (±25°) and vertical (155°-205°)
                if (-25 <= angle <= 25) or (155 <= abs(angle) <= 205):
                    parking_lines.append((x1, y1, x2, y2))

    return parking_lines


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
    img = rescale_image(img, scale_percent=65)
    ip.add_image_to_plot("input", img)

    # Convert to grayscale, enhance contrast, and apply Gaussian blur
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_contrast = enhance_contrast(img_gray)
    img_blur = cv2.GaussianBlur(img_contrast, (5, 5), 0)
    ip.add_image_to_plot("enhanced blur", img_blur)

    # Apply Canny edge detection
    low_threshold = 50
    high_threshold = 150
    img_canny = cv2.Canny(img_blur, low_threshold, high_threshold)
    ip.add_image_to_plot("canny", img_canny)

    # Detect parking lines (filter by length and angle)
    min_length = 100  # Adjust to match the desired line length range
    max_length = 600
    parking_lines = detect_parking_lines(img, img_canny, min_length, max_length)

    # Mark detected lines on the image
    for (x1, y1, x2, y2) in parking_lines:
        # Draw lines in green
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Show the image with the detected lines
    ip.add_image_to_plot("marked parking lines", img)

    # Display results
    cv2.imshow("canny", img_canny)
    cv2.imshow("marked", img)
    cv2.waitKey(0)
    ip.plot_images()
