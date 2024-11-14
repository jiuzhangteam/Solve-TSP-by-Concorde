# -*- coding:utf-8 -*-

import pandas as pd
import random
from haversine import haversine
import numpy as np
from data.order import Order
from data.depot import Depot
from data.vehicle import Vehicle

class Data:
    """
    A class to represent the data for the TSP problem, including orders, vehicles, and depot information.
    """

    def __init__(self):
        """
        Initialize the Data class with empty attributes.
        """
        self.vehicleNum = 1
        self.order_list = []
        self.vehicle_list = []
        self.order_dic = {}
        self.customer_orders = {}
        self.weight_dic = {}
        self.cubic_dic = {}
        self.node_dic = {}
        self.distance = {}
        self.vehicle_dic = {}
        self.customer_tasks = {}

    def read_json(self, data=None):
        """
        Read JSON data from a file or a given data object.

        Args:
        data (dict): The JSON data to read. If None, it reads from a file.
        """
        if data:
            self.data = data
        else:
            import json
            # Load JSON data from a file
            with open('input.json', 'r', encoding='utf-8') as f:
                self.data = json.load(f)

        self.customerNum = len(self.data['orders'])
        vehicleNum = len(self.data['vehicles'])
        print("Order quantity:", self.customerNum)
        print("Vehicle quantity:", vehicleNum)

    def read_order(self):
        """
        Read order information from the JSON data and create Order objects.
        """
        self.config = self.data['dispatchId']
        for order_data in self.data['orders']:
            order = Order(
                order_data['orderNo'],
                order_data['cubic'],
                order_data['weight'],
                (float(order_data['lonLat'].split(',')[1]),
                 float(order_data['lonLat'].split(',')[0])),
                order_data['addressNo'],
                order_data['taskNo']
            )
            self.order_list.append(order)

        self.depot = Depot(
            self.data['depots'][0]['address'],
            self.data['depots'][0]['deName'],
            self.data['depots'][0]['province'],
            self.data['depots'][0]['city'],
            self.data['depots'][0]['addressNo'],
            self.data['depots'][0]['district'],
            self.data['depots'][0]['deCode'],
            (float(self.data['depots'][0]['lonLat'].split(',')[1]),
             float(self.data['depots'][0]['lonLat'].split(',')[0]))
        )

        for vehicle_data in self.data['vehicles']:
            vehicle = Vehicle(
                vehicle_data['dispatchZoneCode'],
                vehicle_data['vehicleId'],
                vehicle_data['maxWeight'],
                vehicle_data['maxVolume']
            )
            self.vehicle_list.append(vehicle)
            self.vehicle_dic[vehicle.vehicleId] = (vehicle.maxVolume, vehicle.dispatchZoneCode)

        # Create dictionaries for order and customer information
        for order in self.order_list:
            self.order_dic[order.addressNo] = order.lonLat
            self.customer_orders[order.addressNo] = ';'.join([o.orderNo for o in self.order_list if o.addressNo == order.addressNo])
            self.customer_tasks[order.addressNo] = ';'.join([o.taskNo for o in self.order_list if o.addressNo == order.addressNo])

        # Calculate total weight and cubic
        total_weight = sum(order.weight for order in self.order_list)
        total_cubic = sum(order.cubic for order in self.order_list)
        print("Total weight:", total_weight)
        print("Total cubic:", total_cubic)

    def calculate_distance(self):
        """
        Calculate the distances between all nodes (orders and depot) using the haversine formula.
        """
        for key1, value1 in self.node_dic.items():
            for key2, value2 in self.node_dic.items():
                if key1 != key2:
                    self.distance[(key1, key2)] = haversine(value1, value2)

        # Update distances with values from the JSON data if available
        for key1, value1 in self.order_dic.items():
            for key2, value2 in self.order_dic.items():
                if key1 != key2:
                    for dis in self.data['matrix']:
                        if (dis['fromAddressNo'] == key1 and dis['toAddressNo'] == key2) or (
                                dis['fromAddressNo'] == key2 and dis['toAddressNo'] == key1):
                            self.distance[(key1, key2)] = dis['distance']

        # Set distances to and from the depot
        for key, value in self.order_dic.items():
            self.distance[('start', key)] = self.distance[(key, 'start')] = self.data['matrix'][0]['distance']

        # Set return to start distances to 0
        for key in self.node_dic.keys():
            self.distance[(key, 'end')] = self.distance[('end', key)] = 0

        # Check for missing distances
        for key1, value1 in self.order_dic.items():
            if (key1, 'end') not in self.distance or self.distance[(key1, 'end')] == 10000:
                print(f"{key1} and 'end' distance not found")

    def add_depot(self):
        """
        Add the depot node to the node dictionary.
        """
        self.node_dic['start'] = self.depot.lonLat
        self.node_dic['end'] = self.depot.lonLat
        print("Node dictionary length after adding depot:", len(self.node_dic))


if __name__ == '__main__':
    data = Data()
    data.read_json()
    data.read_order()
    data.add_depot()
    data.calculate_distance()