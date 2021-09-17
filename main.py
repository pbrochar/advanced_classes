import time
import asyncio
from error import OutOfGazError, TooMuchFuelError
from race import Race
from car import Car


if __name__ == "__main__":
    tuture = Car("Renault", "Max", 10, 10, 10, 10, 200, 150, 10)
    toto = Car("Tesla", "Paul", 10, 10, 10, 10, 210, 150, 12)
    carglass = Car("BMW", "Leo", 10, 10, 10, 10, 200, 162, 14)
    titi = Car("Peugeot", "Dede", 10, 10, 10, 10, 200, 150, 10)
    niglo = Car("2ch", "Andre", 10, 10, 10, 10, 50, 10, 10)
    voiture = Car("Ferrari", "Fisenzo", 10, 10, 10, 10, 50, 10, 100)
    ferrari = Car("Pedalo", "Patrick", 10, 10, 10, 10, 150, 90 , 11)
    car = []
    race = Race(tuture, toto, carglass, titi, niglo, voiture, ferrari)
    asyncio.run(race.run())