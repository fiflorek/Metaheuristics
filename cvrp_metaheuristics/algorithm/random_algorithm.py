import random
import sys

<<<<<<< HEAD:cvrp_metaheuristics/algorithm/random_algorithm.py
from cvrp_metaheuristics.algorithm.algorithm import Algorithm
from cvrp_metaheuristics.algorithm.result import Result
from cvrp_metaheuristics.problem.cvrp import cost
=======
from algorithm.algorithm import Algorithm
from algorithm.result import Result
from problem.cvrp import cost, Cvrp
from utils.configuration import Config
from utils.init_methods import init_random_genotype
>>>>>>> 4eda22e (standarize init methods):src/algorithm/random_algorithm.py


class RandomAlgorithm(Algorithm):

    def _initialize_algorithm(self) -> None:
        pass

    def solve(self) -> list[Result]:
        no_of_solutions = self.config.population_size * self.config.generations
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

        self.result_list.append(Result(best, round(average, 2), best_genotype))

        return self.result_list

    def generate_random_solution(self) -> list[int]:
<<<<<<< HEAD:cvrp_metaheuristics/algorithm/random_algorithm.py
        city_ids = list(range(1, self.no_of_cities))
        return random.sample(city_ids, len(city_ids))
=======
        return init_random_genotype(self.cvrp)




>>>>>>> 4eda22e (standarize init methods):src/algorithm/random_algorithm.py
