import pytest

from cvrp_metaheuristics.algorithm.result import Result
from cvrp_metaheuristics.algorithm.config.genetic_config import GeneticConfig
from cvrp_metaheuristics.algorithm.genetic_algorithm import GeneticAlgorithm
from cvrp_metaheuristics.problem.individual import Individual


@pytest.fixture
def genetic_config():
    return GeneticConfig(**{
        "problem_instance": "toy",
        "no_of_runs": 1,
        "algorithm": "genetic",
        "population_size": 10,
        "generations": 50,
        "init_type": "greedy",
        "crossover_probability": 0.6,
        "crossover_type": "ox",
        "mutation_probability": 0.2,
        "mutation_type": "inversion",
        "tournament_size": 6
    })


@pytest.fixture
def genetic_algorithm(cvrp, genetic_config):
    return GeneticAlgorithm(cvrp, genetic_config)


def test_init_greedy_population(genetic_algorithm):
    genetic_algorithm.initialize_population()
    assert len(genetic_algorithm.current_population.population) == genetic_algorithm.population_size
    assert all(isinstance(ind, Individual) for ind in genetic_algorithm.current_population.population)
    # greedy init so all should be the same
    assert len({individual.fitness for individual in genetic_algorithm.current_population.population}) == 1


def test_selection(genetic_algorithm):
    selected = genetic_algorithm.selection(genetic_algorithm.current_population.population)
    assert isinstance(selected, Individual)
    assert selected in genetic_algorithm.current_population.population


def test_solve_genetic_algorithm(genetic_algorithm):
    results = genetic_algorithm.solve()
    assert len(results) == genetic_algorithm.generations
    assert all(isinstance(r, Result) for r in results)
