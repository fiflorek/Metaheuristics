import random
from typing import Dict

from cvrp_metaheuristics.problem.cvrp import cost, Cvrp
from cvrp_metaheuristics.utils.enums import Crossover, Mutation


class Individual:
    fitness_cache: Dict[int, float] = {}

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


def cross(parent_a: list[int], parent_b: list[int], crossover_type: Crossover) -> tuple[list[int], list[int]]:
    if crossover_type == Crossover.OX:
        return cross_ox(parent_a, parent_b), cross_ox(parent_b, parent_a)
    else:
        return cross_pmx(parent_a, parent_b)


def cross_ox(parent_a: list[int], parent_b: list[int]) -> list[int]:
    """
    Performs an Order Crossover (OX) on two parent genotypes to produce a child genotype.

    The Order Crossover (OX) operator works by selecting a random segment from the first parent
    and preserving the order of the remaining genes from the second parent.

    Args:
        parent_a (list[int]): The first parent genotype.
        parent_b (list[int]): The second parent genotype.

    Returns:
        list[int]: The child genotype resulting from the crossover.
    """
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


def cross_pmx(parent_a: list[int], parent_b: list[int]) -> tuple[list[int], list[int]]:
    """
    Performs a Partially Mapped Crossover (PMX) on two parent genotypes to produce two child genotypes.

    The Partially Mapped Crossover (PMX) operator works by selecting a random segment from the first parent
    and mapping it to the corresponding segment in the second parent. The remaining genes are filled in
    by preserving the order and position from the other parent.

    Args:
        parent_a (list[int]): The first parent genotype.
        parent_b (list[int]): The second parent genotype.

    Returns:
        tuple[list[int], list[int]]: A tuple containing two child genotypes resulting from the crossover.
    """
    swap_index_a, swap_index_b = generate_two_random_indexes(len(parent_a) - 1)
    child_a = parent_b
    child_b = parent_a
    if swap_index_a != 0 and swap_index_b != len(parent_a) - 1:
        cross_map = {}
        for i in range(swap_index_a, swap_index_b + 1):
            # if <3, 4> in map don't add <4, 9> just skip it
            if parent_a[i] not in cross_map and parent_b[i] not in cross_map:
                cross_map[parent_a[i]] = parent_b[i]
                cross_map[parent_b[i]] = parent_a[i]
        for i in range(len(child_a)):
            if child_a[i] in cross_map:
                child_a[i] = cross_map[child_a[i]]
            if child_b[i] in cross_map:
                child_b[i] = cross_map[child_b[i]]
    return child_a, child_b


def mutate(individual: list[int], mutation_type: Mutation) -> list[int]:
    if mutation_type == Mutation.SWAP:
        return mutate_swap(individual)
    else:
        return mutate_inversion(individual)


def mutate_swap(individual: list[int]) -> list[int]:
    """
    Performs a swap mutation on an individual's genotype.

    This mutation selects two random indices in the genotype and swaps their values.

    Args:
        individual (list[int]): The genotype of the individual to be mutated.

    Returns:
        list[int]: The mutated genotype with two values swapped.
    """
    swap_index_a, swap_index_b = generate_two_random_indexes(len(individual) - 1)

    swap(individual, swap_index_a, swap_index_b)

    return individual


def mutate_inversion(individual: list[int]) -> list[int]:
    """
    Performs an inversion mutation on an individual's genotype.

    This mutation selects two random indices in the genotype and reverses the order of the genes between these indices.

    Args:
        individual (list[int]): The genotype of the individual to be mutated.

    Returns:
        list[int]: The mutated genotype with the order of genes between two indices reversed.
    """
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
