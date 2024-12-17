import numpy as np

np.random.seed(0)

num_cities = 10
num_ants = 20
alpha = 1.0
beta = 5.0
rho = 0.5
initial_pheromone = 0.1
num_iterations = 100

cities = np.random.rand(num_cities, 2)

def calculate_distance_matrix(cities):
    num_cities = len(cities)
    distance_matrix = np.zeros((num_cities, num_cities))
    for i in range(num_cities):
        for j in range(i + 1, num_cities):
            distance = np.linalg.norm(cities[i] - cities[j])
            distance_matrix[i][j] = distance
            distance_matrix[j][i] = distance
    return distance_matrix

distance_matrix = calculate_distance_matrix(cities)

pheromone = np.ones((num_cities, num_cities)) * initial_pheromone

def select_next_city(probabilities):
    return np.random.choice(len(probabilities), p=probabilities)

def calculate_probabilities(ant_path, pheromone, distance_matrix, alpha, beta):
    current_city = ant_path[-1]
    probabilities = np.zeros(len(distance_matrix))

    for city in range(len(distance_matrix)):
        if city not in ant_path:
            probabilities[city] = (pheromone[current_city][city] ** alpha) * ((1.0 / distance_matrix[current_city][city]) ** beta)
    probabilities /= probabilities.sum()
    return probabilities

def construct_solution(pheromone, distance_matrix, alpha, beta):
    solution = []
    for _ in range(num_ants):
        ant_path = [np.random.randint(num_cities)]
        while len(ant_path) < num_cities:
            probabilities = calculate_probabilities(ant_path, pheromone, distance_matrix, alpha, beta)
            next_city = select_next_city(probabilities)
            ant_path.append(next_city)
        solution.append(ant_path + [ant_path[0]])
    return solution

def update_pheromones(pheromone, solutions, distance_matrix, rho):
    pheromone *= (1 - rho)
    for solution in solutions:
        path_length = sum(distance_matrix[solution[i], solution[i+1]] for i in range(len(solution) - 1))
        pheromone_delta = 1.0 / path_length
        for i in range(len(solution) - 1):
            pheromone[solution[i]][solution[i + 1]] += pheromone_delta
            pheromone[solution[i + 1]][solution[i]] += pheromone_delta
    return pheromone

best_solution = None
best_path_length = float('inf')

for iteration in range(num_iterations):
    solutions = construct_solution(pheromone, distance_matrix, alpha, beta)
    pheromone = update_pheromones(pheromone, solutions, distance_matrix, rho)

    for solution in solutions:
        path_length = sum(distance_matrix[solution[i], solution[i + 1]] for i in range(len(solution) - 1))
        if path_length < best_path_length:
            best_path_length = path_length
            best_solution = solution

    print(f"Iteration {iteration + 1}:  Path length = {best_path_length}")

    if iteration > 0 and best_path_length == previous_best_path_length:
        print(f"Convergence reached at iteration {iteration + 1}. Best solution found.")
        break

    previous_best_path_length = best_path_length

print("\nBest solution found:", best_solution)
print("Shortest path length:", best_path_length)
