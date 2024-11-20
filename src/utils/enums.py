from enum import Enum


class AlgorithmName(Enum):
    GENETIC = 'genetic'
    RANDOM = 'random'
    GREEDY = 'greedy'
    ANNEALING = 'annealing'
    TABU_SEARCH = 'tabu_search'

    def is_metaheuristic(self):
        return self in [AlgorithmName.GENETIC, AlgorithmName.ANNEALING, AlgorithmName.TABU_SEARCH]


class Mutation(Enum):
    SWAP = 'swap'
    INVERSION = 'inversion'


class Selection(Enum):
    ROULETTE = 'roulette'
    TOURNAMENT = 'tournament'


class Initialization(Enum):
    RANDOM = 'random'
    GREEDY = 'greedy'


class Crossover(Enum):
    PMX = 'pmx'
    OX = 'ox'


class DataFileConstants(Enum):
    NAME = 'NAME'
    COMMENT = 'COMMENT'
    TYPE = 'TYPE'
    DIMENSION = 'DIMENSION'
    EDGE_WEIGHT_TYPE = 'EDGE_WEIGHT_TYPE'
    CAPACITY = 'CAPACITY'
    NODE_COORD_SECTION = 'NODE_COORD_SECTION'
    DEMAND_SECTION = 'DEMAND_SECTION'
    DEPOT_SECTION = 'DEPOT_SECTION'
    EOF = 'EOF'
