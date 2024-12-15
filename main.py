import cv2


import src.detection as det
from src.selector import Selector
from src.file_opener import FileOpener as fo
from src.file_finder import get_filename_notype
from src.parking_spot_parameters import setup_parking_spots
import src.drawer_parking_spot as draw
from src.image_util import rescale_image, dilate_frame


MIN_COUNT_DICT = {
    "DEFAULT" : 500,
    "mask_parking_crop" : 1200,
    "mask_parking_space_1920_1080" : 450
}
RESIZE_SCALE = {
    "DEFAULT" : 100,
    "mask_parking_crop" : 100,
    "mask_parking_space_1920_1080" : 50
}


if __name__ == "__main__":
    
    # select
    sel = Selector()
    mask_path, video_path = sel.select_video()
    is_duration_limited, duration_parking = sel.select_duration_parking()
    
    # Load image and video
    mask_name = get_filename_notype(mask_path)
    mask = fo.open_as_mask(mask_path)
    video = fo.open_as_video(video_path)
    if not mask_name in MIN_COUNT_DICT.keys():
        mask_name = "DEFAULT"
    
    parking_spots = setup_parking_spots(mask_image=mask)
    
    frame_number = 0
    papap = 1
    at_frame = 30
    ret = True
    while ret:
        ret,frame = video.read()
        if not ret:
            break
        frame_dilated = dilate_frame(frame)
        
        if frame_number % at_frame == 0:
            for spot in parking_spots:
                det.detection(spot, frame_dilated, 
                              min_count=MIN_COUNT_DICT[mask_name])
        
        for spot in parking_spots:
            if is_duration_limited and spot.time.time_delta > duration_parking:
                draw.draw_overdue(spot, frame)
            draw.draw_parking_field(spot, frame)
            

        cv2.imshow('dilated', rescale_image(frame_dilated,
                                            RESIZE_SCALE[mask_name]))
        cv2.imshow('frame (orange: overdue)', rescale_image(frame,
                                          RESIZE_SCALE[mask_name]))
        
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        
        frame_number = frame_number + 1
    
    print(f"\n\n")
    print("Current parked duration in seconds: ")
    for spot in parking_spots:
        print(spot.lable_id, 
              spot.time.time_delta)
    
    video.release()
    cv2.destroyAllWindows()