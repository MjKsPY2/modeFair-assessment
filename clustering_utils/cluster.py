import numpy as np


class Cluster:
    def __init__(self, start_index, all_nodes):
        self.all_nodes = all_nodes
        # Initialize array to hold cluster node indices
        self.node_indices = [start_index]
        # Initialize the cluster weight to be the weight of current node
        self.weight = all_nodes[start_index][2]

    def addNode(self, index):
        self.node_indices.append(index)  # Add to cluster node indices
        self.weight += self.all_nodes[index][2]  # Add the weight of the node

    def getCenter(self):
        if len(self.node_indices) <= 0:  # if the cluster is empty
            return None
        # Return center
        return np.sum(self.all_nodes[self.node_indices, :2], axis=0) / len(self.node_indices)

    def removeNode(self, index):
        self.node_indices.remove(index)  # Remove the node from this cluster
        # Reduce cluster weight by the weight of the node
        self.weight -= self.allnodes[index][2]
