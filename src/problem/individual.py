import random

from problem.cvrp import cost, Cvrp


class Individual:
    fitness_cache = {}

    def __init__(self, genotype: list[int], fitness=0.0):
        self.genotype = genotype
        self.fitness = fitness

    def evaluate(self, cvrp: 'Cvrp') -> None:
        genotype_hash = hash(tuple(self.genotype))
        if genotype_hash in Individual.fitness_cache:
            self.fitness = Individual.fitness_cache[genotype_hash]
        else:
            self.fitness = cost(cvrp, self.genotype)
            Individual.fitness_cache[genotype_hash] = self.fitness


def cross(parent_a: list[int], parent_b: list[int]) -> list[int]:
    child = [0 for _ in range(len(parent_a))]
    swap_index_a, swap_index_b = generate_two_random_indexes(len(parent_a) - 1)
    assigned_genes = set()
    for i in range(swap_index_a, swap_index_b + 1):
        child[i] = parent_a[i]
        assigned_genes.add(parent_a[i])
    remaining_genes = [gene for gene in parent_b if gene not in assigned_genes]
    tmp = 0
    for i in range(len(child)):
        if child[i] == 0:
            child[i] = remaining_genes[tmp]
            tmp += 1
    return child


def mutate(individual: list[int], mutation_type: str) -> list[int]:
    if mutation_type == 'swap':
        return mutate_by_swap(individual)
    else:
        return mutate_by_inversion(individual)


def mutate_by_swap(individual: list[int]) -> list[int]:
    swap_index_a, swap_index_b = generate_two_random_indexes(len(individual) - 1)

    swap(individual, swap_index_a, swap_index_b)

    return individual


def mutate_by_inversion(individual: list[int]) -> list[int]:
    swap_index_a, swap_index_b = generate_two_random_indexes(len(individual) - 1)

    while swap_index_a < swap_index_b:
        swap(individual, swap_index_a, swap_index_b)
        swap_index_a += 1
        swap_index_b -= 1

    return individual


def generate_two_random_indexes(x: int) -> tuple[int, int]:
    swap_index_a = random.randint(0, x)
    swap_index_b = swap_index_a
    while swap_index_a == swap_index_b:
        swap_index_b = random.randint(0, x)
    if swap_index_a < swap_index_b:
        return swap_index_a, swap_index_b
    else:
        return swap_index_b, swap_index_a


def swap(lst, a, b):
    tmp = lst[a]
    lst[a] = lst[b]
    lst[b] = tmp
