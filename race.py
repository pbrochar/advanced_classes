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
        rank = 1
        ranked, unranked = [], []
        for result in results:
            if isinstance(result[0], OutOfGazError):
                unranked.append(result)
            else:
                ranked.append(result)
        ranked.sort(key=None if grading_unit == 's' else lambda car_ranked: car_ranked[0] * car_ranked[1].maximum_speed, reverse=True if grading_unit == 'm' else False)
        unranked.sort(key=lambda car_unranked: car_unranked[0].move_time * car_unranked[1].maximum_speed, reverse=True)
        if ranked:
            print("=== RANKED ===")
            for i in range(0, len(ranked), 1):
                print(f"Rank {rank} -> {'TIME' if grading_unit == 's' else 'DISTANCE'} : {round(ranked[i][0], 3) if grading_unit == 's' else ranked[i][1].maximum_speed} {grading_unit} -> Car : {ranked[i][1].model} - {ranked[i][1].name}")
                rank += 1
        if unranked:
            print("=== UNRANKED ===")    
            for i in range(0, len(unranked), 1):
                print(f"Rank {rank} -> DISTANCE : {round(unranked[i][0].move_time * unranked[i][1].maximum_speed, 3)} m -> Car : {unranked[i][1].model} - {unranked[i][1].name} ")
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
    