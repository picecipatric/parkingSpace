import cv2
import numpy as np

punkte = []

def sort_points():
    punkte.sort(key=lambda punkt: abs(punkt[0]) + abs(punkt[1]))
    return punkte[0]


def paint_parkinglot(event, x, y, flags, param):
    
    img = param
    if event == cv2.EVENT_LBUTTONDOWN:
        punkte.append((x, y))
        print(f"Punkt hinzugefügt: {x}, {y}")
        
        cv2.circle(img, (x, y), 1, (0, 0, 255), -1)
        cv2.imshow("Parkplatz", img)
        
        if len(punkte) == 4:
            zuschneiden(img)
            
def zuschneiden(img):

    maske = np.zeros(img.shape[:2], dtype=np.uint8)
    
    punkte_array = np.array(punkte, dtype=np.int32)
    cv2.fillPoly(maske, [punkte_array], 255)

    ausgeschnitten = cv2.bitwise_and(img, img, mask=maske)
    x, y, w, h = cv2.boundingRect(punkte_array)
    
    ausgeschnittener_bereich = ausgeschnitten[y:y+h, x:x+w]

    cv2.imshow("Ausgeschnittener Bereich", ausgeschnittener_bereich)
    cv2.imwrite("ausgeschnittener_bereich.jpg", ausgeschnittener_bereich)

    paint_parking_lot(ausgeschnittener_bereich, img)
    
def paint_parking_lot(Parkplätze, img):
    """
    Findet weisse horizontale Linien, die von links nach rechts verlaufen und mindestens so breit sind wie das Bild.
    """
    graubild = cv2.cvtColor(Parkplätze, cv2.COLOR_BGR2GRAY)
    cv2.imshow("graubild", graubild)
    cv2.waitKey(0)
    
    _, maske = cv2.threshold(graubild, 200, 255, cv2.THRESH_BINARY)
    cv2.imshow(f"maske", maske)
    cv2.waitKey(0)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (Parkplätze.shape[1] // 2, 1))
    horizontale_linie = cv2.morphologyEx(maske, cv2.MORPH_OPEN, kernel)
    cv2.imshow("horizontale_linie", horizontale_linie)
    cv2.waitKey(0)
    
    konturen, _ = cv2.findContours(horizontale_linie, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    offset = sort_points()
    x_offset = offset[0]
    y_offset = offset[1]

    
    for kontur in konturen:
        x, y, w, h = cv2.boundingRect(kontur)  
        cv2.line(img, (x + x_offset, y + y_offset), (x + w + x_offset, y + h + y_offset), (0, 0, 255), 2)
        
        # if w >= img.shape[1] - 10:
            
        #     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        #     print(f"Weiße horizontale Linie gefunden: x={x}, y={y}, Breite={w}, Höhe={h}") 
    
    
    cv2.imshow("final", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()