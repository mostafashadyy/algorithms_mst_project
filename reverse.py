import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter
import time
from tqdm import tqdm
from scipy.io import mmread

def reverse_delete_mst(G):
    # Make a copy of the graph to work on
    graph = G.copy()
    
    # Get all edges sorted in descending order of weight
    edges = sorted(graph.edges(data=True), key=lambda x: -x[2].get('weight', 1))
    
    mst_edges = []
    total_weight = 0
    
    for u, v, weight in edges:
        # Temporarily remove the edge
        graph.remove_edge(u, v)
        
        # Check if the graph is still connected
        if not nx.is_connected(graph):
            # If not connected, this edge must be in the MST, so add it back
            graph.add_edge(u, v, weight=weight['weight'])
            mst_edges.append((u, v, weight['weight']))
            total_weight += weight['weight']
        # Else, the edge is permanently removed
    
    return mst_edges, total_weight

def load_graph(file_path):
    # Load the graph data from a .mtx file
    data = mmread(file_path).toarray()  # Load matrix as a dense array
    G = nx.from_numpy_array(data)  # Convert to NetworkX graph (from numpy array)
    
    # Ensure the edge weights are properly set as numbers (e.g., float)
    for u, v, data in G.edges(data=True):
        if 'weight' not in data:  # In case there is no 'weight' attribute
            data['weight'] = 1  # Default weight if no weight attribute exists
        data['weight'] = float(data['weight'])  # Ensure the weight is stored as a float
    
    return G

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
    computational_cost = len(G.edges) * len(G.nodes)  # O(E*V) for connectivity checks
    print(f"Computational cost (empirical complexity): {computational_cost}")
    
    # Function to update the animation frame
    def update(frame, computational_cost, algorithm_execution_time):
        ax.clear()
        ax.axis('off')
        ax.set_title(f"Reverse-Delete Algorithm: Step {frame + 1}/{len(mst)}", fontsize=16)
        
        # Draw nodes (darker grey)
        nx.draw_networkx_nodes(G, pos, ax=ax, node_size=8, node_color='#B0B0B0')
        
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
                update(i, start_time_algorithm, computational_cost)
                writer.grab_frame()
                pbar.update(1)
    
    print(f"✅ Video saved as '{output_video}'")

    return computational_cost

def process_multiple_files(file_paths):
    for index, file_path in enumerate(file_paths):
        output_video = f"{index+1}_dataset_reverse_delete.mp4"
        print(f"Processing {file_path}...")
        computational_cost = create_mst_video(file_path, output_video)
        print(f"Empirical Computational Cost for {file_path}: {computational_cost}")

if __name__ == "__main__":
    file_paths = [
        "USAir97.mtx",  # First file
        "TF14.mtx",  # Second file
        "ex13.mtx",  # Third file
        "lhr04c.mtx",  # Fourth file
        "amazon0302.mtx"  # Fifth file
    ]
    process_multiple_files(file_paths)  # Process all datasets
