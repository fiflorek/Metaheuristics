from abc import abstractmethod, ABC

from src.algorithm.result import Result
from src.problem.cvrp import Cvrp
from algorithm.config.configuration import Config
from utils.enums import Crossover, Initialization


class Algorithm(ABC):
    """Base class for algorithms."""
    _cvrp: Cvrp  # problem that the algorithm is trying to solve
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
    def distances_matrix(self) -> list[list[int]]:
        return self.cvrp.distances_matrix

    @property
    def config(self) -> Config:
        return self._config

    @property
    def depot_number(self) -> int:
        return self.cvrp.depot_number

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
