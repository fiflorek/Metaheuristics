import math
from dataclasses import dataclass


@dataclass(frozen=True)
class City:
    city_number: int
    x: int
    y: int
    demand: int


class Cvrp:

    def __init__(self, no_of_cities: int, truck_capacity: int, cities: list[City], depot_number: int):
        self.no_of_cities = no_of_cities
        self.truck_capacity = truck_capacity
        self.cities = cities
        self.depot_number = depot_number
        self.distances_matrix = self._init_distances_matrix()

    def _init_distances_matrix(self) -> list[list[float]]:
        matrix = [[0.0 for _ in range(self.no_of_cities)] for _ in range(self.no_of_cities)]
        for i, row in enumerate(matrix):
            for j, element in enumerate(row):
                matrix[i][j] = distance(self.cities[i], self.cities[j])
        return matrix

    def print_distances_matrix(self) -> None:
        for i, row in enumerate(self.distances_matrix):
            for j, element in enumerate(row):
                print(self.distances_matrix[i][j], end=' ')
            print()

    def __str__(self):
        print(
            f"CVRP(no_of_cities={self.no_of_cities},"
            f" truck_capacity={self.truck_capacity},"
            f" depot_number={self.depot_number})")


def distance(city_a: City, city_b: City) -> float:
    return math.sqrt((city_a.x - city_b.x) ** 2 + (city_a.y - city_b.y) ** 2)


#  TO DO: when truck is i.e. 80% empty - maybe then turn back instead of going to depot only when its empty
# I would like to make a check, if let's say truck has enough capacity for only one more city:
# is it better to go back now and refill later, or go to the next city and then go back to depot
# which basically is checking if city_a -> depot -> city_b < depot -> city_a -> city_b

def cost(cvrp: Cvrp, route: list[int]) -> float:
    """
    Calculates the total cost of a given route for the CVRP problem.

    The cost is calculated based on the distances between cities and the truck's capacity.
    If the truck's capacity is insufficient to visit the next city, it returns to the depot to refill.

    Args:
        cvrp (Cvrp): The CVRP problem instance containing cities, distances, and truck capacity.
        route (list[int]): A list of city numbers representing the route to be evaluated.

    Returns:
        float: The total cost of the route.
    """
    # first step is from depot to first city
    depot_city_number = cvrp.depot_number
    first_city = cvrp.cities[route[0]]
    last_city = cvrp.cities[route[len(route) - 1]]
    route_cost = cvrp.distances_matrix[depot_city_number][first_city.city_number]
    current_truck_capacity = cvrp.truck_capacity - first_city.demand
    for i in range(1, len(route)):
        current_city_number = cvrp.cities[route[i - 1]].city_number
        next_city = cvrp.cities[route[i]]
        if current_truck_capacity < next_city.demand:
            # go back to depot and refill the truck
            route_cost += cvrp.distances_matrix[depot_city_number][current_city_number]
            current_truck_capacity = cvrp.truck_capacity
            current_city_number = depot_city_number
        route_cost += cvrp.distances_matrix[current_city_number][next_city.city_number]
        current_truck_capacity -= next_city.demand
    route_cost += cvrp.distances_matrix[depot_city_number][last_city.city_number]
    return route_cost
