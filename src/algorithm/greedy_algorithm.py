import sys

from algorithm.result import Result
from problem.cvrp import cost

from src.algorithm.algorithm import Algorithm


class GreedyAlgorithm(Algorithm):
    _current_city: int
    _visited_cities: list[int]

    def _initialize_algorithm(self) -> None:
        self._visited_cities = []
        self.visit_city(0)

    @property
    def current_city(self) -> int:
        return self._current_city

    @property
    def visited_cities(self) -> list[int]:
        return self._visited_cities

    def visit_city(self, city_id: int) -> None:
        self._current_city = city_id
        self._visited_cities.append(city_id)

    def find_nearest_city_not_yet_visited(self) -> int:
        return min(range(self.no_of_cities), key=lambda city: self.distances_matrix[self.current_city][
            city] if city not in self.visited_cities else sys.maxsize)

    def solve(self) -> Result:
        for _ in range(1, self._cvrp.no_of_cities):
            self.visit_city(self.find_nearest_city_not_yet_visited())

        best = average = cost(self.cvrp, self.visited_cities)
        best_genotype = self.visited_cities

        return Result(best, round(average, 2), best_genotype)
