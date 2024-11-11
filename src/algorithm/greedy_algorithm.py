import sys

from algorithm.result import Result
from problem.cvrp import cost
from problem.cvrp import Cvrp
from utils.configuration import Config


def find_nearest(cvrp: Cvrp, city_id: int, visited_cities: list[int]) -> int:
    closest = sys.maxsize
    closest_index = 0
    for i, value in enumerate(cvrp.distances_matrix[city_id]):
        if i not in visited_cities and value < closest:
            closest_index = i
            closest = value
    return closest_index


def solve_cvrp_greedy(cvrp: Cvrp, config: Config) -> Result:
    current_city_id = 0
    solution = [current_city_id]
    for _ in range(1, cvrp.no_of_cities):
        nearest_city_id = find_nearest(cvrp, current_city_id, solution)
        solution.append(nearest_city_id)
        current_city_id = nearest_city_id

    best, average = cost(cvrp, solution)
    best_genotype = solution

    return Result(best, round(average, 2), best_genotype)
