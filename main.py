import time
import sys
from typing import Optional

class OutOfGazError(Exception):
    pass


class Car:
    def __init__ (self,
                  model: str,
                  name: str,
                  weight: int,
                  length: int,
                  height: int,
                  width: int,
                  maximum_speed: int,
                  tank_size: int,
                  average_consumption: int
                  ):
        self.model = model
        self.name = name
        self.weight = weight
        self.length = length
        self.height = height
        self.width = width
        self.maximum_speed = maximum_speed
        self.tank_size = tank_size
        self.average_consumption = average_consumption
        if self.average_consumption <= 0:
            raise ValueError('average_consumption can\'t be less than or equal to 0.')
        self.fuel_quantity = tank_size
    
    def __lt__(self, other: "Car") -> bool:
        car_volume = self.length * self.width * self.length
        other_car_volume = other.length * other.width * other.width
        return car_volume < other_car_volume
    
    def __gt__(self, other: "Car") -> bool:
        car_volume = self.length * self.width * self.length
        other_car_volume = other.length * other.width * other.width
        return car_volume > other_car_volume

    def __eq__(self, other: "Car") -> bool:
        car_volume = self.length * self.width * self.length
        other_car_volume = other.length * other.width * other.width
        return car_volume == other_car_volume
    
    def __ne__(self, other: "Car") -> bool:
        car_volume = self.length * self.width * self.length
        other_car_volume = other.length * other.width * other.width
        return car_volume != other_car_volume
    
    def move_on(self, duration: Optional[int] = None) -> None:
        maximum_move_time = self.fuel_quantity / self.average_consumption
        if duration is None:
            move_time = maximum_move_time
        elif duration < maximum_move_time:
            move_time = duration
        else:
            time.sleep(maximum_move_time)
            raise OutOfGazError("No Gaz")
        time.sleep(move_time)

 
if __name__ == "__main__":
    #try:
    tuture = Car("Clio", "tuture", 10, 10, 10, 10, 100, 100, 10)
    # except ValueError as e:
    #     print(f"Error: {e}")
    #     sys.exit(0)
    # try:
    #     tuture.move_on(5)
    # except OutOfGazError as e:
    #     print(f"Error: {e}")
    voiture = Car("Multipla", "MoiMocheEtMechant", 15, 20, 20, 20, 100, 100, 10)
    print(tuture < voiture)
    print(voiture > tuture)
    print(tuture == voiture)
    print(voiture != tuture)