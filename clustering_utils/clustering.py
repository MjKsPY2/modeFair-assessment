import numpy as np
from .cluster import Cluster
from utils.utils import getEuclideanDistance


class Clustering:
    def __init__(self, max_capacity, nodes):
        self.max_capacity = max_capacity  # max capacity of a cluster
        self.nodes = nodes
        self.clusters = self.initClusters()  # Initialize clusters

        # Improve the clusters by n_clusters iterations
        self.improveClusters(len(self.clusters))

    def initClusters(self):
        unclustered = [i for i in range(len(self.nodes))]  # Unclustered nodes
        clusters = [Cluster(unclustered.pop(), self.nodes)]  # Initialize clusters
        while len(unclustered) > 0:  # While there is still unclustered node
            cluster = clusters[-1]  # get current cluster
            center = cluster.getCenter()  # get the center of the current cluster
            distances = [
                getEuclideanDistance(center, self.nodes[index, :2])
                for index in unclustered
            ]  # get the distances from all of the nodes to the center

            min_index = np.argmin(distances)  # get the closet node
            node = self.nodes[unclustered[min_index]]

            # if the cluster still have enough capacity
            if (cluster.weight + node[2] <= self.max_capacity):
                # add the node into the cluster
                cluster.addNode(unclustered[min_index])
            else:
                # add into a new cluster
                clusters.append(Cluster(unclustered[min_index], self.nodes))
            # remove the node from unclustered list
            unclustered.remove(unclustered[min_index])
        return clusters

    def improveClusters(self, n_iters):
        for _ in range(n_iters):

            # For every nodes
            for cur_cluster in self.clusters:
                cur_center = cur_cluster.getCenter()
                for i in cur_cluster.node_indices:
                    node = self.nodes[i]

                    # Calculate its distance to its current cluster's center
                    cur_distance = getEuclideanDistance(cur_center, node[:2])

                    for cluster in self.clusters:  # For all the other clusters
                        if (
                            cluster != cur_cluster
                            and cluster.weight + node[2] <= self.max_capacity
                        ):  # if the cluster still has enough capacity
                            center = cluster.getCenter()
                            distance = getEuclideanDistance(center, node[:2])

                            # if the node is closer to new cluster
                            if (distance < cur_distance):
                                # remove the node from its current cluster
                                cur_cluster.removeNode(i)
                                # add the node to the new cluster
                                cluster.addNode(node)
