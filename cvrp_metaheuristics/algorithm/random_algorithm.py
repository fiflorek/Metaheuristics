import sys

from cvrp_metaheuristics.algorithm.algorithm import Algorithm
from cvrp_metaheuristics.algorithm.config.random_config import RandomConfig
from cvrp_metaheuristics.algorithm.result import Result
from cvrp_metaheuristics.problem.cvrp import cost
from cvrp_metaheuristics.utils.init_methods import init_random_genotype


class RandomAlgorithm(Algorithm):

    config: RandomConfig

    def _initialize_algorithm(self) -> None:
        pass

    def solve(self) -> list[Result]:
        """
        Solves the CVRP problem using a Random Algorithm

        This method generates random solutions and selects the best one.

        Returns:
            list[Result]: A list of results, each containing the fitness of the best
            individual, the average fitness of the generated solutions, and the genotype
            of the best individual.
        """
        no_of_solutions = self.config.no_of_solutions
        best = sys.float_info.max
        best_genotype = []
        average = 0.0
        for _ in range(no_of_solutions):
            solution = self.generate_random_solution()
            solution_cost = cost(self.cvrp, solution)
            if solution_cost < best:
                best = solution_cost
                best_genotype = solution
            average += solution_cost
        average /= no_of_solutions

        self.result_list.append(Result(best, average, best_genotype))

        return self.result_list

    def generate_random_solution(self) -> list[int]:
        return init_random_genotype(self.cvrp)
