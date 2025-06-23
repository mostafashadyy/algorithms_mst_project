import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter
import time
from tqdm import tqdm
from scipy.io import mmread
import numpy as np

# Borůvka's Algorithm to find MST
def boruvka_mst(G):
    # Initialize
    num_components = len(G.nodes)
    component = {node: node for node in G.nodes}  # Each node is its own component
    mst = []
    total_weight = 0

    while num_components > 1:
        # This will store the smallest outgoing edge for each component
        cheapest = {node: None for node in G.nodes}

        # For each edge, update the smallest outgoing edge for its components
        for u, v, weight in G.edges(data=True):
            comp_u = component[u]
            comp_v = component[v]
            
            if comp_u != comp_v:  # If the nodes are in different components
                if cheapest[comp_u] is None or cheapest[comp_u][2]['weight'] > weight['weight']:
                    cheapest[comp_u] = (u, v, weight)
                if cheapest[comp_v] is None or cheapest[comp_v][2]['weight'] > weight['weight']:
                    cheapest[comp_v] = (u, v, weight)

        # Add the smallest edges to the MST and merge the components
        for comp, edge in cheapest.items():
            if edge:
                u, v, weight = edge
                if component[u] != component[v]:  # If they are in different components
                    mst.append((u, v, weight['weight']))
                    total_weight += weight['weight']
                    # Merge the components
                    old_component = component[u]
                    new_component = component[v]
                    for node in component:
                        if component[node] == old_component:
                            component[node] = new_component
                    num_components -= 1

        # Reset the cheapest list for the next iteration
        cheapest = {node: None for node in G.nodes}
    
    return mst, total_weight

# Function to load the graph from a file
def load_graph(file_path):
    # Load the graph data from a .mtx file
    data = mmread(file_path).toarray()  # Load matrix as a dense array
    G = nx.from_numpy_array(data)  # Convert to NetworkX graph (from numpy array)
    return G

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
    computational_cost = len(G.edges) * np.log(len(G.nodes))
    print(f"Computational cost (empirical complexity): {computational_cost}")
    
    # Function to update the animation frame (with computational cost passed in)
    def update(frame, computational_cost, algorithm_execution_time):
        ax.clear()
        ax.axis('off')
        ax.set_title(f"Borůvka's Algorithm: Step {frame + 1}/{len(mst)}", fontsize=16)
        
        # Draw nodes (darker grey)
        nx.draw_networkx_nodes(G, pos, ax=ax, node_size=8, node_color='#B0B0B0')  # Darker grey
        
        # Draw MST edges added so far in a darker blue
        for i in range(frame + 1):
            u, v, weight = mst[i]
            color = '#3D5C7E'  # Darker blue for MST edges
            nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], edge_color=color, width=2, ax=ax)
        
        # Draw remaining edges in red
        remaining_edges = mst[frame + 1:]
        for u, v, weight in remaining_edges:
            color = 'red'  # Red for remaining edges
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
                update(i, start_time_algorithm, computational_cost)
                writer.grab_frame()
                pbar.update(1)
    
    print(f"✅ Video saved as '{output_video}'")

    return computational_cost

# Main function to handle multiple datasets
def process_multiple_files(file_paths):
    for index, file_path in enumerate(file_paths):
        output_video = f"{index+1}_dataset_boruvka.mp4"  # Name the video based on the index
        print(f"Processing {file_path}...")
        computational_cost = create_mst_video(file_path, output_video)
        print(f"Empirical Computational Cost for {file_path}: {computational_cost}")

# Example usage
if __name__ == "__main__":
    # List of file paths for multiple datasets
    file_paths = [
        "USAir97.mtx",  # First file
        "TF14.mtx",  # Second file
        "ex13.mtx",  # Third file
        "lhr04c.mtx",  # Fourth file
        "amazon0302.mtx"  # Fifth file
    ]
    process_multiple_files(file_paths)  # Process all datasets
