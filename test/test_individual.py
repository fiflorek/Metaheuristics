import cvrp_metaheuristics.problem.individual as individual
from cvrp_metaheuristics.problem.individual import Individual


def test_swap():
    lst = [1, 2, 3, 4, 5]
    individual.swap(lst, 1, 3)
    assert lst == [1, 4, 3, 2, 5]


def test_hash():
    genotype_a = [1, 2, 3, 4, 5]
    genotype_b = [1, 2, 3, 4, 5]
    hash_a = hash(tuple(genotype_a))
    hash_b = hash(tuple(genotype_b))
    assert hash_a == hash_b


def test_generate_two_random_indexes():
    for _ in range(100):
        index_a, index_b = individual.generate_two_random_indexes(9)
        assert index_a != index_b
        assert 0 <= index_a <= 9
        assert 0 <= index_b <= 9
        assert index_a < index_b


def test_ordered_cross(mocker):
    mock = mocker.patch('cvrp_metaheuristics.problem.individual.generate_two_random_indexes')
    mock.return_value = (2, 5)

    parent_a = [i for i in range(1, 10)]
    parent_b = [5, 7, 4, 9, 1, 3, 6, 2, 8]
    child = [7, 9, 3, 4, 5, 6, 1, 2, 8]

    assert child == individual.cross_ox(parent_a, parent_b)


def test_pmx_crossover_skip_mapping(mocker):
    mock = mocker.patch('cvrp_metaheuristics.problem.individual.generate_two_random_indexes')
    mock.return_value = (2, 5)

    parent_a = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    parent_b = [5, 7, 4, 9, 1, 3, 6, 2, 8]
    child_a = [5, 2, 4, 3, 1, 6, 7, 8, 9]
    child_b = [1, 7, 3, 9, 5, 4, 6, 2, 8]
    mock.return_value = (2, 5)
    assert (child_b, child_a) == individual.cross_pmx(parent_a, parent_b)


def test_pmx_crossover_full_mapping(mocker):
    mock = mocker.patch('cvrp_metaheuristics.problem.individual.generate_two_random_indexes')
    mock.return_value = (3, 5)

    parent_a = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    parent_b = [4, 3, 1, 2, 8, 7, 5, 6, 9]
    child_a = [1, 4, 3, 2, 8, 7, 6, 5, 9]
    child_b = [2, 3, 1, 4, 5, 6, 8, 7, 9]
    assert (child_b, child_a) == individual.cross_pmx(parent_a, parent_b)


def test_mutate_by_swap(mocker):
    mock = mocker.patch('cvrp_metaheuristics.problem.individual.generate_two_random_indexes')
    mock.return_value = (1, 5)
    genotype = [5, 6, 7, 1, 2, 3, 4]
    mock.return_value = (1, 5)
    individual.mutate_swap(genotype)
    assert genotype == [5, 3, 7, 1, 2, 6, 4]


def test_mutate_by_inversion(mocker):
    mock = mocker.patch('cvrp_metaheuristics.problem.individual.generate_two_random_indexes')
    mock.return_value = (1, 5)
    genotype = [5, 6, 7, 1, 2, 3, 4]
    mock.return_value = (1, 5)
    individual.mutate_inversion(genotype)
    assert genotype == [5, 3, 2, 1, 7, 6, 4]


def test_evaluate(cvrp, mocker):
    mock = mocker.patch('cvrp_metaheuristics.problem.individual.cost')
    mock.return_value = 10.0

    genotype_a = [1, 2, 3, 4, 5]
    genotype_b = [1, 2, 3, 4, 5]
    individual_a = Individual(genotype_a)
    individual_a.evaluate(cvrp)
    individual_b = Individual(genotype_b)
    individual_b.evaluate(cvrp)

    assert individual_a.fitness == 10.0
    assert hash(tuple(genotype_a)) in Individual.fitness_cache
    assert Individual.fitness_cache[hash(tuple(genotype_a))] == 10.0
    assert individual_b.fitness == 10.0
    assert hash(tuple(genotype_b)) in Individual.fitness_cache
    assert Individual.fitness_cache[hash(tuple(genotype_b))] == 10.0
    assert len(Individual.fitness_cache) == 1
