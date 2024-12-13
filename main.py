import cv2
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
    
    #print(parking_lots[0])
    frame_number = 0
    at_frame = 50
    ret = True
    while ret:
        ret,frame = video.read()
        
        if frame_number % at_frame == 0:
            for parking_lot_index, parking_lot in enumerate(parking_lots):
                x1, y1, w, h, = parking_lot

                parking_lot_check = frame[y1:y1 + h, x1:x1 + w, :]

                parking_status = availability(parking_lot_check)
                
                status[parking_lot_index] = parking_status
        
        for parking_lot_index, parking_lot in enumerate(parking_lots):
            parking_status = status[parking_lot_index]
            x1, y1, w, h, = parking_lots[parking_lot_index]
            
            if parking_status:
                frame = cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), (0, 0, 255), 2)
            else:
                frame = cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), (0, 255, 0), 2)
        
        cv2.imshow('frame',frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        
        frame_number = frame_number + 1
    
    video.release
    cv2.destroyAllWindows()