import cv2
import numpy as np
from src.util import get_parking_lines, availability


if __name__ == "__main__":
    
    # Load image

    #
    
    mask = "./images/mask.png"
    video_path = "./images/parking_video.mp4"
    
    mask = cv2.imread(mask, 0)
    
    video = cv2.VideoCapture(video_path)
    ##video = rescale_video(video, scale_percent=80)
    
    connected_lines = cv2.connectedComponentsWithStats(mask, 4, cv2.CV_32S)
    
    parking_lots = get_parking_lines(connected_lines)
    
    status = [None for j in parking_lots]
    
    frame_number = 0
    papap = 1
    at_frame = 50
    ret = True
    while ret:
        ret,frame = video.read()
        videogray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        videoblur = cv2.GaussianBlur(videogray, (3, 3),1)
        videothresh = cv2.adaptiveThreshold(
            videoblur, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 25, 16)
        
        videoMedian = cv2.medianBlur(videothresh, 5)
        
        kernel = np.ones((3,3), np.uint8)
        videoDilate = cv2.dilate(videoMedian,kernel, iterations=1)
        
        
        if frame_number % at_frame == 0:
            for parking_lot_index, parking_lot in enumerate(parking_lots):
                x1, y1, w, h = parking_lot
                
                parking_status = availability(parking_lot,videoDilate)
                
                status[parking_lot_index] = parking_status
        
        for parking_lot_index, parking_lot in enumerate(parking_lots):
            parking_status = status[parking_lot_index]
            x1, y1, w, h, = parking_lots[parking_lot_index]
            
            
            if parking_status:
                frame = cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), (0, 255, 0), 2)
            else:
                frame = cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), (0, 0, 255), 2)
        
        cv2.imshow('frame',frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        
        frame_number = frame_number + 1
    
    video.release
    cv2.destroyAllWindows()