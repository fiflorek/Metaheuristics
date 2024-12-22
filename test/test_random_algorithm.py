import pytest

from cvrp_metaheuristics.algorithm.result import Result
from cvrp_metaheuristics.algorithm.random_algorithm import RandomAlgorithm
from cvrp_metaheuristics.algorithm.config.random_config import RandomConfig


@pytest.fixture
def random_config():
    return RandomConfig(**{"algorith": "random", "problem_instance": "toy", "no_of_solutions": 100})


def test_solve_random(cvrp, random_config):
    result = RandomAlgorithm(cvrp, random_config).solve()
    assert all(isinstance(r, Result) for r in result)
    assert len(result) == 1
    assert len(result[0].best_genotype) == cvrp.no_of_cities - 1
    assert result[0].best > 0
    assert result[0].average > 0
