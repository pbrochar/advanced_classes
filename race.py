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
        move_times = await asyncio.gather(*[
            car.move_on(duration=None if distance is None else distance / car.maximum_speed)
            for car in self.cars     
        ], return_exceptions=True)
        results = list(zip(move_times, self.cars))
        self._print_results(results, grading_unit='m' if distance is None else 's')
    