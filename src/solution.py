# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt
from data.data import Data
import json
import os

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ""))
parent_path = os.path.dirname(root_path)


class Solution:
    """
    A class to represent a solution to the TSP problem, including visualization and output generation.
    """

    def __init__(self, data: Data, routes, tasks):
        """
        Initialize the Solution class.

        Args:
        data (Data): An instance of the Data class containing node information and distances.
        routes (list): A list of routes, where each route is a list of node IDs.
        tasks (list): A list of tasks, where each task is a dictionary containing route and vehicle information.
        """
        self.data = data
        self.m = 0
        self.routes = routes
        self.routeNum = len(routes)
        self.tasks = tasks

    def visualize(self):
        """
        Visualize the solution using matplotlib.
        """
        print("\n\n==============Drawing the Graph==============")
        plt.figure(0)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title("Solution")
        plt.scatter(self.data.node_dic['start'][0], self.data.node_dic['start'][1], c='blue', alpha=1, marker=',',
                    linewidths=3, label='depot')
        for i in self.data.order_dic.keys():
            plt.scatter(self.data.node_dic[i][0], self.data.node_dic[i][1], c='black', alpha=1, marker='o', s=15,
                        linewidths=3)

        # Define colors for each route
        colors = ['red', 'green', 'cyan', 'magenta', 'yellow', 'black', 'purple', 'orange', 'brown', 'pink']

        # Plot each route
        for k in range(self.routeNum):
            color = colors[k % len(colors)]
            for i in range(len(self.routes[k]) - 1):
                a = self.routes[k][i]
                b = self.routes[k][i + 1]
                x = [self.data.node_dic[a][0], self.data.node_dic[b][0]]
                y = [self.data.node_dic[a][1], self.data.node_dic[b][1]]
                plt.plot(x, y, color, linewidth=2)

        plt.grid(False)
        plt.legend(loc='upper right')
        plt.savefig(f"{parent_path}/output/" + self.data.config + ".png", bbox_inches='tight')
        plt.show(block=False)

    def write_file(self):
        """
        Write the solution to a JSON file.
        """
        result = {}
        lst = []
        ind = 1
        for task in self.tasks:
            task['route'].pop()  # Remove 'end'
            task['route'].pop(0)  # Remove 'start'
            p = "start"
            way = "BIL000" + str(ind)
            for index, orderid in enumerate(task['route']):
                cor_string = ','.join(str(element) for element in self.data.order_dic[orderid][::-1])
                lst.append({
                    "dispatchZoneId": self.data.vehicle_dic[task["vehicle_id"]][1],
                    "waybillNo": way,
                    "vehicleId": task["vehicle_id"],
                    "seq": index + 1,
                    "lonLat": cor_string,
                    "addressNo": orderid,
                    "eta": "-",
                    "etd": "-",
                    "distance": self.data.distance[p, orderid],
                    "orderNo": self.data.customer_orders[orderid],
                    "taskNo": self.data.customer_tasks[orderid]
                })
                p = orderid
            ind += 1

        result["dispatchId"] = self.data.config
        result["dispatch"] = lst
        final = {"code": 0, "result": result}

        # Write the result to a JSON file
        with open(f"{parent_path}/output/output_" + self.data.config + '.json', 'w', encoding='utf-8') as file:
            json.dump(final, file, ensure_ascii=False, indent=4)
        return final