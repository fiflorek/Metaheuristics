import pytest

from cvrp_metaheuristics.algorithm.result import Result
from cvrp_metaheuristics.algorithm.greedy_algorithm import GreedyAlgorithm
from cvrp_metaheuristics.algorithm.config.configuration import Config


@pytest.fixture
def greedy_config():
    return Config({"algorith": "random", "problem_instance": "toy"})


@pytest.fixture
def greedy(cvrp, greedy_config):
    return GreedyAlgorithm(cvrp, greedy_config)


def test_solve_greedy(greedy):
    result = greedy.solve()
    assert all(isinstance(r, Result) for r in result)
    assert len(result) == 1
    assert len(result[0].best_genotype) == greedy.cvrp.no_of_cities - 1
    assert result[0].best > 0
    assert result[0].average > 0


def test_results_are_deterministic(greedy):
    results = [greedy.solve()[0].best for _ in range(10)]
    assert len(set(results)) == 1


# results based on toy instance
def test_find_nearest_not_visited(greedy):
    # after init only depot is visited
    assert greedy.find_nearest_city_not_yet_visited() == 3
    greedy.visit_city(3, 1)
    assert greedy.find_nearest_city_not_yet_visited() == 1
    greedy.visit_city(1, 2)
    assert greedy.find_nearest_city_not_yet_visited() == 2
    greedy.visit_city(2, 3)
    assert greedy.find_nearest_city_not_yet_visited() == 5
    greedy.visit_city(5, 4)
    assert greedy.find_nearest_city_not_yet_visited() == 4
    greedy.visit_city(4, 5)
