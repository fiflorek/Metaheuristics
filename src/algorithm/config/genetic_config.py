from typing import Dict, Any

from algorithm.config.configuration import Config
from utils.enums import Crossover, Mutation, Initialization


class GeneticConfig(Config):
    _no_of_runs: int
    _population_size: int
    _generations: int
    _init_type: Initialization
    _crossover_probability: float
    _crossover_type: Crossover
    _mutation_probability: float
    _mutation_type: Mutation
    _tournament_size: int

    def __init__(self, config_dict: Dict[str, Any]):
        super().__init__(config_dict)
        self._no_of_runs = config_dict.get("no_of_runs", 1)
        self._population_size = config_dict.get("population_size", 100)
        self._generations = config_dict.get("generations", 10)
        self._crossover_probability = config_dict.get("crossover_probability")
        self._crossover_type = Crossover(config_dict.get("crossover_type", "ox"))
        self._mutation_probability = config_dict.get("mutation_probability")
        self._mutation_type = Mutation(config_dict.get("mutation_type", "swap"))
        self._tournament_size = config_dict.get("tournament_size")
        self._init_type = Initialization(config_dict.get("init_type", "random"))

    @property
    def no_of_runs(self) -> int:
        return self._no_of_runs

    @property
    def population_size(self) -> int:
        return self._population_size

    @property
    def generations(self) -> int:
        return self._generations

    @property
    def init_type(self) -> Initialization:
        return self._init_type

    @property
    def crossover_probability(self) -> float:
        return self._crossover_probability

    @property
    def crossover_type(self) -> Crossover:
        return self._crossover_type

    @property
    def mutation_probability(self) -> float:
        return self._mutation_probability

    @property
    def mutation_type(self) -> Mutation:
        return self._mutation_type

    @property
    def tournament_size(self) -> int:
        return self._tournament_size

    def __str__(self):
        return super().__str__() + f"Population size: {self.population_size}\n" \
                                   f"Generations: {self.generations}\n" \
                                   f"Initialization type: {self.init_type}\n" \
                                   f"Crossover probability: {self.crossover_probability}\n" \
                                   f"Crossover type: {self.crossover_type}\n" \
                                   f"Mutation probability: {self.mutation_probability}\n" \
                                   f"Mutation type: {self.mutation_type}\n" \
                                   f"Tournament size: {self.tournament_size}\n" \
                                   f"Number of runs: {self.no_of_runs}\n"
