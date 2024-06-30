import numpy as np


class Ant:
    def __init__(self, distance_mat, alpha, beta):
        self.distance_mat = distance_mat
        self.alpha = alpha
        self.beta = beta
        self.visited = [0]
        self.total_distance = 0

    def move(self, pheromone, alpha, beta, test=False):
        # calculate the probabilities to choose a node
        norm_row = self.calcProbabilities(pheromone, alpha, beta)
        next_index = norm_row.argmax()  # get the one with highest probability
        if not test:  # if the ant is exploring
            next_index = np.random.choice(range(len(norm_row)), 1, p=norm_row)[0]
        self.go(next_index)  # go to the selected node

    def go(self, next_index):
        pre = self.visited[-1]
        self.total_distance += self.distance_mat[pre][next_index]
        self.visited.append(next_index)

    def calcProbabilities(self, pheromone, alpha, beta):
        cur_index = self.visited[-1]

        distance_row = self.distance_mat[cur_index]
        pheromone_row = np.copy(pheromone[cur_index])
        pheromone_row[self.visited] = 0  # avoid selecting the visited nodes

        row = pheromone_row**alpha * ((1.0 / distance_row) ** beta)
        return row / row.sum()
