# Metaheuristics

## Description
This repository is a Python project that solves the **Capacitated Vehicle Routing Problem (CVRP)** using various metaheuristic algorithms.
The CVRP is an NP-hard problem, which is why metaheuristics are used to solve it.
The problem consists of `n` locations and a symmetrical matrix of distances between these locations.
The goal is to find the shortest route that visits all locations exactly once.
Additionally, each location has a specific demand for goods that must be delivered in one trip (i.e., you cannot revisit a location to deliver the remaining goods).
The goods are delivered on a truck that has a defined capacity. The truck can visit a special location - warehouse - to refill the goods.
For more details please visit: http://vrp.galgos.inf.puc-rio.br/index.php/en/

## Configuration
The program is configured using the `config.yaml` file. This allows user to use different algorithms and parameters to try to solve the problem.
Currently, three algorithms/metaheuristics are supported: "greedy", "random", and "genetic".
Here are example configuration parameters:
```yaml
problem_instance: "A-n32-k5"
no_of_runs: 10
algorithm: "genetic"
population_size: 100
generations: 500
crossover_probability: 0.6
mutation_probability: 0.2
mutation_type: 'swap'
tournament_size: 6
```
___
```yaml
problem_instance: "A-n32-k5"
no_of_runs: 1
algorithm: "random"
population_size: 10
generations: 50
```
___
```yaml
problem_instance: "A-n32-k5"
no_of_runs: 1
algorithm: "greedy"
```


## Setup and Run
1. Clone the repository  
`git clone git@github.com:fiflorek/Metaheuristics.git`
2. Create virtual environment  
`python3 -m venv venv`  
`source venv/bin/activate`
3. Install requirements  
`pip install -r requirements.txt`
4. Configure algorithm parameters in config.yaml
5. Run the tests  
`python -m unittest discover -s test`
6. Run the program  
`python src/metaheuristics.py`
The results are saved in the "results" directory relative to where the script is run from.

## Algorithms
### Greedy
The Greedy algorithm is a simple and deterministic approach. It works by always selecting the next closest city to visit. This method produces a suboptimal solution, but sometimes because of its implementation simplicity it can produce "good enough" results.
The algorithm may also be used as a starting point for more complex ones (i.e., Genetic Algorithm).
### Random
As the name suggests the Random algorithm generates a random sequence of cities to visit and evaluates it. It is often used as a starting point to metaheuristic algorithms. 
In this program the number of solutions generated equals `population_size * generations`.
### Genetic Algorithm
TODO: Add description
### Simulated Annealing
Not implemented yet
### Tabu Search
Not implemented yet