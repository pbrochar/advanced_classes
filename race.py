import asyncio
from error import OutOfGazError
from car import Car
from typing import Optional, Tuple


class Race:
    def __init__(
            self, *args: list[Car]
    ):
        self.cars: list[Car] = args
    
    def __iter__(self):
        for car in self.cars:
            yield dict(car)

    def _print_results(self, results: list[tuple], grading_unit: str) -> None:
        """
        The result list is divided into two lists: the list of ranked cars and the list of unranked cars.
        Depending on the grading_unit, the ranked list is sorted by time (grading_unit = 's') or by distance (grading_unit = 'm')
        """
        
        ranked, unranked = [], []
        for result in results: # split results in two list : ranked and if necessary unranked cars
            if isinstance(result[0], OutOfGazError):
                unranked.append(result)
            else:
                ranked.append(result)
    
        # Sort the two list, if grading_unit is 'm' the distance covered is calculated from the race time and the maximum_speed of the car.
        # For the unranked car, sort is only done by distance covered.
        ranked.sort(key=None if grading_unit == 's' else lambda car_ranked: car_ranked[0] * car_ranked[1].maximum_speed, reverse=True if grading_unit == 'm' else False)
        unranked.sort(key=lambda car_unranked: car_unranked[0].move_time * car_unranked[1].maximum_speed, reverse=True)

        rank = 1
        if ranked:
            print("=== RANKED ===")
            for car in ranked:
                print(f"Rank {rank} -> {'TIME' if grading_unit == 's' else 'DISTANCE'} : {round(car[1], 3) if grading_unit == 's' else car[1].maximum_speed} {grading_unit} -> Car : {car[1].model} - {car[1].name}")
                rank += 1
        if unranked:
            print("=== UNRANKED ===")    
            for car in unranked:
                print(f"Rank {rank} -> DISTANCE : {round(car[0].move_time * car[1].maximum_speed, 3)} m -> Car : {car[1].model} - {car[1].name} ")
                rank += 1
    
    def full_gas(self) -> None:
        for car in self.cars:
            car.put_fuel()

    async def run(self, distance: Optional[int] = None) -> None:
        """
        Method to start the race with all the cars.
        If no distance is specified then the race will be run until the fuel is exhausted.
        If there is no precise distance then the ranking will be done on the distance covered (grading_unit = 'm'), otherwise, on the time (grading_unit = 's')
        The results are then put in the form of a list[tuple] containing the race time and the corresponding car
        """
        move_times = await asyncio.gather(*[
            car.move_on(duration=None if distance is None else distance / car.maximum_speed)
            for car in self.cars     
        ], return_exceptions=True)
        results = list(zip(move_times, self.cars))
        self._print_results(results, grading_unit='m' if distance is None else 's')
    