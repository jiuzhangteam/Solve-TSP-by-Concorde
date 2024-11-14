# -*- coding:utf-8 -*-

from concorde.tsp import TSPSolver
from concorde.tests.data_utils import get_dataset_path
import pandas as pd
import numpy as np
from data.data import Data
from solution import Solution

class PyConcorde:
    """
    A class to solve the Traveling Salesman Problem (TSP) using the Concorde library.
    """

    def __init__(self, data: Data):
        """
        Initialize the PyConcorde class with data.

        Args:
        data (Data): An instance of the Data class containing node information and distances.
        """
        self.data = data
        self.route = []
        self.dis = 0

    def create_tsp_file(self, file_path, dist_matrix):
        """
        Create a TSP file from a distance matrix.

        Args:
        file_path (str): The path where the TSP file will be saved.
        dist_matrix (numpy.array): The distance matrix representing the TSP problem.
        """
        with open(f"{file_path}.tsp", 'w') as f:
            n = len(dist_matrix)
            f.write("NAME: temp\n")
            f.write("TYPE: TSP\n")
            f.write(f"DIMENSION: {n}\n")
            f.write("EDGE_WEIGHT_TYPE: EXPLICIT\n")
            f.write("EDGE_WEIGHT_FORMAT: FULL_MATRIX\n")
            f.write("EDGE_WEIGHT_SECTION\n")
            for row in dist_matrix:
                f.write(" ".join(str(int(dist)) for dist in row) + "\n")
            f.write("EOF\n")

    def solve(self):
        """
        Solve the TSP problem using the Concorde solver and calculate the total distance.
        """
        # Create a fixed distance matrix excluding the depot node
        fix_matrix = []
        node_lst = list(self.data.node_dic.keys())
        node_lst.remove('depot')  # Assuming 'depot' is the key for the depot node
        for node1 in node_lst:
            lst = []
            for node2 in node_lst:
                lst.append(self.data.distance[node1, node2])
            fix_matrix.append(lst)
        fix_matrix = np.array(fix_matrix)

        # Create the TSP file and solve the problem
        self.create_tsp_file("tsp_data", fix_matrix)
        solver = TSPSolver.from_tspfile("tsp_data.tsp")
        solution = solver.solve(verbose=False)

        # Print solution details
        print("feasibility:", solution.found_tour)
        print("best value:", solution.optimal_value)
        print("solution:", solution.tour)

        # Extract the route and calculate the total distance
        self.route = [node_lst[index] for index in solution.tour]
        print("route:", self.route)

        # Adjust the route to start from the 'start' node
        position = self.route.index('start')
        self.route = self.route[position:] + self.route[:position]
        print("adjusted route:", self.route)

        self.dis = sum(self.data.distance[self.route[i], self.route[i + 1]] for i in range(len(self.route) - 1))
        self.dis += self.data.distance[self.route[-1], self.route[0]]

def start():
    """
    The main function to start the TSP solving process.
    """
    data = Data()
    data.read_json()
    data.read_order()
    data.add_depot()
    data.calculate_distance()
    p = PyConcorde(data)
    p.solve()
    print("total_distance:", p.dis)
    task = {
        'route': p.route + ["end"],
        'distance': p.dis,
        'vehicle_id': data.vehicle_list[0].vehicleId
    }
    s = Solution(data, [p.route], [task])
    s.visualize()
    result = s.write_file()

if __name__ == '__main__':
    start()

