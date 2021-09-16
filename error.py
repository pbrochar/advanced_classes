class CarError(Exception):
    pass

class OutOfGazError(CarError):
    pass

class TooMuchFuelError(CarError):
    pass