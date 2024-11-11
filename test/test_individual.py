from unittest import TestCase
from unittest.mock import patch
from problem import individual
from problem.individual import Individual


class TestIndividual(TestCase):

    @patch('individual.generate_two_random_indexes')
    def test_ordered_cross(self, mock):
        parent_a = [i for i in range(1, 10)]
        parent_b = [5, 7, 4, 9, 1, 3, 6, 2, 8]
        child = [7, 9, 3, 4, 5, 6, 1, 2, 8]
        mock.return_value = (2, 5)

        self.assertEqual(child, individual.cross(parent_a, parent_b))

    @patch('individual.generate_two_random_indexes')
    def test_mutate_by_swap(self, mock):
        genotype = [5, 6, 7, 1, 2, 3, 4]
        mock.return_value = (1, 5)
        individual.mutate_by_swap(genotype)

        self.assertEqual(genotype, [5, 3, 7, 1, 2, 6, 4])

    @patch('individual.generate_two_random_indexes')
    def test_mutate_by_inversion(self, mock):
        genotype = [5, 6, 7, 1, 2, 3, 4]
        mock.return_value = (1, 5)
        individual.mutate_by_inversion(genotype)

        self.assertEqual(genotype, [5, 3, 2, 1, 7, 6, 4])

    def test_generate_two_random_indexes(self):
        for _ in range(100):
            index_a, index_b = individual.generate_two_random_indexes(9)
            self.assertNotEqual(index_a, index_b)
            self.assertTrue(0 <= index_a <= 9)
            self.assertTrue(0 <= index_b <= 9)
            self.assertLess(index_a, index_b)

    def test_swap(self):
        lst = [1, 2, 3, 4, 5]
        individual.swap(lst, 1, 3)
        self.assertEqual(lst, [1, 4, 3, 2, 5])

    @patch('individual.cost')
    def test_evaluate(self, mock):
        cvrp = object()
        mock.return_value = 10.0

        genotype_a = [1, 2, 3, 4, 5]
        genotype_b = [1, 2, 3, 4, 5]

        individual_a = Individual(genotype_a)
        individual_a.evaluate(cvrp)

        individual_b = Individual(genotype_b)
        individual_b.evaluate(cvrp)

        self.assertEqual(individual_a.fitness, 10.0)
        self.assertIn(hash(tuple(genotype_a)), Individual.fitness_cache)
        self.assertEqual(Individual.fitness_cache[hash(tuple(genotype_a))], 10.0)

        self.assertEqual(individual_b.fitness, 10.0)
        self.assertIn(hash(tuple(genotype_b)), Individual.fitness_cache)
        self.assertEqual(Individual.fitness_cache[hash(tuple(genotype_b))], 10.0)

        self.assertEqual(1, len(Individual.fitness_cache))

    def test_hash(self):
        genotype_a = [1, 2, 3, 4, 5]
        genotype_b = [1, 2, 3, 4, 5]
        hash_a = hash(tuple(genotype_a))
        hash_b = hash(tuple(genotype_b))

        self.assertEqual(hash_a, hash_b)