import random
import sys

from algorithm.algorithm import Algorithm
from algorithm.result import Result
from problem.cvrp import cost, Cvrp
from utils.configuration import Config


class RandomAlgorithm(Algorithm):

    def _initialize_algorithm(self) -> None:
        pass

    def solve(self) -> Result:
        no_of_solutions = self.config.population_size * self.config.generations
        best = sys.maxsize
        best_genotype = []
        average = 0
        solutions = []
        for _ in range(no_of_solutions):
            solution = self.generate_random_solution()
            solutions.append(solution)
            solution_cost = cost(self.cvrp, solution)
            if solution_cost < best:
                best = solution_cost
                best_genotype = solution
            average += solution_cost
        average /= no_of_solutions

        return Result(best, round(average, 2), best_genotype)

    def generate_random_solution(self) -> list[int]:
        city_ids = list(range(1, self.no_of_cities))
        return random.sample(city_ids, len(city_ids))




