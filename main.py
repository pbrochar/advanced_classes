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
        self.fuel_quantity = tank_size
        