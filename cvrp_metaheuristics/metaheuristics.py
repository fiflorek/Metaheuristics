import argparse
import sys
import time
from pathlib import Path
from typing import Dict, Type

import yaml

from cvrp_metaheuristics.algorithm.config.configuration import Config
from cvrp_metaheuristics.algorithm.config.genetic_config import GeneticConfig
from cvrp_metaheuristics.algorithm.config.random_config import RandomConfig
from cvrp_metaheuristics.algorithm.config.tabu_config import TabuSearchConfig
from cvrp_metaheuristics.algorithm.genetic_algorithm import GeneticAlgorithm
from cvrp_metaheuristics.algorithm.greedy_algorithm import GreedyAlgorithm
from cvrp_metaheuristics.algorithm.random_algorithm import RandomAlgorithm
from cvrp_metaheuristics.algorithm.result import Result
from cvrp_metaheuristics.algorithm.tabu_search import TabuSearch
from cvrp_metaheuristics.problem.cvrp import Cvrp
from cvrp_metaheuristics.utils.enums import AlgorithmName
from cvrp_metaheuristics.utils.file_utils import save_results_to_file, save_best_run_to_file, read_problem


def solve_problem(cvrp: Cvrp, config) -> None:
    algorithm_mapping: Dict[AlgorithmName, Type[GeneticAlgorithm | RandomAlgorithm | GreedyAlgorithm | TabuSearch]] = {
        AlgorithmName.GENETIC: GeneticAlgorithm,
        AlgorithmName.RANDOM: RandomAlgorithm,
        AlgorithmName.GREEDY: GreedyAlgorithm,
        AlgorithmName.TABU_SEARCH: TabuSearch,
    }

    selected_algorithm = algorithm_mapping.get(config.algorithm, GreedyAlgorithm)
    solve = selected_algorithm(cvrp, config).solve

    if selected_algorithm:
        start_time = time.time()
        if config.algorithm.is_metaheuristic():
            global_best = sys.float_info.max
            global_avg = 0.0
            global_best_genotype: list[int] = []
            global_best_run: list[Result] = []
            for i in range(config.no_of_runs):
                run_i = solve()
                for generation in run_i:
                    if generation.best < global_best:
                        global_best = generation.best
                        global_best_genotype = generation.best_genotype
                        global_best_run = run_i
                    global_avg += generation.average
            global_avg /= (config.no_of_runs * config.generations)
            global_result = Result(global_best, round(global_avg, 2), global_best_genotype)
            end_time = time.time()
            avg_execution_time = round((end_time - start_time) / config.no_of_runs, 2)

            # As of now, best run saves only generation number, avg and best values.
            # It disregards the best genotype of each generation - but it might be used in the future
            best_run_data = [(generation_result.best, generation_result.average) for generation_result in
                             global_best_run]

            save_best_run_to_file(best_run_data, config)
            save_results_to_file(global_result, config, avg_execution_time)
        else:
            # No need to loop over greedy since its deterministic.
            # Random is not deterministic but let's not waste resources.
            result = solve()[0]
            end_time = time.time()
            avg_execution_time = round(end_time - start_time, 2)
            save_results_to_file(result, config, avg_execution_time)
    else:
        print(f"Algorithm {config.algorithm} not found")
        return


def main():
    parser = argparse.ArgumentParser(
        prog="cvrp_metaheuristics",
        description="This program solves Capacitated Vehicle Routing Problem using metaheuristic algorithms",
        epilog="The default configuration file resides in config/config.yaml "
               "The file contains examples of configurations for various algorithms."
    )
    parser.add_argument("-c", "--config", default="config/config.yaml", help="Path to the configuration file", type=str)
    args = parser.parse_args()
    root_dir = Path(__file__).resolve().parent.parent
    config_file_path = root_dir / "config/config.yaml"
    data_set_dir = root_dir / "resources/data_set/A"

    with open(config_file_path, 'r') as file:
        configuration = yaml.safe_load(file)

    config_mapping = {
        AlgorithmName.GENETIC: GeneticConfig,
        AlgorithmName.RANDOM: RandomConfig,
        AlgorithmName.TABU_SEARCH: TabuSearchConfig,
        AlgorithmName.GREEDY: Config
    }

    config_class = config_mapping.get(AlgorithmName(configuration.get("algorithm", "greedy")))
    config = config_class(configuration)

    cvrp = read_problem(data_set_dir / f'{config.problem_instance}.vrp')

    solve_problem(cvrp, config)


if __name__ == '__main__':
    main()
