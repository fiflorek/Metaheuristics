from pydantic import PositiveInt, field_validator

from cvrp_metaheuristics.algorithm.config.configuration import Config
from cvrp_metaheuristics.utils.enums import Mutation, Initialization


class TabuSearchConfig(Config):
    """
    Configuration for Tabu Search Algorithm.

    Attributes:
        no_of_runs (int): How many times the algorithm should be run.
        generations (int): Number of generations (within one run of the algorithm).
        init_type (Initialization): Type of initialization, currently supported are: greedy, random.
        neighbourhood_size (int): Number of neighbours to visit in each generation.
        tabu_list_size (int): Size of the tabu list.
        mutation_type (Mutation): Type of mutation, currently supported are: swap, inversion.
    """
    no_of_runs: int
    init_type: Initialization
    generations: PositiveInt
    neighbourhood_size: PositiveInt
    tabu_list_size: PositiveInt
    mutation_type: Mutation

    @field_validator('no_of_runs')
    def is_valid_no_of_runs(cls, value: int) -> int:
        if value < 1 or value > 10:
            raise ValueError('Number of runs has to be in range [1, 10]')
        return value
