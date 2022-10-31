#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/31 18:45
# @Author  : Xavier Ma
# @Email   : xavier_mayiming@163.com
# @File    : RSA4m2mkSPP.py
# @Statement : The ripple-spreading algorithm for the many-to-many k shortest paths problem
def find_neighbor(network):
    """
    Find the neighbor of each node
    :param network:
    :return: {node 1: [the neighbor nodes of node 1], ...}
    """
    nn = len(network)
    neighbor = []
    for i in range(nn):
        neighbor.append(list(network[i].keys()))
    return neighbor


def find_speed(network, neighbor):
    """
    Find the ripple-spreading speed
    :param network:
    :param neighbor:
    :return:
    """
    speed = 1e10
    for i in range(len(network)):
        for j in neighbor[i]:
            speed = min(speed, network[i][j])
    return speed


def main(network, source, destination, k):
    """
    The ripple-spreading algorithm for the shortest path problem
    :param network: {node1: {node2: length, node3: length, ...}, ...}
    :param source: the source node set
    :param destination: the destination node set
    :param k: the k shortest paths
    :return:
    """
    # Step 1. Initialization
    nn = len(network)  # node number
    new_network = {}  # reverse the network
    for i in range(nn):
        new_network[i] = {}
    for i in range(nn):
        for j in network[i].keys():
            new_network[j][i] = network[i][j]
    neighbor = find_neighbor(new_network)  # the neighbor set
    v = find_speed(new_network, neighbor)  # the ripple-spreading speed
    t = 0  # simulated time index
    nr = 0  # the current number of ripples - 1
    epicenter_set = []  # epicenter set
    radius_set = []  # radius set
    length_set = []  # length set
    path_set = []  # path set
    active_set = []  # the set containing all active ripples
    omega = {}  # the set that records the ripple generated at each node
    for node in range(nn):
        omega[node] = []

    # Step 2. Initialize the first ripples
    for node in destination:
        epicenter_set.append(node)
        radius_set.append(0)
        length_set.append(0)
        path_set.append([node])
        active_set.append(nr)
        omega[node].append(nr)
        nr += 1

    # Step 3. The main loop
    while True:
        # Step 3.1. Termination judgment
        flag = True
        for node in source:
            if len(omega[node]) < k:  # the source node has not been visited k times
                flag = False
                break
        if flag:
            break

        # Step 3.2. Time updates
        t += 1
        incoming_ripples = {}  # the incoming ripples to each node in this period

        for ripple in active_set:

            # Step 3.3. Active ripples spread out
            radius_set[ripple] += v

            # Step 3.4. New incoming ripples
            epicenter = epicenter_set[ripple]
            path = path_set[ripple]
            radius = radius_set[ripple]
            length = length_set[ripple]
            for node in neighbor[epicenter]:
                if len(omega[node]) < k and node not in path:  # the node has been visited no more than k times
                    temp_length = new_network[epicenter][node]
                    if temp_length <= radius < temp_length + v:
                        temp_path = path.copy()
                        temp_path.append(node)
                        if node in incoming_ripples.keys():
                            incoming_ripples[node].append({
                                'path': temp_path,
                                'radius': radius - temp_length,
                                'length': length + temp_length,
                            })
                        else:
                              incoming_ripples[node] = [{
                                  'path': temp_path,
                                  'radius': radius - temp_length,
                                  'length': length + temp_length,
                              }]

        # Step 3.5. Generate new ripples
        for node in incoming_ripples.keys():
            new_ripples = sorted(incoming_ripples[node], key=lambda x: x['radius'], reverse=True)
            if len(omega[node]) + len(new_ripples) > k:
                new_ripples = new_ripples[: k - len(omega[node])]
            for item in new_ripples:
                path_set.append(item['path'])
                epicenter_set.append(node)
                radius_set.append(item['radius'])
                length_set.append(item['length'])
                active_set.append(nr)
                omega[node].append(nr)
                nr += 1

        # Step 3.6. Active -> inactive
        remove_ripple = []
        for ripple in active_set:
            epicenter = epicenter_set[ripple]
            radius = radius_set[ripple]
            flag_inactive = True
            for node in neighbor[epicenter]:
                if radius < new_network[epicenter][node] and len(omega[node]) < k:
                    flag_inactive = False
                    break
            if flag_inactive:
                remove_ripple.append(ripple)
        for ripple in remove_ripple:
            active_set.remove(ripple)

    # Step 4. Sort the results
    result = {}
    for node in source:
        result[node] = []
        for ripple in omega[node]:
            path_set[ripple].reverse()
            result[node].append({
                'path': path_set[ripple],
                'length': length_set[ripple],
            })
    return result


if __name__ == '__main__':
    network = {
        0: {1: 6, 2: 7, 3: 4},
        1: {0: 6, 3: 3, 4: 7},
        2: {0: 7, 5: 2, 7: 5},
        3: {0: 4, 1: 3, 5: 2, 6: 9},
        4: {1: 7, 6: 7, 9: 9},
        5: {2: 2, 3: 2, 7: 6, 8: 4},
        6: {3: 9, 4: 7, 8: 7, 9: 4},
        7: {2: 5, 5: 6, 10: 3},
        8: {5: 4, 6: 7, 10: 5, 11: 1},
        9: {4: 9, 6: 4, 11: 7},
        10: {7: 3, 8: 5, 11: 7},
        11: {8: 1, 9: 7, 10: 7}
    }
    source = [0, 1]
    destination = [10, 11]
    k = 3
    print(main(network, source, destination, k))
