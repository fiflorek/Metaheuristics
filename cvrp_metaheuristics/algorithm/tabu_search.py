import random
from typing import Set

from algorithm.algorithm import Algorithm
from algorithm.greedy_algorithm import GreedyAlgorithm
from algorithm.result import Result
from problem.individual import Individual
from utils.enums import Initialization
from problem import individual


class TabuSearch(Algorithm):
    _current_best: Individual
    _tabu_list: Set[int]  # this set contains hashes of genotypes

    def _initialize_algorithm(self) -> None:
        self.init_individual()

    @property
    def neighbourhood_size(self) -> int:
        return self.config.neighbourhood_size

    @property
    def current_best(self) -> Individual:
        return self._current_best

    @property
    def tabu_list(self) -> Set[int]:
        return self._tabu_list

    @current_best.setter
    def current_best(self, best: Individual) -> None:
        self._current_best = best

    def solve(self) -> list[Result]:
        for i in range(1, self.generations):
            neighbours = self.search_neighbourhood()
            best_neighbour = self.best_neighbour_not_in_tabu(neighbours)
            if best_neighbour is not None:
                self.current_best = best_neighbour

    def init_individual(self) -> None:
        if self.config.init_type == Initialization.RANDOM:
            genotype = list(range(1, self.no_of_cities))
            random.shuffle(genotype)
        else:
            genotype = GreedyAlgorithm(self.cvrp, self.config).solve()[0].best_genotype
        self.current_best = Individual(genotype)
        self.current_best.evaluate(self.cvrp)

    def search_neighbourhood(self) -> list[Individual]:
        neighbours: list[Individual] = []
        for i in range(self.neighbourhood_size):
            # TO CHECK: is it updated in place?
            # neighbour_genotype = self.current_best.genotype[:]
            # individual.mutate(neighbour_genotype, self.mutation_type)
            neighbour_genotype = individual.mutate(self.current_best.genotype[:], self.mutation_type)
            neighbour = Individual(neighbour_genotype)
            neighbour.evaluate(self.cvrp)
            neighbours.append(neighbour)
        return neighbours

    def best_neighbour_not_in_tabu(self, neighbours: list[Individual]) -> Individual:
        best_neighbour = None
        best_neighbour_fitness = float('inf')
        for i in range(1, len(neighbours)):
            if (neighbours[i].fitness < best_neighbour_fitness
                    and hash(tuple(neighbours[i].genotype)) not in self.tabu_list):
                best_neighbour_fitness = neighbours[i].fitness
                best_neighbour = neighbours[i]
        return best_neighbour
