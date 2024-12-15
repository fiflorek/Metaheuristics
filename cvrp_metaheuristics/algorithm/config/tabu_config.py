from cvrp_metaheuristics.algorithm.config.configuration import Config
from cvrp_metaheuristics.utils.enums import Mutation, Initialization


class TabuSearchConfig(Config):
    """
    Configuration for Tabu Search Algorithm.
    
    Parameters:
    no_of_runs: int -> How many times should the algorithm be run
    generations: int -> Number of generations (within one run of the algorithm)
    init_type: Initialization -> Type of initialization, currently supported are: greedy, random
    neighbourhood_size: int -> Number of neighbours to visit in each generation.Neighbour is defined as 'one muatation away' from the current solution
    tabu_list_size: int -> Size of the tabu list. Purpose of the tabu list is to prevent the algorithm from looping through the same neighbourhoods
    mutation_type: Mutation -> Type of mutation, currently supported are: swap, inversion
    """

    _no_of_runs: int
    _init_type: Initialization
    _generations: int
    _neighbourhood_size: int
    _tabu_list_size: int
    _mutation_type: Mutation

    def __init__(self, config_dict):
        super().__init__(config_dict)
        self._no_of_runs = config_dict.get("no_of_runs", 1)
        self._init_type = Initialization(config_dict.get("init_type", "random"))
        self._neighbourhood_size = config_dict.get("neighbourhood_size", 100)
        self._tabu_list_size = config_dict.get("tabu_list_size", 50)
        self._mutation_type = Mutation(config_dict.get("mutation_type", "swap"))
        self._generations = config_dict.get("generations", 10)

    @property
    def no_of_runs(self) -> int:
        return self._no_of_runs

    @property
    def init_type(self) -> Initialization:
        return self._init_type

    @property
    def neighbourhood_size(self) -> int:
        return self._neighbourhood_size

    @property
    def tabu_list_size(self) -> int:
        return self._tabu_list_size

    @property
    def mutation_type(self) -> Mutation:
        return self._mutation_type

    @property
    def generations(self) -> int:
        return self._generations

    def __str__(self):
        return super().__str__() + f"Neighbourhood size: {self.neighbourhood_size}\n" \
                                   f"Tabu list size: {self.tabu_list_size}\n" \
                                   f"Mutation type: {self.mutation_type}\n" \
                                   f"Generations: {self.generations}\n" \
                                   f"Initialization type: {self.init_type}\n" \
                                   f"Number of runs: {self.no_of_runs}\n"
