from unittest import TestCase

from cvpr_metaheuristics.problem.cvrp import City, Cvrp


class TestRandomAlgorithm(TestCase):

    def setUp(self):
        cities = [City(i, i * 10, i * 10, i * 5) for i in range(5)]
        self.cvrp = Cvrp(no_of_cities=5, truck_capacity=100, cities=cities, depot_number=0)

    def test_generate_random_solution(self):
        pass
