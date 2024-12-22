from pydantic import BaseModel

from cvrp_metaheuristics.utils.enums import AlgorithmName


class Config(BaseModel):
    problem_instance: str = "A-n32-k5"
    algorithm: AlgorithmName = AlgorithmName.GREEDY
