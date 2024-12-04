from cvrp_metaheuristics.problem.cvrp import City, distance, cost
import pytest


@pytest.mark.parametrize("city_a, city_b, expected_distance", [
    (City(city_number=0, x=0, y=0, demand=0), City(city_number=1, x=0, y=3, demand=0), 3.0),
    (City(city_number=0, x=0, y=0, demand=0), City(city_number=2, x=4, y=0, demand=0), 4.0),
    (City(city_number=0, x=1, y=1, demand=0), City(city_number=3, x=4, y=5, demand=0), 5.0)
])
def test_distance(city_a, city_b, expected_distance):
    assert distance(city_a, city_b) == expected_distance


def test_cost(cvrp):
    genotype = [3, 1, 2, 5, 4]
    total = cost(cvrp, genotype)
    assert total == 278.01
