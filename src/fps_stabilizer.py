import time

class FpsStabilizer:
    """
    Stablizes fps of a video
    """
    def __init__(self, FPS:float)->None:
        self.fps = 30.0
        self.wait_delay = 1/self.fps
        self.old_timestamp = time.time()
        
        if type(FPS) is float or type(FPS) is int:
            if FPS > 0:
                self.fps = FPS
                self.wait_delay = 1./self.fps
    
    def setup_stable_fps(self)->None:
        """
        Sets up fps stabilizer.
        """
        self.old_timestamp = time.perf_counter()         
    
    def ensure_stable_fps(self)->None:
        """
        Tries to ensure stable fps.
        """
        while(time.perf_counter() - self.old_timestamp) <= self.wait_delay:
            None
        self.old_timestamp = time.perf_counter()