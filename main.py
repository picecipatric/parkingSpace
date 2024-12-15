import cv2


import src.detection as det
from src.selector import Selector
from src.file_opener import FileOpener as fo
from src.file_finder import get_filename_notype
# from src.util import get_parking_lines, availability
from src.parking_spot_parameters import ParkingSpot, setup_parking_spots
from src.drawer_parking_spot import draw_parking_field


MIN_COUNT_DICT = {
    "DEFAULT" : 1000,
    "mask_parking_crop" : 1000,
    "mask_parking_space_1920_1080" : 450
}


if __name__ == "__main__":
    
    # Load image and video
    mask_path, video_path = Selector().select_video()
    mask_name = get_filename_notype(mask_path)
    mask = fo.open_as_mask(mask_path)
    video = fo.open_as_video(video_path)
    if not mask_name in MIN_COUNT_DICT.keys():
        mask_name = "DEFAULT"
    # video = rescale_video(video, scale_percent=80)
    
    parking_spots = setup_parking_spots(mask_image=mask)
    # connected_lines = cv2.connectedComponentsWithStats(mask, 4, cv2.CV_32S)
    # parking_lots = get_parking_lines(connected_lines)
    # status = [None for j in parking_lots]
    
    frame_number = 0
    papap = 1
    at_frame = 50
    ret = True
    while ret:
        ret,frame = video.read()
        if not ret:
            break
        # videogray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # videoblur = cv2.GaussianBlur(videogray, (3, 3),1)
        # videothresh = cv2.adaptiveThreshold(
        #     videoblur, 255,
        #     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        #     cv2.THRESH_BINARY_INV, 25, 16)
        
        # videoMedian = cv2.medianBlur(videothresh, 5)
        
        # kernel = np.ones((3,3), np.uint8)
        # videoDilate = cv2.dilate(videoMedian,kernel, iterations=1)
        # videoDilate = det.dilate_frame(frame)
        frame_dilated = det.dilate_frame(frame)
        
        if frame_number % at_frame == 0:
            for spot in parking_spots:
                det.detection(spot, frame_dilated, 
                              min_count=MIN_COUNT_DICT[mask_name])
            # for parking_lot_index, parking_lot in enumerate(parking_lots):
            #     x1, y1, w, h = parking_lot
                
            #     parking_status = availability(parking_lot,videoDilate)
                
            #     status[parking_lot_index] = parking_status
        
        for spot in parking_spots:
            draw_parking_field(spot, frame)
        # for parking_lot_index, parking_lot in enumerate(parking_lots):
        #     parking_status = status[parking_lot_index]
        #     x1, y1, w, h, = parking_lots[parking_lot_index]
            
            
        #     if parking_status:
        #         frame = cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), (0, 255, 0), 2)
        #     else:
        #         frame = cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), (0, 0, 255), 2)
        
        cv2.imshow('frame',frame)
        cv2.imshow('dilated',frame_dilated)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        
        frame_number = frame_number + 1
    
    for spot in parking_spots:
        print(spot.lable_id, 
              spot.time.time_current_parked_delta)
    
    video.release()
    cv2.destroyAllWindows()