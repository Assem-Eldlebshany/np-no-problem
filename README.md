# np-no-problem

## How to Run
### Install Dependencies

After cloning the repository, navigate to the project directory in your terminal and run the following command to install the required dependencies:

```bash
pip install -r requirements.txt
```

# Graph Drawing Contest

This repository contains a solution to the Graph Drawing Contest, where the goal was to minimize edge crossings in a 2D graph layout. The graph is represented using a set of vertices and edges, provided in a JSON file. The challenge was to rearrange the graph layout such that the number of edge crossings is minimized while preserving the graph's structure.

## Project Overview

The project uses multiple algorithms to take in a graph's **vertices** and **edges** as input in JSON format, then generates an optimized layout with the minimum number of edge crossings. The output is a new JSON file with updated vertex coordinates.

## Input Format

The input file should be in JSON format, containing two primary components:

- **vertices**: A list of vertices, each with an `id` and initial `x`, `y` coordinates.
- **edges**: A list of edges, each defined by a `source` and `target` referencing the vertex `id`. 
- The input is provided in JSON format with the following structure:

```json
{
  "nodes": [
    {"id": 1, "x": 0, "y": 0},
    {"id": 2, "x": 1, "y": 1},
    {"id": 3, "x": 2, "y": 0}
  ],
  "edges": [
    {"source": 1, "target": 2},
    {"source": 2, "target": 3},
    {"source": 3, "target": 1}
  ]
}
```
## Techniques Used

The following techniques were implemented to optimize the graph layout and minimize edge crossings:

### 1. Kamada-Kawai Layout

A force-directed layout algorithm that minimizes the energy of the system, where nodes are treated as connected by springs. The goal of the Kamada-Kawai algorithm is to position nodes in a way that reflects the pairwise distances between them, while also minimizing edge crossings in the layout. It computes node positions by considering the graph as a spring system where the optimal positions of nodes minimize the total spring energy.

### 2. Simulated Annealing

An optimization algorithm that attempts to minimize the number of edge crossings by adjusting node positions iteratively based on temperature-controlled random movements. The algorithm works by exploring different configurations and gradually reducing the "temperature" to allow smaller changes as the system approaches an optimal layout. This method can efficiently search for the optimal placement of nodes by balancing exploration of different configurations with a steady reduction in randomness.

### 3. Spring Layout

A classical physics-based algorithm where nodes repel each other, and edges act like springs, pulling nodes together, resulting in a balanced layout. In this method, the forces applied to the nodes are computed iteratively to achieve a configuration where nodes are spaced apart without overlap, and the edges between them are as evenly distributed as possible. This technique is widely used for visualizing graph structures in a way that is easy to interpret.

