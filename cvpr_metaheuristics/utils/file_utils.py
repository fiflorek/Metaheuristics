from datetime import datetime
import os
from pathlib import Path

from cvpr_metaheuristics.algorithm.result import Result
from cvpr_metaheuristics.problem.cvrp import Cvrp, City
from cvpr_metaheuristics.utils.configuration import Config
from cvpr_metaheuristics.utils.enums import DataFileConstants as DFC

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
    output_dir = root_dir / "results" / f"{problem_instance}/{algorithm.name}/{current_time}"
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def read_problem(file_path: Path) -> Cvrp:
    no_of_cities = 0
    truck_capacity = 0
    city_coordinates = []
    city_demand = []
    depot_number = 0
    with open(file_path, "r") as file:
        for line in file:
            if DFC.DIMENSION.value in line:
                no_of_cities = int(line.split(':')[1].strip())
            elif DFC.CAPACITY.value in line:
                truck_capacity = int(line.split(':')[1].strip())
            elif DFC.NODE_COORD_SECTION.value in line:
                for i in range(0, no_of_cities):
                    line = file.readline()
                    city_coordinates.append(line.strip().split(" "))
            elif DFC.DEMAND_SECTION.value in line:
                for i in range(0, no_of_cities):
                    line = file.readline()
                    city_demand.append(line.strip().split(" "))
            elif DFC.DEPOT_SECTION.value in line:
                depot_number = int(file.readline().strip())

    cities = []
    for i in range(0, no_of_cities):
        number = int(city_coordinates[i][0].strip())
        x = int(city_coordinates[i][1].strip())
        y = int(city_coordinates[i][2].strip())
        demand = int(city_demand[i][1].strip())
        city = City(number - 1, x, y, demand)  # - 1 to adjust that arrays start from 0
        cities.append(city)

    return Cvrp(no_of_cities, truck_capacity, cities, depot_number - 1)  # - 1 to adjust that arrays start from 0
