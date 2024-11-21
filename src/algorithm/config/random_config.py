from algorithm.config.configuration import Config


class RandomConfig(Config):
    _no_of_solutions: int

    def __init__(self, config_dict):
        super().__init__(config_dict)
        self._no_of_solutions = config_dict.get("no_of_solutions", 100)

    @property
    def no_of_solutions(self) -> int:
        return self._no_of_solutions
