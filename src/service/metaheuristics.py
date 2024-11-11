import sys
import time
from pathlib import Path

import yaml

from algorithm.annealing_algorithm import solve_cvrp_annealing
from algorithm.genetic_algorithm import solve_cvrp_genetic
from algorithm.greedy_algorithm import solve_cvrp_greedy
from algorithm.random_algorithm import solve_cvrp_random
from algorithm.result import Result
from problem.cvrp import read_problem, Cvrp
from utils.configuration import Config
from utils.enums import Algorithm
from utils.file_utils import save_results_to_file, save_best_run_to_file


def solve_problem(cvrp: Cvrp, config: Config) -> None:
    algorithm_mapping = {
        Algorithm.GENETIC: solve_cvrp_genetic,
        Algorithm.RANDOM: solve_cvrp_random,
        Algorithm.GREEDY: solve_cvrp_greedy,
        Algorithm.ANNEALING: solve_cvrp_annealing
    }

    selected_algorithm = algorithm_mapping.get(config.algorithm)

    if selected_algorithm:
        start_time = time.time()
        if config.algorithm.is_metaheuristic():
            global_best = sys.maxsize
            global_avg = 0
            global_best_genotype = []
            global_best_run = []
            for i in range(config.no_of_runs):
                run_i = selected_algorithm(cvrp, config)
                for generation, run_i in run_i.items():
                    if run_i.best < global_best:
                        global_best = run_i.best
                        global_best_genotype = run_i.best_genotype
                        global_best_run = run_i
                    global_avg += run_i.average
            global_result = Result(global_best, global_avg, global_best_genotype)
            end_time = time.time()
            avg_execution_time = round((end_time - start_time) / config.no_of_runs, 2)

            # As of now, best run saves only generation number, avg and best values.
            # It disregards the best genotype of each generation - but it might be used in the future
            best_run_data = [(generation_result.best, generation_result.average) for generation_result in global_best_run.values()]

            save_best_run_to_file(best_run_data, config)
            save_results_to_file(global_result, config, avg_execution_time)
        else:
            # No need to loop over greedy since its deterministic.
            # Random is not deterministic but let's not waste resources.
            result = selected_algorithm(cvrp, config)
            end_time = time.time()
            avg_execution_time = round(end_time - start_time, 2)
            save_results_to_file(result, config, avg_execution_time)
    else:
        print(f"Algorithm {config.algorithm} not found")
        return


def main():
    root_dir = Path(__file__).resolve().parents[2]
    config_file_path = root_dir / "config/config.yaml"
    data_set_dir = root_dir / "resources/data_set/A"

    with open(config_file_path, 'r') as file:
        config = Config(yaml.safe_load(file))

    cvrp = read_problem(data_set_dir / f'{config.problem_instance}.vrp')

    solve_problem(cvrp, config)


# def solve_problem():
#     root_dir = Path(__file__).resolve().parents[2]
#     config_file_path = root_dir / "config/config.yaml"
#     data_set_dir = root_dir / "resources/data_set/A"
#
#     with open(config_file_path, 'r') as file:
#         config = yaml.safe_load(file)
#
#     cvrp = read_problem(data_set_dir / f'{config["problem_instance"]}.vrp')
#
#     no_of_individuals = config["population_size"] * config["generations"] * config["no_of_runs"]
#
#     results = {}
#
#     available_algorithms = {
#         Algorithm.GENETIC.value: solve_cvrp_genetic,
#         Algorithm.RANDOM.value: solve_cvrp_random,
#         Algorithm.GREEDY.value: solve_cvrp_greedy,
#         Algorithm.ANNEALING.value: solve_cvrp_annealing
#     }
#
#     selected_algorithm = available_algorithms.get(config["algorithm"])
#     if selected_algorithm:
#         selected_algorithm(cvrp, config)
#     else:
#         print(f"Algorithm {config['algorithm']} not found")
#         return
#
#     if config["algorithm"] == 'genetic':
#         best = sys.maxsize
#         best_run_index = 0
#         avg = 0
#         best_genotype = []
#         execution_time = 0
#         ga_runs = []
#         for i in range(config["no_of_runs"]):
#             start_time = time.time()
#             ga_run = solve_cvrp_genetic(cvrp, config)
#             for result in ga_run:
#                 if ga_run[result]["best"] < best:
#                     best = ga_run[result]["best"]
#                     best_genotype = ga_run[result]["best_genotype"]
#                     best_run_index = i
#                 avg += ga_run[result]["avg"]
#
#             end_time = time.time()
#             execution_time += round(end_time - start_time, 2)
#             ga_runs.append(ga_run)
#             print(f"Run {i + 1} completed")
#
#         results = {"best": best, "avg": round(avg / (config["no_of_runs"] * config["generations"]), 2),
#                    "best_genotype": best_genotype, "execution_time": round(execution_time / config["no_of_runs"], 2)}
#         save_to_file(ga_runs[best_run_index], config, results)
#     elif config["algorithm"] == 'random':
#         start_time = time.time()
#         results = solve_cvrp_random(cvrp, no_of_individuals)
#         end_time = time.time()
#         results["execution_time"] = round(end_time - start_time, 2)
#     elif config["algorithm"] == 'greedy':
#         start_time = time.time()
#         results = solve_cvrp_greedy(cvrp)
#         end_time = time.time()
#         results["execution_time"] = round(end_time - start_time, 2)
#
#     print(results)


if __name__ == '__main__':
    main()
