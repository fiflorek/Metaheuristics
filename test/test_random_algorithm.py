from unittest import TestCase

from src.problem.cvrp import City, Cvrp


class TestRandomAlgorithm(TestCase):

    def setUp(self):
        cities = [City(i, i * 10, i * 10, i * 5) for i in range(5)]
        self.cvrp = Cvrp(no_of_cities=5, truck_capacity=100, cities=cities, depot_number=0)

    def test_generate_random_solution(self):
        solution = generate_random_solution(self.cvrp)
        self.assertEqual(len(solution), self.cvrp.no_of_cities - 1)
        self.assertTrue(all(city_id in solution for city_id in range(1, self.cvrp.no_of_cities)))