import random

from cvrp_metaheuristics.algorithm.config.configuration import Config
from cvrp_metaheuristics.algorithm.greedy_algorithm import GreedyAlgorithm
from cvrp_metaheuristics.problem.cvrp import Cvrp


def init_random_genotype(cvrp: Cvrp) -> list[int]:
    genotype = list(range(1, cvrp.no_of_cities))
    random.shuffle(genotype)
    return genotype


def init_greedy_genotype(cvrp: Cvrp, config: Config) -> list[int]:
    return GreedyAlgorithm(cvrp, config).solve()[0].best_genotype
