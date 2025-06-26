import networkx as nx  # used to create and manipulate graphs/networks.
import matplotlib.pyplot as plt  # used for plotting graphs and visualizing results.
from matplotlib.animation import FFMpegWriter  # Enables saving animations as .mp4 videos.
import time  # used to measure execution time.
from tqdm import tqdm  # used to show a progress bar
from scipy.io import mmread  # mmread reads Matrix Market (.mtx) files (used for graph input).
import numpy as np  # used for numerical operations, such as log2 and matrix conversions.

# DSU (Disjoint Set Union) class for cycle detection in Kruskal's Algorithm
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))  # Each node starts as its own parent (not connected to anyone)
        self.rank = [0] * n  # Rank keeps track of tree height (used to keep trees short)

    def find(self, x):
        # This function finds the root of the set that x belongs to
        # If x is not its own parent, keep moving up to find the root
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression: make x point directly to root
        return self.parent[x]  # Return the root

    def union(self, x, y):
        # This function joins the sets that x and y belong to
        rootX = self.find(x)  # Find the root of x
        rootY = self.find(y)  # Find the root of y

        if rootX != rootY: # Only join them if they are in different sets
            # Attach the shorter tree to the taller one (union by rank)
            if self.rank[rootX] > self.rank[rootY]:
                self.parent[rootY] = rootX  # Make rootX the parent
            elif self.rank[rootX] < self.rank[rootY]:
                self.parent[rootX] = rootY  # Make rootY the parent
            else:
                self.parent[rootY] = rootX  # Pick one as parent if ranks are equal
                self.rank[rootX] += 1  # Increase the rank (height) of the new root
            return True  # Successfully joined two different sets (no cycle)
        return False  # They were already connected (would create a cycle)


# Kruskal's Algorithm to find MST
def kruskal_mst(G):
    edges = list(G.edges(data=True))  # Get all edges from the graph, including their weights

    edges.sort(key=lambda x: x[2]['weight'])  # Sort edges by weight (smallest first)

    dsu = DSU(len(G.nodes))  # Create a DSU object to track connected nodes (for cycle checking)
    mst = []  # This will store the final MST edges
    total_weight = 0  # This will keep track of the total weight of the MST

    # Loop through each edge, starting from the smallest weight
    for u, v, weight in edges:
        if dsu.union(u, v):  # Try to add the edge; if it doesn’t form a cycle
            mst.append((u, v, weight['weight']))  # Add edge to the MST
            total_weight += weight['weight']  # Add its weight to the total

    return mst, total_weight  # Return the list of MST edges and the total weight

# Function to load the graph from a file
def load_graph(file_path):
    # Load the graph data from a .mtx file
    data = mmread(file_path).toarray()  # Turns the matrix into a 2D NumPy array
    G = nx.from_numpy_array(data)  # Convert to NetworkX graph (from numpy array)

    # Loop through all edges in the graph
    for u, v, data in G.edges(data=True):
        # If any edge has a negative weight
        if data['weight'] < 0:
            data['weight'] += 1.5  # Adjust negative weight to positive + 1.5
            
    return G # Return the final graph

# Main function for animation and video creation
def create_mst_video(file_path, output_video="kruskal_mst_video.mp4"):
    # Load graph from file
    G = load_graph(file_path)
    print(f"Loaded graph with {len(G.nodes)} nodes and {len(G.edges)} edges")

    # Start timer for the algorithm execution time
    start_time_algorithm = time.time()
    
    # Run Kruskal's Algorithm to find the MST
    mst, mst_weight = kruskal_mst(G)

    # Stop timer for the algorithm execution time
    end_time_algorithm = time.time()

    # Calculate the algorithm execution time
    algorithm_execution_time = end_time_algorithm - start_time_algorithm
    print(f"Algorithm execution time: {algorithm_execution_time:.6f} seconds")

    print(f"MST has {len(mst)} edges with total weight: {mst_weight}")
    
    # Prepare the figure and axes for animation
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.axis('off')
    pos = nx.kamada_kawai_layout(G)  # Layout for nodes
    
    # Calculate the computational cost (empirical complexity)
    computational_cost = len(G.edges) * np.log2(len(G.edges)) # O(E log E)
    print(f"Computational cost (empirical complexity): {computational_cost}")
    
    # Function to update the animation frame
    def update(frame, computational_cost, algorithm_execution_time):
        ax.clear()
        ax.axis('off')
        ax.set_title(f"Kruskal's Algorithm: Step {frame + 1}/{len(mst)}", fontsize=16)
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, ax=ax, node_size=8, node_color='#B0B0B0')
        
        # Draw MST edges added so far in a darker blue
        for i in range(frame + 1):
            u, v, weight = mst[i]
            color = '#3D5C7E'
            nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], edge_color=color, width=2, ax=ax)
        
        # Draw remaining edges in red
        remaining_edges = mst[frame + 1:]
        for u, v, weight in remaining_edges:
            color = 'red'
            nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], edge_color=color, width=0.5, ax=ax)
        
        # Add live execution time and MST cost, along with computational cost on the left of the graph
        ax.text(-0.1, 0.9, f"Total MST Cost: {mst_weight:.2f}", transform=ax.transAxes, ha="left", va="top", fontsize=12)
        ax.text(-0.1, 0.85, f"Algorithm Execution Time: {algorithm_execution_time:.6f} sec", transform=ax.transAxes, ha="left", va="top", fontsize=12)
        ax.text(-0.1, 0.8, f"Computational Cost: {computational_cost:.2f}", transform=ax.transAxes, ha="left", va="top", fontsize=12)
    
    # Initialize the video writer using FFmpeg
    writer = FFMpegWriter(fps=30)
    
    total_frames = len(mst)
    
    # Create the animation with a progress bar
    with tqdm(total=total_frames, desc="Rendering frames", ncols=100, unit="frame") as pbar:
        with writer.saving(fig, output_video, dpi=100):
            for i in range(total_frames):
                update(i, computational_cost, algorithm_execution_time)
                writer.grab_frame()
                pbar.update(1)
    
    print(f"Video saved as '{output_video}'")

    return computational_cost

# Main function to handle multiple datasets
def process_multiple_files(file_paths):
    for index, file_path in enumerate(file_paths):
        output_video = f"{index+1}_dataset_kruskal.mp4"
        print(f"Processing {file_path}...")
        computational_cost = create_mst_video(file_path, output_video)
        print(f"Empirical Computational Cost for {file_path}: {computational_cost}")

if __name__ == "__main__":
    file_paths = [
        "USAir97.mtx",
        "G13.mtx",
        "Trefethen_2000.mtx",
        "lhr04c.mtx",
        "amazon0302.mtx"
    ]
    process_multiple_files(file_paths)
