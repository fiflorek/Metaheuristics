from typing import Any, Dict

from cvrp_metaheuristics.utils.enums import AlgorithmName


class Config:
    _problem_instance: str
    _algorithm: AlgorithmName

    def __init__(self, config_dict: Dict[str, Any]):
        self.problem_instance = config_dict.get("problem_instance", "A-n32-k5")
        self.algorithm = AlgorithmName(config_dict.get("algorithm", "greedy"))

    def __str__(self):
        return (f"Problem instance: {self.problem_instance}\n"
                f"Algorithm: {self.algorithm}\n")