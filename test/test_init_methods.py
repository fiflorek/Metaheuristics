from cvrp_metaheuristics.utils.init_methods import init_random_genotype


def test_init_random_genotype(cvrp):
    random_genotype = init_random_genotype(cvrp)
    assert len(set(random_genotype)) == cvrp.no_of_cities - 1
    # depot is 0, so we do not take that into account
    for i in range(1, cvrp.no_of_cities):
        assert i in random_genotype


def test_if_genotypes_are_unique(cvrp):
    genotypes = []
    for i in range(100):
        genotypes.append(init_random_genotype(cvrp))
    unique_genotypes = [g for g in genotypes if genotypes.count(g) == 1]
    assert len(unique_genotypes) > 1
