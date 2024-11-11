import time
from pathlib import Path

import yaml

from algorithm.annealing_algorithm import solve_cvrp_annealing
from algorithm.genetic_algorithm import solve_cvrp_genetic
from algorithm.greedy_algorithm import solve_cvrp_greedy
from algorithm.random_algorithm import solve_cvrp_random
from problem.cvrp import read_problem, Cvrp
from utils.configuration import Config
from utils.enums import Algorithm


# same result for each algorithm -
# each algorithm should be solved_no_of_runs times and the best result should be saved
# best, avg, best_genotype, execution_time, configuration -> save to file results.txt
# best_genotype -> save to file best_run.txt

def solve_problem(cvrp: Cvrp, config: Config) -> None:

    algorithm_mapping = {
        Algorithm.GENETIC: solve_cvrp_genetic,
        Algorithm.RANDOM: solve_cvrp_random,
        Algorithm.GREEDY: solve_cvrp_greedy,
        Algorithm.ANNEALING: solve_cvrp_annealing
    }

    selected_algorithm = algorithm_mapping.get(config.algorithm)

    if selected_algorithm:
        results = []
        start_time = time.time()
        if config.algorithm.is_metaheuristic():
            for i in range(config.no_of_runs):
                results.append(selected_algorithm(cvrp, config))
        else:
            # No need to loop over greedy since its deterministic.
            # Random is not deterministic but let's not waste resources.
            results.append(selected_algorithm(cvrp, config))
        end_time = time.time()
        execution_time = round((end_time - start_time) / config.no_of_runs if config.algorithm.is_metaheuristic() else end_time - start_time, 2)
        save_results_to_file(results, config, execution_time)
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
