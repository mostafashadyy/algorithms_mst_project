# Miscellaneous Networks - Minimum Spanning Tree (MST) Algorithms

## Overview

In this mini-project, we explore the concept of **Minimum Spanning Trees (MST)** by applying five different MST algorithms to a selected set of **Miscellaneous Networks** from the [Network Repository](https://networkrepository.com/misc.php). These networks represent various real-world problems and can range in size from small to very large, making them ideal for demonstrating the scalability and performance of the algorithms.

### Selected Network Category: Miscellaneous Networks

The **Miscellaneous Networks** category consists of a broad range of networks that don't fit neatly into traditional categories such as social, communication, or transportation networks. These networks come from various real-world domains and can have diverse structures and applications. By analyzing these networks and applying MST algorithms, we can demonstrate the effectiveness of different algorithms in various contexts, ranging from large-scale communication networks to e-commerce platforms.

Below are the datasets chosen from the **Miscellaneous Networks** category, each with its own set of applications:

#### 1. **USAir97**
   - **Link**: [USAir97 Dataset](https://networkrepository.com/USAir97.php)
   - **Description**: The USAir97 network represents a network of flights between major airports in the United States, showing the connectivity between these airports.
   - **Applications**: 
     - **Airline Route Optimization**: Used to optimize flight routes between cities, reducing travel time or fuel consumption.
     - **Transportation Logistics**: Helps in improving the overall logistics in the transportation industry by visualizing and optimizing airline connectivity.
     - **Network Design and Analysis**: Useful in the field of communication and network design for optimizing the routing of data across connected hubs.

#### 2. **G13**
   - **Link**: [G13 Dataset](https://networkrepository.com/G13.php)
   - **Description**: G13 is a graph representing the network of 13 major international airports, each linked by flight routes.
   - **Applications**: 
     - **Global Airline Connectivity**: Used to analyze the structure and efficiency of air transport between major international hubs.
     - **Travel Planning**: Helps in evaluating the most cost-effective flight paths and optimizing travel itineraries for passengers and cargo.
     - **Disaster Recovery Planning**: Analyzes the resilience of global airport networks and their response to disruptions.

#### 3. **Trefethen‑2000**
   - **Link**: [Trefethen‑2000 Dataset](https://networkrepository.com/Trefethen_2000.php)
   - **Description**: This graph represents a benchmark scientific network named after Lloyd N. Trefethen's influential 2000 work. While not representing real-world connectivity (like social or transportation networks), it's typically used for testing algorithms—especially spectral and numerical methods—on medium-sized synthetically generated graphs.
   - **Applications**: 
     - **Numerical & Spectral Method Testing**: Serves as a controllable benchmark for evaluating the performance of eigenvalue solvers, spectral clustering, and embedding methods in computational linear algebra.
     - **Benchmarking Algorithm Efficiency**: Used to measure runtime, convergence, and accuracy of matrix decomposition and graph signal processing techniques.
     - **Educational Value**: Helps students and researchers in numerical analysis and graph theory to understand the interplay between graph structure, eigen-spectra, and algorithmic stability.

#### 4. **LHR04C**
   - **Link**: [LHR04C Dataset](https://networkrepository.com/lhr04c.php)
   - **Description**: The LHR04C network represents the connectivity of various companies within a business ecosystem, such as financial institutions, suppliers, and customers.
   - **Applications**: 
     - **Business Network Analysis**: Used to study the relationships between companies and suppliers, helping in business development and supply chain optimization.
     - **Financial Risk Assessment**: Can be used for analyzing financial risk based on the interconnections between financial institutions and understanding the impact of a financial collapse in a network.
     - **Market Analysis**: Helps in understanding market dynamics and identifying the key players or institutions that drive the economy.

#### 5. **Amazon0302**
   - **Link**: [Amazon0302 Dataset](https://networkrepository.com/amazon0302.php)
   - **Description**: The Amazon-2008 network represents the co-purchase network of products from Amazon, where nodes represent products and edges represent products that are often bought together.
   - **Applications**: 
     - **Recommendation Systems**: Used for designing recommendation algorithms in e-commerce platforms, helping recommend products to users based on previous purchase patterns.
     - **Market Basket Analysis**: Analyzes patterns in consumer purchasing behavior to improve sales strategies and targeted marketing efforts.
     - **Supply Chain Optimization**: Helps in managing inventory by identifying frequently co-purchased products, allowing for better stock management.

### Applications of Miscellaneous Networks

The networks in this category represent a range of domains, from transportation and logistics to e-commerce and business analytics. By studying these networks and applying MST algorithms, we can improve decision-making in various fields:

- **Optimization of Transport Networks**: Whether it’s airlines, road networks, or rail systems, MST algorithms help in minimizing the cost of transportation by analyzing connectivity and reducing unnecessary routes.
  
- **Supply Chain Efficiency**: By analyzing the relationships between suppliers, retailers, and consumers, businesses can design better and more efficient supply chains.
  
- **Product Recommendation and Market Analysis**: In e-commerce, understanding which products are often purchased together can help businesses improve their recommendation engines and sales strategies.
  
- **Network Resilience and Disaster Recovery**: By studying the structure of complex networks like the airline network or financial institution network, we can design systems that are resilient to disruptions and recover faster in case of failures.

### Overview of Minimum Spanning Tree (MST) Algorithms

In this project, we implemented and tested five classical algorithms to construct **Minimum Spanning Trees (MST)**. These algorithms are widely used in network design, graph theory, and optimization problems. Below is a brief explanation of each algorithm:

1. **Kruskal's Algorithm**:
   Kruskal’s algorithm is a **greedy** approach that sorts all edges of the graph by their weight and adds the edges to the MST one by one, ensuring no cycles are formed. The algorithm uses the **Disjoint Set Union (DSU)** data structure to detect cycles and efficiently manage connected components.

2. **Prim's Algorithm**:
   Prim’s algorithm starts with an arbitrary node and expands the MST by repeatedly adding the smallest edge that connects a new vertex to the already selected vertices. It uses a **priority queue** (min-heap) to efficiently select the next minimum edge.

3. **Borůvka's Algorithm**:
   Borůvka’s algorithm is a **parallelizable** MST algorithm that works by repeatedly finding the smallest outgoing edge for each component of the graph. It connects components until only one component remains, forming the MST.

4. **Reverse-Delete Algorithm**:
   The reverse-delete algorithm starts with a fully connected graph and removes edges in **decreasing order of their weight**, ensuring that the graph remains connected after each removal. It uses a depth-first search (DFS) or similar connectivity check to determine if the graph remains connected after edge removal.

5. **Karger’s Algorithm**:
   Karger’s algorithm is a **randomized** approach that contracts edges randomly, reducing the graph size until only two nodes remain. The remaining edges between these nodes form a minimum cut. This algorithm is particularly used for approximating minimum cuts in large networks.

# Minimum Spanning Tree (MST) Algorithms - Results

## Execution Time, Complexity, and Total Weight for Each Algorithm

Below is a summary of the **execution time**, **computational complexity**, and **total weight** for each algorithm applied to the selected datasets. Each dataset represents a real-world network scenario, and the results have been recorded for better comparison.

### Algorithm Performance

#### 1. **USAir97**

| Algorithm        | Execution Time | Time Complexity |               | Total Weight | Video |
|------------------|----------------|-----------------|---------------|--------------|-------|
| Kruskal’s        | 0.002338s      | O(E log E)      | 23500.64      | 6.116        | [Kruskal Video](https://github.com/mostafashadyy/algorithms_mst_project/blob/main/1_dataset_kruskal.mp4) |
| Prim’s           | 0.003230s      | O(E log V)      | 17805.33      | 6.116        | [Prim Video](https://github.com/mostafashadyy/algorithms_mst_project/blob/main/1_dataset_prim.mp4) |
| Borůvka’s        | 0.005879s      | O(E log V)      | 17805.33      | 6.116        | [Borůvka Video](https://github.com/mostafashadyy/algorithms_mst_project/blob/main/1_dataset_boruvka.mp4) |
| Reverse-Delete   | 0.216917s      | O(E * V)        | 705832.00     | 6.116        | [Reverse-Delete Video](https://github.com/mostafashadyy/algorithms_mst_project/blob/main/1_dataset_reverse_delete.mp4) |
| Karger’s         | 0.540510s      | O(V * V)        | 110224.00     | 0.027        | [Karger Video](https://github.com/mostafashadyy/algorithms_mst_project/blob/main/1_dataset_karger.mp4) |

#### 2. **G13**

| Algorithm        | Execution Time | Time Complexity |               | Total Weight | Video |
|------------------|----------------|-----------------|---------------|--------------|-------|
| Kruskal’s        | 0.001991s      | O(E log E)      | 17030.17      | 440.50       | [Kruskal Video](https://github.com/mostafashadyy/algorithms_mst_project/blob/main/2_dataset_kruskal.mp4) |
| Prim’s           | 0.002398s      | O(E log V)      | 15430.17      | 440.50       | [Prim Video](https://github.com/mostafashadyy/algorithms_mst_project/blob/main/2_dataset_prim.mp4) |
| Borůvka’s        | 0.020102s      | O(E log V)      | 15430.17      | 440.50       | [Borůvka Video](https://github.com/mostafashadyy/algorithms_mst_project/blob/main/2_dataset_boruvka.mp4) |
| Reverse-Delete   | 0.287114s      | O(E * V)        | 1280000.00    | 440.50       | [Reverse-Delete Video](https://github.com/mostafashadyy/algorithms_mst_project/blob/main/2_dataset_reverse_delete.mp4) |
| Karger’s         | 2.018892s      | O(V * V)        | 640000.00     | 1            | [Karger Video](https://github.com/mostafashadyy/algorithms_mst_project/blob/main/2_dataset_karger.mp4) |

#### 3. **Trefethen_2000**

| Algorithm        | Execution Time | Time Complexity |               | Total Weight | Video |
|------------------|----------------|-----------------|---------------|--------------|-------|
| Kruskal’s        | 0.036885s      | O(E log E)      | 31609.03      | 1999.0       | [Kruskal Video](https://github.com/mostafashaddy/algorithms_mst_project/blob/main/3_dataset_kruskal.mp4) |
| Prim’s           | 0.051552s      | O(E log V)      | 240731.86     | 1999.0       | [Prim Video](https://github.com/mostafashadyy/algorithms_mst_project/blob/main/3_dataset_prim.mp4) |
| Borůvka’s        | 0.141159s      | O(E log V)      | 240731.86     | 1999.0       | [Borůvka Video](https://github.com/mostafashadyy/algorithms_mst_project/blob/main/3_dataset_boruvka.mp4) |
| Reverse-Delete   | 22.845624s     | O(E * V)        | 43906000      | 1999.0       | [Reverse-Delete Video](https://github.com/mostafashadyy/algorithms_mst_project/blob/main/3_dataset_reverse_delete.mp4) |
| Karger’s         | 96.323841s     | O(V * V)        | 4000000       | 14930        | [Karger Video](https://github.com/mostafashadyy/algorithms_mst_project/blob/main/3_dataset_karger.mp4) |

#### 4. **LHR04C**

| Algorithm        | Execution Time | Time Complexity |               | Total Weight | Video |
|------------------|----------------|-----------------|---------------|--------------|-------|
| Kruskal’s        | 0.118585s      | O(E log E)      | 1350634.09    | 252.439      | [Kruskal Video](https://github.com/mostafashaddy/algorithms_mst_project/blob/main/4_dataset_kruskal.mp4) |
| Prim’s           | 0.141027s      | O(E log V)      | 992329.52     | 252.439      | [Prim Video](https://github.com/mostafashadyy/algorithms_mst_project/blob/main/4_dataset_prim.mp4) |
| Borůvka’s        | 0.476363s      | O(E log V)      | 992329.52     | 252.439      | [Borůvka Video](https://github.com/mostafashadyy/algorithms_mst_project/blob/main/4_dataset_boruvka.mp4) |
| Reverse-Delete   | 235.314083s    | O(E * V)        | 339078882.00  | 252.439      | [Reverse-Delete Video](https://github.com/mostafashadyy/algorithms_mst_project/blob/main/4_dataset_reverse_delete.mp4) |
| Karger’s         | 417.203164s    | O(V * V)        | 16818201.00   | 1.001        | [Karger Video](https://github.com/mostafashadyy/algorithms_mst_project/blob/main/4_dataset_karger.mp4) |

#### 5. **Amazon0302**

| Algorithm        | Execution Time | Time Complexity |               | Total Weight | Video |
|------------------|----------------|-----------------|---------------|--------------|-------|
| Kruskal’s        | 2.391807s      | O(E log E)      | 249988891.84  | 262110.0     | [Kruskal Video](https://github.com/mostafashaddy/algorithms_mst_project/blob/main/5_dataset_kruskal.mp4) |
| Prim’s           | 2.982875s      | O(E log V)      | 22227561.72   | 262110.0     | [Prim Video](https://github.com/mostafashadyy/algorithms_mst_project/blob/main/5_dataset_prim.mp4) |
| Borůvka’s        | 0.00s          | O(E log V)      | 22227561.72   | 262110.0     | [Borůvka Video](https://github.com/mostafashadyy/algorithms_mst_project/blob/main/5_dataset_boruvka.mp4) |
| Reverse-Delete   | 0.00s          | O(E * V)        | 323674845347  | 262110.0     | [Reverse-Delete Video](https://github.com/mostafashadyy/algorithms_mst_project/blob/main/5_dataset_reverse_delete.mp4) |
| Karger’s         | 0.00s          | O(V * V)        | 68702176321   | 0.00         | [Karger Video](https://github.com/mostafashadyy/algorithms_mst_project/blob/main/5_dataset_karger.mp4) |


### Computational Cost vs. Network Size: MST Algorithm Cost Graph

The computational cost of each MST algorithm was empirically tested by running the algorithms on networks of varying sizes. The performance was measured in terms of execution time, and the results were plotted to show how the cost grows as the number of nodes and edges increases. All growth curves are presented in a single plot with appropriate legends to allow easy comparison between the algorithms.

---

![Kruskal Graph](https://raw.githubusercontent.com/mostafashadyy/algorithms_mst_project/main/graphs/kruskal_graph.png)


![Prim Graph](https://raw.githubusercontent.com/mostafashadyy/algorithms_mst_project/main/graphs/prim_graph.png)


![Boruvka Graph](https://raw.githubusercontent.com/mostafashadyy/algorithms_mst_project/main/graphs/boruvka_graph.png)


![Reverse Graph](https://raw.githubusercontent.com/mostafashadyy/algorithms_mst_project/main/graphs/reverse_graph.png)


![Karger Graph](https://raw.githubusercontent.com/mostafashadyy/algorithms_mst_project/main/graphs/karger_graph.png)

