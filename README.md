# Detection of Sensitive Parts of the Road Network Based on Graph Centrality Measures

### Authors: Monika Etrych, Karol Jurzec, Jakub Cudak

## Abstract
In urban planning and transportation management, identifying critical segments of road networks is essential for optimizing traffic flow and enhancing infrastructure resilience. This paper presents a methodology for detecting sensitive parts of a road network using graph centrality measures. Utilizing the OSMnx library to retrieve and construct the road graph of a specified territory. This weighted graph is then subjected to various centrality analyses, including betweenness, closeness, and eigenvector centrality, to pinpoint the most influential nodes and edges within the network.

Our approach highlights the road segments that are crucial for maintaining optimal traffic flow and those that could cause significant disruptions if compromised. The findings offer valuable insights for urban planners and traffic management authorities, enabling targeted improvements and strategic interventions in the road infrastructure. This research contributes to more efficient and resilient urban transportation systems by leveraging advanced graph theoretical techniques.

## Dataset
The dataset consists of nodes and edges that form a road graph of a user-selected territory. This dataset is obtained using the `osmnx` (a Python library for OpenStreetMap data), which serves as a core component of our program. The primary function, `ox.graph_from_place(...)`, allows us to retrieve a road graph for a specified location using two main parameters: location and filter.

The user is required to provide only one parameter: a location identification string (e.g., "Kurdwanów, Podgórze, Krakow, Lesser Poland, Poland"), which defines the geographic area for the graph data. Our program sets the second parameter, a custom filter, to refine the dataset.

By applying a custom filter developed through a trial and error method (illustrated in Figure 1), we can extract relevant data from the extensive OSM dataset, focusing exclusively on roads intended for car travel while excluding service roads.

```python
filter_string = ( 
    '["highway"~"motorway|trunk|primary|secondary|tertiary|road|' 
    'residential|motorway_link|trunk_link|primary_link|secondary_link' 
    '|tertiary|link|living_street|unclassified|service"]["access"!="no"]'
)

However, the graph obtained using this method is overly complex, containing many unnecessary nodes, particularly in roundabouts.



