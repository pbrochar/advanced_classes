import time
from typing import Optional
from error import OutOfGazError, TooMuchFuelError


class Car:
    def __init__ (
            self,
            model: str,
            name: str,
            weight: int,
            length: int,
            height: int,
            width: int,
            maximum_speed: int,
            tank_size: int,
            average_consumption: int,
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
        self._fuel_quantity = tank_size

    def __iter__(self):
        """
        Allows to create a dictionary from the dict() function.
        """
        yield 'model', self.model
        yield 'name', self.name
        yield 'weight', self.weight
        yield 'lenght', self.length
        yield 'height', self.height
        yield 'width', self.width
        yield 'maximum_speed', self.maximum_speed
        yield 'tank_size', self.tank_size
        yield 'average_consumption', self.average_consumption
        yield 'gas', self.gas

    def __lt__(self, other: "Car") -> bool:
        return self._get_volume() < other._get_volume()
    
    def __gt__(self, other: "Car") -> bool:
        return self._get_volume() > other._get_volume()

    def __eq__(self, other: "Car") -> bool:
        return self._get_volume() == other._get_volume()

    def __ne__(self, other: "Car") -> bool:
        return self._get_volume() != other._get_volume()
    
    def _get_volume(self) -> int:
        return self.length * self.width * self.length
    
    def move_on(self, duration: Optional[int] = None) -> None:
        """
        This function allows the car to move forward.
        If the time is not specified, the car will move forward until the tank is empty.
        The specified time cannot be greater than the capacity of the car, 
        in this case it will move forward until the tank is empty and an exception OutOfGazError will be raise.
        """
        
        maximum_move_time = self.gas / self.average_consumption
        if duration is None:
            move_time = maximum_move_time
        elif duration < maximum_move_time:
            move_time = duration
        else:
            time.sleep(maximum_move_time)
            raise OutOfGazError("No Gaz")
        time.sleep(move_time)

    def put_fuel(self, quantity: Optional[int] = None) -> None:
        """
        This function allows to add a quantity of fuel in the car.
        You can't add a negative amount.
        If no amount is specified, then the tank will be filled up completely.
        """
        if quantity is None:
            self.gas = self.tank_size
        elif quantity < 0:
            raise ValueError("you can't add a negative value.")
        else:
            self.gas += quantity
        
    @property
    def gas(self) -> int:
        return self._fuel_quantity

    @gas.setter
    def gas(self, quantity: int) -> None:
        if quantity < 0:
            raise ValueError("gas can't be less than 0.")
        elif quantity > self.tank_size:
            self._fuel_quantity = self.tank_size
            raise TooMuchFuelError("fuel_quantity can\'t be greater than tank_size")
        else:
            self._fuel_quantity = quantity

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
    try:
        voiture.put_fuel(-5)
    except ValueError as e:
        print(f"Error: {e}")
    except TooMuchFuelError as e:
        print(f"Error: {e}")
    print(voiture.gas)
    print(dict(voiture))