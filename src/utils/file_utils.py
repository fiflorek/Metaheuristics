from datetime import datetime
import os
from pathlib import Path

from algorithm.result import Result
from utils.configuration import Config

root_dir = Path(__file__).resolve().parents[2]


def save_results_to_file(results: list[Result], config: Config, execution_time: float):
    results_dir = get_or_create_results_dir(config.problem_instance, config.algorithm)
    results_file = results_dir / "results.txt"
    with open(results_file, 'w') as file:
        file.write(f"Best: {results.best}\n")
        file.write(f"Average: {results.average}\n")
        file.write(f"Best genotype: {results.best_genotype}\n")
        file.write(f"Configuration: {config}\n")


def save_to_file(ga_run, config, global_results):
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M")
    output_dir = Path(__file__).parent.parent.parent / f"{config['problem_instance']}/{current_time}"
    os.makedirs(output_dir, exist_ok=True)
    output_file_path = output_dir / "best_run.txt"
    with open(output_file_path, 'w') as file:
        for generation, data in ga_run.items():
            file.write(f"{generation}, {data['best']}, {data['avg']}\n")
    with open(output_dir / "results.txt", 'w') as file:
        file.write(f"Best: {global_results['best']}\n")
        file.write(f"Average: {global_results['avg']}\n")
        file.write(f"Execution time: {global_results['execution_time']}\n")
        file.write(f"Best genotype: {global_results['best_genotype']}\n")


def get_or_create_results_dir(problem_instance, algorithm):
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M")
    output_dir = root_dir / f"{problem_instance}/{algorithm}/{current_time}"
    os.makedirs(output_dir, exist_ok=True)
    return output_dir
