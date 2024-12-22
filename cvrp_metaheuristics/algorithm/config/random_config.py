from pydantic import PositiveInt

from cvrp_metaheuristics.algorithm.config.configuration import Config


class RandomConfig(Config):
    """
    Configuration for Random Algorithm.

    Attributes:
        no_of_solutions: int -> Number of solutions to generate
    """
    no_of_solutions: PositiveInt
