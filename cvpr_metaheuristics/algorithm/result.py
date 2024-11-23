from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Result:
    best: float
    average: float
    best_genotype: List[int]

    def __str__(self):
        return f"Best: {self.best}, Average: {self.average}, Best genotype: {self.best_genotype}"
