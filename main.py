import cv2
import sys



import src.detection as det
from src.selector import Selector
from src.file_opener import FileOpener as fo
from src.file_finder import get_filename_notype
from src.parameters_parking_spot import setup_parking_spots
import src.drawer_parking_spot as draw
from src.image_util import rescale_image, dilate_frame
from src.fps_stabilizer import FpsStabilizer


FPS = 30

RESIZE_SCALE = {
    "DEFAULT" : 100,
    "mask_parking_crop" : 100,
    "mask_parking_space_1920_1080" : 75
}
MIN_COUNT_DICT = {
    "DEFAULT" : 500,
    "mask_parking_crop" : 1200,
    "mask_parking_space_1920_1080" : 450
}

def main():
    # select
    sel = Selector()
    mask_path, video_path = sel.select_video()
    if mask_path == None:
        sys.exit()
    is_duration_limited, duration_parking = sel.select_duration_parking()
    
    # Load image and video
    mask = fo.open_as_mask(mask_path)
    video = fo.open_as_video(video_path)
    
    mask_name = get_filename_notype(mask_path)
    if not mask_name in MIN_COUNT_DICT.keys():
        mask_name = "DEFAULT"
    
    frame_number = 0
    at_frame = FPS 
    ret = True
    
    # Setup parking pots and detection
    parking_spots = setup_parking_spots(mask_image=mask)
    
    # Setup video stablizer
    vid_stabeilizer = FpsStabilizer(FPS)
    vid_stabeilizer.setup_stable_fps()
    
    while ret:
        vid_stabeilizer.ensure_stable_fps()
       
        ret,frame = video.read()
        if not ret:
            break
        frame_dilated = dilate_frame(frame)
        
        if frame_number % at_frame == 0:
            is_new_overlay = False
            for spot in parking_spots:
                det.detection(spot, frame_dilated, 
                              min_count=MIN_COUNT_DICT[mask_name])
        
        is_new_overlay = False
        for spot in parking_spots:
            if is_duration_limited and spot.time.time_delta > duration_parking:
                if not is_new_overlay: 
                    overlay = frame.copy()
                    is_new_overlay = True
                draw.draw_overdue(spot, overlay)
        if is_new_overlay:
            draw.display_overdue_overlay(overlay, frame)
        
        for spot in parking_spots:
            draw.draw_parking_spot(spot, frame)
            

        # cv2.imshow('dilated', rescale_image(frame_dilated,
        #                                     RESIZE_SCALE[mask_name]))
        cv2.imshow('frame (orange: overdue)', rescale_image(frame,
                                          RESIZE_SCALE[mask_name]))
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        frame_number = frame_number + 1
        
    
    print(f"\n\n")
    print("Current parked duration in seconds: ")
    for spot in parking_spots:
        print(spot.lable_id, 
              spot.time.time_delta)
    
    video.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()