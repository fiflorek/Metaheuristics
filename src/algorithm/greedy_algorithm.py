import sys

from src.algorithm.result import Result
from src.problem.cvrp import cost

from src.algorithm.algorithm import Algorithm


class GreedyAlgorithm(Algorithm):
    _current_city: int
    _visited_cities: dict[int, int]

    def _initialize_algorithm(self) -> None:
        # city_id, visit_sequence pair
        self._visited_cities = {}
        self._solution = []
        self.visit_city(0, 0)

    @property
    def current_city(self) -> int:
        return self._current_city

    @property
    def visited_cities(self) -> dict[int, int]:
        return self._visited_cities

    def visit_city(self, city_id: int, visit_sequence: int) -> None:
        self._current_city = city_id
        self._visited_cities[city_id] = visit_sequence

    def find_nearest_city_not_yet_visited(self) -> int:
        return min(range(self.no_of_cities), key=lambda city: self.distances_matrix[self.current_city][
            city] if city not in self.visited_cities.keys() else sys.maxsize)

    # search through not visited cities. Find the nearest one

    def solve(self) -> list[Result]:
        for i in range(1, self._cvrp.no_of_cities):
            self.visit_city(self.find_nearest_city_not_yet_visited(), i)

        genotype = [city_id for city_id, visit_sequence in sorted(self.visited_cities.items(), key=lambda item: item[1])]
        best = average = cost(self.cvrp, genotype)
        # not including depot number in the solution (0)
        genotype.remove(self.depot_number)

        self.result_list.append(Result(best, round(average, 2), genotype))

        return self.result_list
