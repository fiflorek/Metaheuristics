from abc import abstractmethod, ABC

from cvrp_metaheuristics.algorithm.result import Result
from cvrp_metaheuristics.problem.cvrp import Cvrp
from cvrp_metaheuristics.utils.configuration import Config
from cvrp_metaheuristics.utils.enums import Crossover, Initialization


class Algorithm(ABC):
    """Base class for algorithms."""
    _cvrp: Cvrp
    _config: Config
    _result_list: list[Result]

    def __init__(self, cvrp: Cvrp, config: Config) -> None:
        self._cvrp = cvrp
        self._config = config
        self._result_list = []
        self._initialize_algorithm()

    @property
    def cvrp(self) -> Cvrp:
        return self._cvrp

    @property
    def no_of_cities(self) -> int:
        return self.cvrp.no_of_cities

    @property
    def population_size(self) -> int:
        return self.config.population_size

    @property
    def generations(self) -> int:
        return self.config.generations

    @property
    def distances_matrix(self) -> list[list[float]]:
        return self.cvrp.distances_matrix

    @property
    def config(self) -> Config:
        return self._config

    @property
    def depot_number(self) -> int:
        return self.cvrp.depot_number

    @property
    def crossover_type(self) -> Crossover:
        return self.config.crossover_type

    @property
    def init_type(self) -> Initialization:
        return self.config.init_type

    @property
    def result_list(self) -> list[Result]:
        return self._result_list

    @abstractmethod
    def _initialize_algorithm(self) -> None:
        """Initializes the algorithm. """
        ...

    @abstractmethod
    def solve(self) -> list[Result]:
        """Solves the CVRP problem."""
        ...
