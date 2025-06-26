import networkx as nx  # used to create and manipulate graphs/networks.
import matplotlib.pyplot as plt  # used for plotting graphs and visualizing results.
from matplotlib.animation import FFMpegWriter  # Enables saving animations as .mp4 videos.
import time  # used to measure execution time.
from tqdm import tqdm  # used to show a progress bar
from scipy.io import mmread  # mmread reads Matrix Market (.mtx) files (used for graph input).
import numpy as np  # used for numerical operations, such as log2 and matrix conversions.

# Boruvka's Algorithm to find MST
def boruvka_mst(G):
    num_components = len(G.nodes)  # Start with each node as its own component
    component = {node: node for node in G.nodes}  # Track which component each node belongs to
    mst = []  # List to store MST edges
    total_weight = 0  # Total weight of MST

    while num_components > 1:  # Repeat until all nodes are in one component
        cheapest = {node: None for node in G.nodes}  # Store cheapest edge for each component

        for u, v, weight in G.edges(data=True):  # Check all edges
            comp_u = component[u]  # Component of u
            comp_v = component[v]  # Component of v

            if comp_u != comp_v:  # If u and v are in different components
                if cheapest[comp_u] is None or cheapest[comp_u][2]['weight'] > weight['weight']:
                    cheapest[comp_u] = (u, v, weight)  # Update cheapest edge for u's component
                if cheapest[comp_v] is None or cheapest[comp_v][2]['weight'] > weight['weight']:
                    cheapest[comp_v] = (u, v, weight)  # Update cheapest edge for v's component

        for comp, edge in cheapest.items():  # Add valid cheapest edges
            if edge:
                u, v, weight = edge
                if component[u] != component[v]:  # Still in different components
                    mst.append((u, v, weight['weight']))  # Add edge to MST
                    total_weight += weight['weight']  # Add weight to total

                    old_component = component[u]  # Get u's component
                    new_component = component[v]  # Get v's component

                    for node in component:  # Merge components
                        if component[node] == old_component:
                            component[node] = new_component
                    num_components -= 1  # One less component
        cheapest = {node: None for node in G.nodes}  # Reset for next round

    return mst, total_weight  # Return MST and total weight

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
def create_mst_video(file_path, output_video="boruvka_mst_video.mp4"):
    # Load graph from file
    G = load_graph(file_path)
    print(f"Loaded graph with {len(G.nodes)} nodes and {len(G.edges)} edges")

    # Start timer for the algorithm execution time
    start_time_algorithm = time.time()

    # Run Borůvka's Algorithm to find the MST
    mst, mst_weight = boruvka_mst(G)
    
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
    computational_cost = len(G.edges) * np.log2(len(G.nodes)) # O(E log V)
    print(f"Computational cost (empirical complexity): {computational_cost}")
    
    # Function to update the animation frame
    def update(frame, computational_cost, algorithm_execution_time):
        ax.clear()
        ax.axis('off')
        ax.set_title(f"Borůvka's Algorithm: Step {frame + 1}/{len(mst)}", fontsize=16)
        
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
        output_video = f"{index+1}_dataset_boruvka.mp4"
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
