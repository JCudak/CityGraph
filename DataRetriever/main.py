import osmnx as ox
import matplotlib.pyplot as plt

# Specify the location and network type
place_name = "Kurdwanów, Podgórze Duchackie, Krakow, Lesser Poland, Poland"
network_type = "drive"

# Download the road network data for the specified place
roads_graph = ox.graph_from_place(place_name, network_type=network_type)

# Plot the road network
fig, ax = ox.plot_graph(ox.project_graph(roads_graph))
plt.show()
