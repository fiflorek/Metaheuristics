import random

from algorithm.result import Result
from problem import individual
from problem.cvrp import Cvrp
from problem.individual import Individual
from utils.configuration import Config


class Population:

    def __init__(self, population: list[Individual]):
        self.population = population

    def best_individual(self):
        return min(self.population, key=lambda ind: ind.fitness)

    def average_individual(self):
        return round(sum([ind.fitness for ind in self.population]) / len(self.population), 2)

    def worst_individual(self):
        return max(self.population, key=lambda ind: ind.fitness)

    def evaluate(self, cvrp):
        for ind in self.population:
            ind.evaluate(cvrp)


def initialize(population_size: int, cvrp):
    population = []
    for _ in range(population_size):
        genotype = list(range(1, cvrp.no_of_cities))
        random.shuffle(genotype)
        population.append(Individual(genotype))

    return Population(population)


def selection(tournament_size: int, population: list[Individual]):
    tournament = []
    for i in range(tournament_size):
        tournament.append(population[random.randint(0, len(population) - 1)])

    return min(tournament, key=lambda ind: ind.fitness)


def solve_cvrp_genetic(cvrp: Cvrp, config: Config) -> list[Result]:
    results = []  # for each population save the best, average and best_genotype
    population = initialize(config.population_size, cvrp)
    population.evaluate(cvrp)
    best = population.best_individual()
    results[0] = Result(best.fitness, population.average_individual(), best.genotype)

    for i in range(1, config.generations):
        new_population = []
        for j in range(config.population_size):
            parent_a = selection(config.tournament_size, population.population)
            parent_b = selection(config.tournament_size, population.population)
            child_genotype = parent_a.genotype[:]
            if random.random() < config.crossover_probability:
                child_genotype = individual.cross(parent_a.genotype, parent_b.genotype)
            if random.random() < config.mutation_probability:
                child_genotype = individual.mutate(child_genotype, config.mutation_type)
            new_population.append(Individual(child_genotype))
        population = Population(new_population)
        population.evaluate(cvrp)
        best = population.best_individual()
        results.append(Result(best.fitness, population.average_individual(), best.genotype))

    return results
