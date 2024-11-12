from datetime import datetime
import os
from pathlib import Path

from algorithm.result import Result
from utils.configuration import Config

root_dir = Path(__file__).resolve().parents[2]


def save_results_to_file(result: Result, config: Config, execution_time: float) -> None:
    results_dir = get_or_create_results_dir(config.problem_instance, config.algorithm)
    results_file = results_dir / "results.txt"
    with open(results_file, 'w') as file:
        file.write(f"Best: {result.best}\n")
        file.write(f"Average: {result.average}\n")
        file.write(f"Best genotype: {result.best_genotype}\n")
        file.write(f"Execution time: {execution_time}\n")
        file.write(f"Configuration: {config.__str__()}\n")


# this method saves best run - file is later used to generate a plot
def save_best_run_to_file(best_run: list[tuple[float, float]], config: Config) -> None:
    results_dir = get_or_create_results_dir(config.problem_instance, config.algorithm)
    best_run_file = results_dir / "best_run.txt"

    with open(best_run_file, 'w') as file:
        for generation, (best, avg) in enumerate(best_run):
            file.write(f"{generation}, {best}, {avg}\n")


def get_or_create_results_dir(problem_instance, algorithm):
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = root_dir / "results" / f"{problem_instance}/{algorithm}/{current_time}"
    os.makedirs(output_dir, exist_ok=True)
    return output_dir
