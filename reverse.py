import networkx as nx  # used to create and manipulate graphs/networks.
import matplotlib.pyplot as plt  # used for plotting graphs and visualizing results.
from matplotlib.animation import FFMpegWriter  # Enables saving animations as .mp4 videos.
import time  # used to measure execution time.
from tqdm import tqdm  # used to show a progress bar
from scipy.io import mmread  # mmread reads Matrix Market (.mtx) files (used for graph input).

# Reverse's Algorithm to find MST
def reverse_delete_mst(G):
    graph = G.copy()  # Make a copy so we don't change the original graph

    edges = sorted(graph.edges(data=True), key=lambda x: -x[2].get('weight', 1))  # Get all edges sorted in descending order of weight

    mst_edges = []  # List to store edges that will be in the MST
    total_weight = 0  # Total weight of the MST

    for u, v, weight in edges:  # Go through edges from heaviest to lightest
        graph.remove_edge(u, v)  # Try removing this edge from the graph

        # Check if the graph is still connected without this edge
        if not nx.is_connected(graph):  
            # If it's not connected anymore, that means this edge was necessary to keep the graph connected
            graph.add_edge(u, v, weight=weight['weight'])  # So, it's part of the MST and we must add it back
            mst_edges.append((u, v, weight['weight']))  # Add it to MST
            total_weight += weight['weight']  # Add its weight to total
        # Else the graph is still connected, we leave the edge removed (it's not needed in the MST)

    return mst_edges, total_weight  # Return the MST edges and total cost

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

def create_mst_video(file_path, output_video="reverse_delete_mst_video.mp4"):
    # Load graph from file
    G = load_graph(file_path)
    print(f"Loaded graph with {len(G.nodes)} nodes and {len(G.edges)} edges")

    # Start timer for the algorithm execution time
    start_time_algorithm = time.time()

    # Run Reverse-Delete Algorithm to find the MST
    mst, mst_weight = reverse_delete_mst(G)

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
    computational_cost = len(G.edges) * len(G.nodes)  # O(E*V)
    print(f"Computational cost (empirical complexity): {computational_cost}")
    
    # Function to update the animation frame
    def update(frame, computational_cost, algorithm_execution_time):
        ax.clear()
        ax.axis('off')
        ax.set_title(f"Reverse-Delete Algorithm: Step {frame + 1}/{len(mst)}", fontsize=16)
        
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
        
        # Add live execution time and MST cost, along with computational cost
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

def process_multiple_files(file_paths):
    for index, file_path in enumerate(file_paths):
        output_video = f"{index+1}_dataset_reverse_delete.mp4"
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
