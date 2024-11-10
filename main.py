import json
from draw_initial_layout import InitialLayoutDrawer
from draw_spring_layout import SpringLayoutDrawer
from draw_kamada_kawai_layout import KamadaKawaiLayoutDrawer
from draw_planar_layout import PlanarLayoutDrawer


class ScalableGraphDrawer:
    def __init__(self, filename):
        # Load the graph data from the JSON file
        try:
            with open(filename, 'r') as file:
                self.graph_data = json.load(file)
            print("File loaded successfully.")
        except FileNotFoundError:
            print(f"Error: {filename} not found.")
            return
        except json.JSONDecodeError:
            print("Error: JSON format in the file is incorrect.")
            return

        # Initialize each layout drawer
        InitialLayoutDrawer(self.graph_data)
        SpringLayoutDrawer(self.graph_data)
        KamadaKawaiLayoutDrawer(self.graph_data)
        PlanarLayoutDrawer(self.graph_data)


# Load and draw the graph from the file
graph_file = "file.json"
print("Starting ScalableGraphDrawer...")
ScalableGraphDrawer(graph_file)