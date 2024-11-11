from typing import Any, Dict

from utils.enums import Algorithm


class Config:
    def __init__(self, config_dict: Dict[str, Any]):
        self.problem_instance = config_dict.get("problem_instance")
        self.no_of_runs = config_dict.get("no_of_runs")
        self.algorithm = Algorithm(config_dict.get("algorithm"))
        self.population_size = config_dict.get("population_size")
        self.generations = config_dict.get("generations")
        self.crossover_probability = config_dict.get("crossover_probability")
        self.mutation_probability = config_dict.get("mutation_probability")
        self.mutation_type = config_dict.get("mutation_type")
        self.tournament_size = config_dict.get("tournament_size")
