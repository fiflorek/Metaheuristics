from cvrp_metaheuristics.algorithm.config.configuration import Config


class RandomConfig(Config):
    """
    Configuration for Random Algorithm.

        Parameters:
            no_of_solutions: int -> Number of solutions to generate
    """
    _no_of_solutions: int

    def __init__(self, config_dict):
        super().__init__(config_dict)
        self._no_of_solutions = config_dict.get("no_of_solutions", 100)

    @property
    def no_of_solutions(self) -> int:
        return self._no_of_solutions

    def __str__(self):
        return super().__str__() + f"Number of solutions: {self.no_of_solutions}\n"
