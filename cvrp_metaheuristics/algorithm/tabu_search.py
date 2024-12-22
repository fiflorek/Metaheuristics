import random
from typing import Set

from cvrp_metaheuristics.algorithm.config.tabu_config import TabuSearchConfig
from cvrp_metaheuristics.algorithm.algorithm import Algorithm
from cvrp_metaheuristics.algorithm.result import Result
from cvrp_metaheuristics.utils.enums import Initialization, Mutation
from cvrp_metaheuristics.problem.individual import Individual, mutate
from cvrp_metaheuristics.utils.init_methods import init_random_genotype, init_greedy_genotype


class TabuSearch(Algorithm):
    _current_best: Individual
    _tabu_set: Set[int]  # this set contains hashes of genotypes
    _tabu_list: list[int]  # this list contains hashes of genotypes - helps with removing the oldest element
    config: TabuSearchConfig

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

    @current_best.setter
    def current_best(self, best: Individual) -> None:
        self._current_best = best

    @property
    def tabu_set(self) -> Set[int]:
        return self._tabu_set

    @property
    def tabu_list(self) -> list[int]:
        return self._tabu_list

    @property
    def init_type(self) -> Initialization:
        return self.config.init_type

    @property
    def generations(self) -> int:
        return self.config.generations

    @property
    def mutation_type(self) -> Mutation:
        return self.config.mutation_type

    def solve(self) -> list[Result]:
        """
        Solves the CVRP problem using the Tabu Search algorithm.

        This method iterates through generations, searching for the best solution
        in the neighborhood and updating the tabu list to avoid revisiting solutions.

        Returns:
            list[Result]: A list of results, each containing the fitness of the best
            individual, the average fitness of the neighborhood, and the genotype of
            the best individual.
        """
        results = []
        for i in range(1, self.generations):
            neighbours = self.search_neighbourhood()
            best_neighbour = self.best_neighbour_not_in_tabu(neighbours)
            # if all neighbours were already visited (are in tabu list) we're switching the neighbourhood drastically
            # (random genotype)
            if best_neighbour is None:
                best_neighbour = self.change_neighbourhood()
            self.current_best = best_neighbour
            self.update_tabu(best_neighbour)
            avg_fitness = sum([neighbour.fitness for neighbour in neighbours]) / len(neighbours)
            results.append(Result(self.current_best.fitness, avg_fitness, self.current_best.genotype))

        return results

    def init_individual(self) -> None:
        if self.config.init_type == Initialization.RANDOM:
            genotype = init_random_genotype(self.cvrp)
        else:
            genotype = init_greedy_genotype(self.cvrp, self.config)
        self.current_best = Individual(genotype)
        self.current_best.evaluate(self.cvrp)

    def search_neighbourhood(self) -> list[Individual]:
        neighbours: list[Individual] = []
        for i in range(self.neighbourhood_size):
            neighbour_genotype = mutate(self.current_best.genotype[:], self.mutation_type)
            neighbour = Individual(neighbour_genotype)
            neighbour.evaluate(self.cvrp)
            neighbours.append(neighbour)
        return neighbours

    def best_neighbour_not_in_tabu(self, neighbours: list[Individual]) -> Individual | None:
        best_neighbour = None
        best_neighbour_fitness = float('inf')
        for neighbour in neighbours:
            if (neighbour.fitness < best_neighbour_fitness
                    and hash(tuple(neighbour.genotype)) not in self.tabu_set):
                best_neighbour_fitness = neighbour.fitness
                best_neighbour = neighbour
        return best_neighbour

    def update_tabu(self, best_neighbour) -> None:
        genotype_hash = hash(tuple(best_neighbour.genotype))
        self.tabu_set.add(genotype_hash)
        self.tabu_list.append(genotype_hash)
        if len(self.tabu_list) > self.config.tabu_list_size:
            self.tabu_set.remove(self.tabu_list.pop(0))

    def change_neighbourhood(self) -> Individual:
        genotype = init_random_genotype(self.cvrp)
        while hash(tuple(genotype)) in self.tabu_set:
            random.shuffle(genotype)
        i = Individual(genotype)
        i.evaluate(self.cvrp)
        return i
