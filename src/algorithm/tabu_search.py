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
    _tabu_set: Set[int]  # this set contains hashes of genotypes
    _tabu_list: list[int]  # this list contains hashes of genotypes - helps with removing the oldest element

    def _initialize_algorithm(self) -> None:
        self._tabu_set = set()
        self._tabu_list = []
        self.init_individual()

    @property
    def neighbourhood_size(self) -> int:
        return self.config.neighbourhood_size

    @property
    def current_best(self) -> Individual:
        return self._current_best

    @property
    def tabu_set(self) -> Set[int]:
        return self._tabu_set

    @current_best.setter
    def current_best(self, best: Individual) -> None:
        self._current_best = best

    @property
    def tabu_list(self) -> list[int]:
        return self._tabu_list

    def solve(self) -> list[Result]:
        results = []
        for i in range(1, self.generations):
            neighbours = self.search_neighbourhood()
            best_neighbour = self.best_neighbour_not_in_tabu(neighbours)
            # if all neighbours were already visited (are in tabu list) we're switching the neighbourhood drastically
            # (random genotype)
            if best_neighbour is None:
                genotype = list(range(1, self.no_of_cities))
                random.shuffle(genotype)
                while hash(tuple(genotype)) in self.tabu_set:
                    random.shuffle(genotype)
                best_neighbour = Individual(genotype)
                best_neighbour.evaluate(self.cvrp)
            self.current_best = best_neighbour
            self.update_tabu(best_neighbour)
            avg_fitness = round(sum([neighbour.fitness for neighbour in neighbours]) / len(neighbours), 2)
            results.append(Result(self.current_best.fitness, avg_fitness, self.current_best.genotype))

        return results

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
                    and hash(tuple(neighbours[i].genotype)) not in self.tabu_set):
                best_neighbour_fitness = neighbours[i].fitness
                best_neighbour = neighbours[i]
        return best_neighbour

    def update_tabu(self, best_neighbour) -> None:
        genotype_hash = hash(tuple(best_neighbour.genotype))
        self.tabu_set.add(genotype_hash)
        self.tabu_list.append(genotype_hash)
        if len(self.tabu_list) > self.config.tabu_list_size:
            self.tabu_set.remove(self.tabu_list.pop(0))
