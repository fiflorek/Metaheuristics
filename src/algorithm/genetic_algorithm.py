import random

from algorithm.algorithm import Algorithm
from algorithm.result import Result
from problem import individual
from problem.cvrp import Cvrp
from problem.individual import Individual
from utils.configuration import Config


class Population:

    def __init__(self, population: list[Individual]):
        self.population = population

    def best_individual(self) -> Individual:
        return min(self.population, key=lambda ind: ind.fitness)

    def average_individual_fitness(self) -> float:
        return round(sum([ind.fitness for ind in self.population]) / len(self.population), 2)

    def worst_individual(self) -> Individual:
        return max(self.population, key=lambda ind: ind.fitness)

    def evaluate(self, cvrp: Cvrp) -> None:
        for ind in self.population:
            ind.evaluate(cvrp)


class GeneticAlgorithm(Algorithm):

    _current_population: Population
    _current_best: Individual

    def _initialize_algorithm(self) -> None:
        self.initialize_population()
        self.current_population.evaluate(self.cvrp)
        self.current_best = self.current_population.best_individual()
        self.result_list.append(Result(self.current_best.fitness,
                                       self.current_population.average_individual_fitness(), self.current_best.genotype))

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
    def mutation_type(self):
        return self.config.mutation_type

    def selection(self, population: list[Individual]) -> Individual:
        tournament = []
        for i in range(self.tournament_size):
            tournament.append(population[random.randint(0, len(population) - 1)])

        return min(tournament, key=lambda ind: ind.fitness)

    def initialize_population(self) -> None:
        population = []
        for _ in range(self.population_size):
            genotype = list(range(1, self.no_of_cities))
            random.shuffle(genotype)
            population.append(Individual(genotype))

        self.current_population = Population(population)

    def solve(self) -> list[Result]:

        for i in range(1, self.generations):
            new_population = []
            for j in range(self.population_size):
                parent_a = self.selection(self.current_population.population)
                parent_b = self.selection(self.current_population.population)
                child_genotype = parent_a.genotype[:]
                if random.random() < self.crossover_probability:
                    child_genotype = individual.cross(parent_a.genotype, parent_b.genotype)
                if random.random() < self.mutation_probability:
                    child_genotype = individual.mutate(child_genotype, self.mutation_type)
                new_population.append(Individual(child_genotype))
            self.current_population = Population(new_population)
            self.current_population.evaluate(self.cvrp)
            self.current_best = self.current_population.best_individual()
            self.result_list.append(Result(self.current_best.fitness,
                                           round(self.current_population.average_individual_fitness(), 2), self.current_best.genotype))

        return self.result_list
