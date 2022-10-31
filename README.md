### The Ripple-Spreading Algorithm for Many-to-Many the *k* Shortest Path Problem

##### Reference: Hu X B, Zhang C, Zhang G P, et al. Finding the k shortest paths by ripple-spreading algorithms[J]. Engineering Applications of Artificial Intelligence, 2020, 87: 103229.

| Variables     | Meaning                                                      |
| ------------- | ------------------------------------------------------------ |
| network       | Dictionary, {node 1: {node 2: [weight 1, weight 2, ...], ...}, ...} |
| new_network   | The inversed network                                         |
| source        | List, the source nodes                                       |
| destination   | List, the destination nodes                                  |
| k             | The *k* shortest paths                                       |
| nn            | The number of nodes                                          |
| neighbor      | Dictionary, {node1: [the neighbor nodes of node1], ...}      |
| v             | The ripple-spreading speed (i.e., the minimum length of arcs) |
| t             | The simulated time index                                     |
| nr            | The number of ripples - 1                                    |
| epicenter_set | List, the epicenter node of the i-th ripple is epicenter_set[i] |
| path_set      | List, the path of the i-th ripple from the source node to node i is path_set[i] |
| radius_set    | List, the radius of the i-th ripple is radius_set[i]         |
| active_set    | List, active_set contains all active ripples                 |
| objective_set | List, the objective value of the traveling path of the i-th ripple is objective_set[i] |
| omega         | Dictionary, omega[n] contains all ripples generated at node n |

#### Example

![](https://github.com/Xavier-MaYiMing/The-ripple-spreading-algorithm-for-the-many-to-many-k-shortest-paths-problem/blob/main/many-to-many%20k%20shortest%20paths%20problem.png)

The source nodes are 0 and 1, and the destination nodes are 10 and 11. The aim is to determine the three shortest paths from every source node to destination nodes.

```python
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
```

##### Output:

```python
{
    0: [
        {'path': [0, 3, 5, 8, 11], 'length': 11}, 
        {'path': [0, 2, 5, 8, 11], 'length': 14}, 
        {'path': [0, 2, 7, 10], 'length': 15},
    ], 
    1: [
        {'path': [1, 3, 5, 8, 11], 'length': 10}, 
        {'path': [1, 3, 5, 7, 10], 'length': 14}, 
        {'path': [1, 3, 5, 8, 10], 'length': 14},
    ]
}
```

The shortest paths from node 0 are 0->3->5->8->11, 0->2->5->8->11, and 0->2->7->10.

The shortest paths from node 1 are 1->3->5->8->11, 1->3->5->7->11, and 1->3->5->8->10.
