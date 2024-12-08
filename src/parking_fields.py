import cv2
import numpy as np

punkte = []
current_img = None

def sort_points():

    min_x = min(k[0] for k in punkte)
    min_y = min(k[1] for k in punkte)

    new_point = (min_x, min_y)

    print("Neue Koordinate:", new_point)
    
    return new_point



def paint_parkinglot(event, x, y, flags, param):
    global punkte, current_img
    
    img = param
    if event == cv2.EVENT_LBUTTONDOWN:
        punkte.append((x, y))
        print(f"Punkt hinzugefügt: {x}, {y}")
        
        cv2.circle(img, (x, y), 1, (0, 0, 255), -1)
        cv2.imshow("Parkplatz", img)
        
        if len(punkte) == 4:
            zuschneiden(img)
            
            
def zuschneiden(img):
    global punkte, current_img

    maske = np.zeros(img.shape[:2], dtype=np.uint8)
    punkte_array = np.array(punkte, dtype=np.int32)
    cv2.fillPoly(maske, [punkte_array], 255)

    ausgeschnitten = cv2.bitwise_and(img, img, mask=maske)
    x, y, w, h = cv2.boundingRect(punkte_array)
    ausgeschnittener_bereich = ausgeschnitten[y:y+h, x:x+w]

    cv2.imshow("Ausgeschnittener Bereich", ausgeschnittener_bereich)

    paint_parking_lot(ausgeschnittener_bereich, img)
    
    
    
def paint_parking_lot(Parkplätze, img):

    
    hsv = cv2.cvtColor(Parkplätze, cv2.COLOR_BGR2HSV)
    untergrenze = np.array([0, 0, 200])
    obergrenze = np.array([180, 30, 255])
    maske_farbe = cv2.inRange(hsv, untergrenze, obergrenze)
    
    graubild = cv2.cvtColor(Parkplätze, cv2.COLOR_BGR2GRAY)
    cv2.imshow("graubild1", graubild)
    cv2.waitKey(0)
    
    
    maske_thresh = cv2.adaptiveThreshold(
        graubild, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )
       

    maske = cv2.bitwise_and(maske_farbe, maske_thresh)
    cv2.imshow("maske", maske)
    cv2.waitKey(0)

    kernel_width = max(10, Parkplätze.shape[1] // 50)  
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_width, 1))
    
    Line = cv2.morphologyEx(maske, cv2.MORPH_OPEN, kernel)
    cv2.imshow("Linien", Line)
    cv2.waitKey(0)
    
    konturen, _ = cv2.findContours(Line, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    offset = sort_points()
    x_offset = offset[0] 
    y_offset = offset[1]
    
    punkte.clear()
    
    for kontur in konturen:
        x, y, w, h = cv2.boundingRect(kontur)  
        cv2.line(img, (x + x_offset, y + y_offset), (x + w + x_offset, y + h + y_offset), (0, 0, 255), 2)
        
    
    cv2.imshow("final", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()