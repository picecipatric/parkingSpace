import time


class ParkingTime:
    """
    State and times of a parking spot
    """
    def __init__(self):
        self.time_delta = 0.0
        self.datetimes_parked_started = []
        self.datetimes_parked_ended = []
        self.is_parked = False
    
    
    def update_parking_spot(self, is_empty:bool) -> None:
        """
        Update ParkingTime parameters and status

        Args:
            is_empty (bool): Status of parking spot
        """
        # vehicle left
        if is_empty:
            if self.is_parked:
                self._update_vehicle_left()
        # vehicle arrived
        if not is_empty:
            if not self.is_parked:
                self._update_vehicle_arrived()
        # vehicle parked
        self._update_vehicle_parked()
    
    
    def get_current_parked_time(self)->float:
        """
        Get curret parked time of parking spot.

        Returns:
            float: curret parked time of parking spot
        """
        self._update_vehicle_parked()
        return self.time_delta
    
    
    def get_datetimes_parked_started(self)->list[float]:
        """
        Get all starting datetimes of parking spot.

        Returns:
            list[float]: list of all start datetimes
        """
        return self.datetimes_parked_started
    
    
    def get_datetimes_parked_ended(self)->list[float]:
        """
        Get all ending datetimes of parking spot.

        Returns:
            list[float]: list of all start datetimes
        """
        return self.datetimes_parked_ended
    
    
    def _update_vehicle_arrived(self)->None:
        """
        Update parameters, if a vehicle arrived.
        """
        self.datetimes_parked_started.append(time.time())
        self.is_parked = True
    
    
    def _update_vehicle_left(self)-> None:
        """
        Update parameters, if a vehicle left.
        """
        self.datetimes_parked_ended.append(time.time())
        delta_time = self.datetimes_parked_started[-1] - self.datetimes_parked_ended[-1]
        # self.times_parked_delta.append(delta_time)
        self.time_delta = 0.0
        self.is_parked = False
    
    
    def _update_vehicle_parked(self):
        """
        Update parameters, if a vehicle is parked.
        """
        if not self.is_parked:
            return
        self.time_delta = time.time() - self.datetimes_parked_started[-1]



if __name__ == "__main__":
    """
    Testing code
    """
    spots_time = 3*[None]
    for id, spot in enumerate(spots_time):
        spots_time[id] = ParkingTime()
        
    for spot in spots_time:
        for i in range(0, 3):
            if i%2 == 0:
                spot.update_parking_spot(is_empty=False)
            if i%2 == 1:
                spot.update_parking_spot(is_empty=True)
            spot.get_current_parked_time()
        time.sleep(1)
    for spot in spots_time:
        print(
            spot.get_datetimes_parked_started(),
            spot.get_datetimes_parked_ended())