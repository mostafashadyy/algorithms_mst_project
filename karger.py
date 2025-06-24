import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter
import time
from tqdm import tqdm
from scipy.io import mmread
import random

# Karger's Algorithm to find Minimum Cut
def karger_min_cut(G):
    
    # Keep contracting until there are only two nodes left
    contraction_steps = []  # To track each contraction step for visualization
    while len(G.nodes) > 2:
        # Randomly select an edge
        u, v = random.choice(list(G.edges()))
        
        # Contract the edge (merge nodes u and v)
        G = nx.contracted_nodes(G, u, v, self_loops=False)
        contraction_steps.append(list(G.edges(data=True)))  # Store the edges after contraction
    
    # The remaining edges between the two nodes are the minimum cut
    min_cut_edges = list(G.edges(data=True))  # Including edge data to get 'weight'
    
    # Now calculate the minimum cut weight properly
    min_cut_weight = sum(weight['weight'] for _, _, weight in min_cut_edges)
    
    return contraction_steps, min_cut_edges, min_cut_weight

# Function to load the graph from a file
def load_graph(file_path):
    # Load the graph data from a .mtx file
    data = mmread(file_path).toarray()  # Load matrix as a dense array
    G = nx.from_numpy_array(data)  # Convert to NetworkX graph (from numpy array)
    
    # Modify edge weights: if weight is negative, change it to a positive value
    for u, v, data in G.edges(data=True):
        if data['weight'] < 0:
            data['weight'] += 1.5  # Adjust negative weight to positive + 1.5
    
    return G

# Main function for animation and video creation
def create_mst_video(file_path, output_video="karger_mst_video.mp4"):
    # Load graph from file
    G = load_graph(file_path)
    print(f"Loaded graph with {len(G.nodes)} nodes and {len(G.edges)} edges")

    # Start timer for the algorithm execution time
    start_time_algorithm = time.time()

    # Run Karger's Algorithm to find the minimum cut
    contraction_steps, min_cut_edges, min_cut_weight = karger_min_cut(G)
    print(f"Minimum Cut has {len(min_cut_edges)} edges with total weight: {min_cut_weight}")

    # Stop timer for the algorithm execution time
    end_time_algorithm = time.time()

    # Calculate the algorithm execution time
    algorithm_execution_time = end_time_algorithm - start_time_algorithm
    print(f"Algorithm execution time: {algorithm_execution_time:.6f} seconds")
    
    # Prepare the figure and axes for animation
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.axis('off')
    pos = nx.kamada_kawai_layout(G)  # Layout for nodes
    
    # Calculate the computational cost (empirical complexity)
    computational_cost = len(G.nodes) * len(G.nodes)  # O(V*V) for connectivity checks
    print(f"Computational cost (empirical complexity): {computational_cost}")
    
    # Function to update the animation frame (with computational cost passed in)
    def update(frame, computational_cost, algorithm_execution_time):
        ax.clear()
        ax.axis('off')
        ax.set_title(f"Karger's Algorithm: Step {frame + 1}/{len(contraction_steps)}", fontsize=16)
        
        # Draw nodes (darker grey)
        nx.draw_networkx_nodes(G, pos, ax=ax, node_size=8, node_color='#B0B0B0')  # Darker grey
        
        # Draw the edges that were contracted in this step
        edges_at_step = contraction_steps[frame]
        for u, v, weight in edges_at_step:
            color = '#3D5C7E'  # Darker blue for Minimum Cut edges
            nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], edge_color=color, width=2, ax=ax)
        
        # Add live execution time and minimum cut cost, along with computational cost on the left of the graph
        ax.text(-0.1, 0.9, f"Total Min Cut Cost: {min_cut_weight:.2f}", transform=ax.transAxes, ha="left", va="top", fontsize=12)
        ax.text(-0.1, 0.85, f"Algorithm Execution Time: {algorithm_execution_time:.6f} sec", transform=ax.transAxes, ha="left", va="top", fontsize=12)
        ax.text(-0.1, 0.8, f"Computational Cost: {computational_cost:.2f}", transform=ax.transAxes, ha="left", va="top", fontsize=12)
    
    # Initialize the video writer using FFmpeg
    writer = FFMpegWriter(fps=30)
    
    total_frames = len(contraction_steps)
    
    # Create the animation with a progress bar
    with tqdm(total=total_frames, desc="Rendering frames", ncols=100, unit="frame") as pbar:
        with writer.saving(fig, output_video, dpi=100):
            for i in range(total_frames):
                update(i, computational_cost, algorithm_execution_time)
                writer.grab_frame()
                pbar.update(1)
    
    print(f"✅ Video saved as '{output_video}'")

    return computational_cost

# Main function to handle multiple datasets
def process_multiple_files(file_paths):
    for index, file_path in enumerate(file_paths):
        output_video = f"{index+1}_dataset_karger.mp4"  # Name the video based on the index
        print(f"Processing {file_path}...")
        computational_cost = create_mst_video(file_path, output_video)
        print(f"Empirical Computational Cost for {file_path}: {computational_cost}")

# Example usage
if __name__ == "__main__":
    # List of file paths for multiple datasets
    file_paths = [
        "USAir97.mtx",  # First file
        "G13.mtx",  # Second file
        "lock2232.mtx",  # Third file
        "lhr04c.mtx",  # Fourth file
        "amazon0302.mtx"  # Fifth file
    ]
    process_multiple_files(file_paths)  # Process all datasets
