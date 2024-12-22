import random

from cvrp_metaheuristics.algorithm.config.genetic_config import GeneticConfig
from cvrp_metaheuristics.algorithm.algorithm import Algorithm
from cvrp_metaheuristics.algorithm.result import Result
from cvrp_metaheuristics.problem import individual
from cvrp_metaheuristics.problem.cvrp import Cvrp
from cvrp_metaheuristics.problem.individual import Individual
from cvrp_metaheuristics.utils.enums import Initialization, Crossover, Mutation
from cvrp_metaheuristics.utils.init_methods import init_random_genotype, init_greedy_genotype


class Population:

    def __init__(self, population: list[Individual]):
        self.population = population

    def best_individual(self) -> Individual:
        return min(self.population, key=lambda ind: ind.fitness)

    def average_individual_fitness(self) -> float:
        return sum([ind.fitness for ind in self.population]) / len(self.population)

    def worst_individual(self) -> Individual:
        return max(self.population, key=lambda ind: ind.fitness)

    def evaluate(self, cvrp: Cvrp) -> None:
        for ind in self.population:
            ind.evaluate(cvrp)


class GeneticAlgorithm(Algorithm):
    _current_population: Population
    _current_best: Individual
    config: GeneticConfig

    def _initialize_algorithm(self) -> None:
        self.initialize_population()
        self.current_population.evaluate(self.cvrp)
        self.current_best = self.current_population.best_individual()
        self.result_list.append(Result(self.current_best.fitness,
                                       self.current_population.average_individual_fitness(),
                                       self.current_best.genotype))

    @property
    def current_population(self) -> Population:
        return self._current_population

    @current_population.setter
    def current_population(self, population: Population) -> None:
        self._current_population = population

    @property
    def current_best(self) -> Individual:
        return self._current_best

    @current_best.setter
    def current_best(self, best: Individual) -> None:
        self._current_best = best

    @property
    def tournament_size(self):
        return self.config.tournament_size

    @property
    def crossover_probability(self):
        return self.config.crossover_probability

    @property
    def mutation_probability(self):
        return self.config.mutation_probability

    @property
    def init_type(self) -> Initialization:
        return self.config.init_type

    @property
    def population_size(self) -> int:
        return self.config.population_size

    @property
    def generations(self) -> int:
        return self.config.generations

    @property
    def crossover_type(self) -> Crossover:
        return self.config.crossover_type

    @property
    def mutation_type(self) -> Mutation:
        return self.config.mutation_type

    def selection(self, population: list[Individual]) -> Individual:
        tournament = []
        for i in range(self.tournament_size):
            tournament.append(population[random.randint(0, len(population) - 1)])

        return min(tournament, key=lambda ind: ind.fitness)

    def initialize_population(self) -> None:
        population = []
        if self.init_type == Initialization.RANDOM:
            for _ in range(self.population_size):
                genotype = init_random_genotype(self.cvrp)
                population.append(Individual(genotype))
        else:
            genotype = init_greedy_genotype(self.cvrp, self.config)
            for _ in range(self.population_size):
                population.append(Individual(genotype))

        self.current_population = Population(population)

    def solve(self) -> list[Result]:
        """
        Solves the CVRP problem using the Genetic Algorithm.

        This method iterates through generations, applying selection, crossover,
        and mutation to evolve the population towards better solutions.

        Returns:
            list[Result]: A list of results, each containing the fitness of the best
            individual, the average fitness of the population, and the genotype of
            the best individual.
             """
        for i in range(1, self.generations):
            new_population: list[Individual] = []
            while len(new_population) < self.population_size:
                parent_a = self.selection(self.current_population.population)
                parent_b = self.selection(self.current_population.population)
                child_a_genotype = parent_a.genotype[:]
                child_b_genotype = parent_b.genotype[:]
                if random.random() < self.crossover_probability:
                    child_a_genotype, child_b_genotype = (
                        individual.cross(parent_a.genotype, parent_b.genotype, self.crossover_type))
                if random.random() < self.mutation_probability:
                    child_a_genotype = individual.mutate(child_a_genotype, self.mutation_type)
                    child_b_genotype = individual.mutate(child_b_genotype, self.mutation_type)
                new_population.append(Individual(child_a_genotype))
                new_population.append(Individual(child_b_genotype))
            self.current_population = Population(new_population)
            self.current_population.evaluate(self.cvrp)
            self.current_best = self.current_population.best_individual()
            self.result_list.append(Result(self.current_best.fitness,
                                           self.current_population.average_individual_fitness(),
                                           self.current_best.genotype))

        return self.result_list
