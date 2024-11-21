import random

from algorithm.greedy_algorithm import GreedyAlgorithm
from problem.cvrp import Cvrp
from utils.configuration import Config


def init_random_genotype(cvrp: Cvrp) -> list[int]:
    genotype = list(range(1, cvrp.no_of_cities))
    random.shuffle(genotype)
    return genotype


def init_greedy_genotype(cvrp: Cvrp, config: Config) -> list[int]:
    return GreedyAlgorithm(cvrp, config).solve()[0].best_genotype
