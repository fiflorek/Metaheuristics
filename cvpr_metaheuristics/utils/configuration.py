from typing import Any, Dict

from cvpr_metaheuristics.utils.enums import AlgorithmName, Crossover, Mutation, Initialization


class Config:
    def __init__(self, config_dict: Dict[str, Any]):
        self.problem_instance = config_dict.get("problem_instance", "A-n32-k5")
        self.no_of_runs = config_dict.get("no_of_runs", 1)
        self.algorithm = AlgorithmName(config_dict.get("algorithm", "random"))
        self.population_size = config_dict.get("population_size", 100)
        self.generations = config_dict.get("generations", 10)
        self.crossover_probability = config_dict.get("crossover_probability")
        self.crossover_type = Crossover(config_dict.get("crossover_type"))
        self.mutation_probability = config_dict.get("mutation_probability")
        self.mutation_type = Mutation(config_dict.get("mutation_type"))
        self.tournament_size = config_dict.get("tournament_size")
        self.init_type = Initialization(config_dict.get("init_type"))

    def __str__(self):
        return f"problem_instance: {self.problem_instance}, no_of_runs: {self.no_of_runs}, algorithm: {self.algorithm}, " \
               f"population_size: {self.population_size}, generations: {self.generations}, init_type: {self.init_type}, " \
               f"crossover_probability: {self.crossover_probability}, mutation_probability: {self.mutation_probability}, " \
               f"crossover_type: {self.crossover_type.name}, mutation_type: {self.mutation_type.name}, tournament_size: {self.tournament_size}"
