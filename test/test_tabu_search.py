import pytest

from cvrp_metaheuristics.algorithm.result import Result
from cvrp_metaheuristics.algorithm.tabu_search import TabuSearch
from cvrp_metaheuristics.algorithm.config.tabu_config import TabuSearchConfig
from cvrp_metaheuristics.problem.individual import Individual


@pytest.fixture
def genetic_config():
    return TabuSearchConfig({
        "problem_instance": "toy",
        "no_of_runs": 1,
        "algorithm": "tabu_search",
        "generations": 10,
        "init_type": "greedy",
        "neighbourhood_size": 50,
        "tabu_list_size": 10,
        "mutation_type": "swap",
    })


@pytest.fixture
def tabu_search(cvrp, genetic_config):
    return TabuSearch(cvrp, genetic_config)


def test_search_neighbourhood(tabu_search):
    neighbourhood = tabu_search.search_neighbourhood()
    assert len(neighbourhood) == tabu_search.neighbourhood_size
    assert all(isinstance(n, Individual) for n in neighbourhood)
    assert all(n.genotype != tabu_search.current_best for n in neighbourhood)


def test_find_best_not_in_tabu(tabu_search):
    neighbours = tabu_search.search_neighbourhood()
    best_neighbour = tabu_search.best_neighbour_not_in_tabu(neighbours)
    assert best_neighbour is not None
    assert best_neighbour not in tabu_search.tabu_set


def test_solve_tabu_search(tabu_search):
    results = tabu_search.solve()
    assert len(results) == tabu_search.generations
    assert all(isinstance(r, Result) for r in results)
