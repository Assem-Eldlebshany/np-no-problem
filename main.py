import os
import json
from draw_initial_layout import InitialLayoutDrawer
from draw_spring_layout import SpringLayoutDrawer
from draw_kamada_kawai_layout import KamadaKawaiLayoutDrawer
from draw_planar_layout import PlanarLayoutDrawer
from kamada_gradient import GradientLayoutDrawer
from simluated_annealing import SimulatedAnnealingDrawer

class ScalableGraphDrawer:
    def __init__(self, filename):
        # Load the graph data from the JSON file
        try:
            with open(filename, 'r') as file:
                self.graph_data = json.load(file)
            print(f"File {filename} loaded successfully.")
        except FileNotFoundError:
            print(f"Error: {filename} not found.")
            return
        except json.JSONDecodeError:
            print(f"Error: JSON format in the file {filename} is incorrect.")
            return

        # PlanarLayoutDrawer(self.graph_data)
        # InitialLayoutDrawer(self.graph_data)
        # SpringLayoutDrawer(self.graph_data)
        # KamadaKawaiLayoutDrawer(self.graph_data)
        # GradientLayoutDrawer(self.graph_data, alpha=1, learning_rate=0.1, max_iter=1000)
        SimulatedAnnealingDrawer(self.graph_data)

# Directory containing the graph files
directory = "testGraph"

# Check if the directory exists
if not os.path.isdir(directory):
    print(f"Error: Directory {directory} not found.")
else:
    # List all JSON files in the directory
    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]

    # Check if there are any JSON files to process
    if not json_files:
        print(f"No JSON files found in {directory}.")
    else:
        # Iterate over each file and process it
        for graph_file in json_files:
            file_path = os.path.join(directory, graph_file)
            print(f"Starting ScalableGraphDrawer for {file_path}...")
            ScalableGraphDrawer(file_path)
