import random
import sys

from algorithm.algorithm import Algorithm
from algorithm.result import Result
from problem.cvrp import cost, Cvrp
from utils.configuration import Config
from utils.init_methods import init_random_genotype


class RandomAlgorithm(Algorithm):

    def _initialize_algorithm(self) -> None:
        pass

    def solve(self) -> list[Result]:
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

        self.result_list.append(Result(best, round(average, 2), best_genotype))

        return self.result_list

    def generate_random_solution(self) -> list[int]:
        return init_random_genotype(self.cvrp)




