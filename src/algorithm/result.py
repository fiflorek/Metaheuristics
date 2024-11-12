from typing import List


class Result:

    def __init__(self, best: float, average: float, best_genotype: List[int]):
        self.best = best
        self.average = average
        self.best_genotype = best_genotype

    def __str__(self):
        return f"Best: {self.best}, Average: {self.average}, Best genotype: {self.best_genotype}"
