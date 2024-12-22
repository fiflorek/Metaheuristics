from typing_extensions import Self

from pydantic import PositiveInt, model_validator, field_validator

from cvrp_metaheuristics.algorithm.config.configuration import Config
from cvrp_metaheuristics.utils.enums import Crossover, Mutation, Initialization


class GeneticConfig(Config):
    """
    Configuration for Genetic Algorithm.

    Attributes:
        no_of_runs (int): How many times should the algorithm be run.
        population_size (int): Number of individuals in the population (population represents one generation).
        generations (int): Number of generations (within one run of the algorithm).
        init_type (Initialization): Type of initialization, currently supported are: greedy, random.
        crossover_probability (float): Probability of crossover (0.0 - 1.0).
        crossover_type (Crossover): Type of crossover, currently supported are: pmx, ox.
        mutation_probability (float): Probability of mutation (0.0 - 1.0).
        mutation_type (Mutation): Type of mutation, currently supported are: swap, inversion.
        tournament_size (int): How many individuals should participate in the tournament selection.
    """
    no_of_runs: int
    population_size: PositiveInt
    generations: PositiveInt
    init_type: Initialization
    crossover_probability: float
    crossover_type: Crossover
    mutation_probability: float
    mutation_type: Mutation
    tournament_size: int

    @model_validator(mode='after')
    def is_less_than_pop_size(self) -> Self:
        if 0 > self.tournament_size or self.tournament_size >= self.population_size:
            raise ValueError('Tournament size has to be in range [1, population_size]')
        return self

    @field_validator('crossover_probability', 'mutation_probability')
    def is_valid_probability(cls, value: float) -> float:
        if value < 0.0 or value > 1.0:
            raise ValueError('Probability has to be in range [0.0, 1.0]')
        return value

    @field_validator('no_of_runs')
    def is_valid_no_of_runs(cls, value: int) -> int:
        if value < 1 or value > 10:
            raise ValueError('Number of runs has to be in range [1, 10]')
        return value
