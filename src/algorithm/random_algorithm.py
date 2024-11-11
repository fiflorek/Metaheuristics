import random
import sys

from algorithm.result import Result
from problem.cvrp import cost, Cvrp
from utils.configuration import Config


def generate_random_solution(cvrp: Cvrp):
    city_ids = list(range(1, cvrp.no_of_cities))
    return random.sample(city_ids, len(city_ids))


def solve_cvrp_random(cvrp: Cvrp, config: Config) -> Result:
    no_of_solutions = config.population_size * config.generations
    best = sys.maxsize
    best_genotype = []
    average = 0
    solutions = []
    for _ in range(no_of_solutions):
        solution = generate_random_solution(cvrp)
        solutions.append(solution)
        solution_cost = cost(cvrp, solution)
        if solution_cost < best:
            best = solution_cost
            best_genotype = solution
        average += solution_cost
    average /= no_of_solutions

    return Result(best, round(average, 2), best_genotype)
