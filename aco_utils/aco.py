import numpy as np
from .ant import Ant


class ACO:
    def __init__(self, n_ants, distance_mat, decay=0.97, alpha=1, beta=1):
        self.n_ants = n_ants
        self.distance_mat = distance_mat
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        self.pheromone = []
        self.best_route = []
        self.shortest_distance = np.inf

    def fit(self, n_iters):
        n_nodes = len(self.distance_mat)
        # Initialize pheromone
        self.pheromone = (np.ones(self.distance_mat.shape) / n_nodes)

        for _ in range(n_iters):
            ants = [
                Ant(self.distance_mat, self.alpha, self.beta)
                for _ in range(self.n_ants)
            ]  # Initialize ants
            for i in range(n_nodes):  # Let all ants to explore all nodes
                for ant in ants:
                    if i != n_nodes - 1:  # if there is still unexplored node
                        # Move based on pheromone and distance
                        ant.move(self.pheromone, self.alpha, self.beta)
                    else:  # Back to depot
                        ant.go(0)
                        # Record the best_route
                        if ant.total_distance < self.shortest_distance:
                            self.shortest_distance = ant.total_distance
                            self.best_route = ant.visited
            # spread the pheromone along the path of all ants
            self.spreadPheromone(ants)
            self.pheromone *= self.decay  # pheromone evaporates

    def spreadPheromone(self, ants):
        for ant in ants:  # for every ant
            path = ant.visited
            for i in range(len(path) - 1):
                # spread the pheromone on the path
                self.pheromone[path[i]][path[i + 1]
                                        ] += (1.0 / ant.total_distance)
