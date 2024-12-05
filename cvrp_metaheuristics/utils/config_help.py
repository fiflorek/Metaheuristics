import argparse

from cvrp_metaheuristics.algorithm.config.random_config import RandomConfig
from cvrp_metaheuristics.algorithm.config.tabu_config import TabuSearchConfig
from cvrp_metaheuristics.algorithm.config.genetic_config import GeneticConfig
from cvrp_metaheuristics.utils import enums


def configure_arg_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog="cvrp_metaheuristics",
        description="This program solves Capacitated Vehicle Routing Problem using metaheuristic algorithms",
        epilog=f"""
        The default configuration file resides in `config/config.yaml`
        The file contains examples of configurations for various algorithms.
        The configuration file accepts two basic parameters: `problem_instance` and `algorithm`.
        Available instances of the CVRP problem can be found in `resources/data_set` folder.
        Currently supported algorithms are: {', '.join(enums.AlgorithmName.__members__.keys())}
        {prepare_description()}
        """
    )
    parser.add_argument("-c", "--config", default="config/config.yaml",
                        help="Path to the configuration file, relative to the project root folder", type=str)
    return parser


def prepare_description():
    description = "Additionally the following algorithms accept specific parameters, described below:\n"
    for algorithm in enums.AlgorithmName:
        match algorithm:
            case enums.AlgorithmName.RANDOM:
                description += RandomConfig.__doc__
            case enums.AlgorithmName.GENETIC:
                description += GeneticConfig.__doc__
            case enums.AlgorithmName.TABU_SEARCH:
                description += TabuSearchConfig.__doc__

    return description
