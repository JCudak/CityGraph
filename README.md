# Detection of Sensitive Parts of the Road Network Based on Graph Centrality Measures
<p align="center">
  <img src="https://github.com/kifur2/CityGraph/blob/main/DataRetriever/img/main.jpg" width="75%">
</p>




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
```

However, the graph obtained using this method is overly complex, containing many unnecessary nodes, particularly in roundabouts.

<p align="center">
  <img src="https://github.com/kifur2/CityGraph/blob/main/DataRetriever/img/dataset_1.png" width="75%">
</p>

The excess nodes significantly increase the computing power required to calculate centralities. Therefore, we needed to simplify the graph. Our approach involved merging vertices with only two neighboring nodes and combining the edges of the consecutive merged nodes.

<p align="center">
  <img src="https://github.com/kifur2/CityGraph/blob/main/DataRetriever/img/dataset_2.png" width="75%">
</p>

This operation made the retrieved graph nearly ready for analysis using centrality measures. However, each road can be of a different type, ranging from primary or secondary roads to tracks or service roads. Therefore, we need to assign appropriate "weight" values to these roads to account for their varying importance and characteristics. To achieve this, we classify the roads based on their type and assign a weight value accordingly. 
```python
road_type_weights = {
    'motorway': 0.1,
    'motorway_link': 0.1,
    'trunk': 0.15,
    'trunk_link': 0.15,
    'primary': 0.2,
    'primary_link': 0.2,
    'secondary': 0.4,
    'secondary_link': 0.4,
    'tertiary': 0.6,
    'tertiary_link': 0.6,
    'residential': 0.8,
    'service': 0.8,
    'track': 0.8
}
```
Primary roads receive lower weight values due to ease of transportation, while tracks and service roads are assigned higher weights. This weighting system allows us to better reflect the true connectivity and importance of different roads within the graph.

## The centrality measures

Once the weights are assigned, the graph is ready for comprehensive analysis using various centrality measures, such as betweenness, closeness, and eigenvector centrality. These measures will provide insights into the most critical nodes and edges within the road network, helping us to understand traffic flow, identify potential bottlenecks, and optimize route planning.
By simplifying the graph and appropriately weighting the roads, we enhance the efficiency and accuracy of our centrality analyses, leading to more informed decision-making in urban planning and transportation management.

### Betweenness centrality
Shows which nodes are important based on the shortest paths between two nodes. The higher the value, the more shortest paths pass through this node.
In the whole map overview there are most of the low (green) values. 

<p align="center">
  <img src="https://github.com/kifur2/CityGraph/blob/main/DataRetriever/img/betweeneess_1.png" width="75%">
</p>

It is noticeable one almost connected circular lane.They are mostly primary or secondary roads. As road wiki says they link smaller and bigger cities. Krakow does not have the ring road so many trucks must go through them. In addition, the Debnicki Bridge with one of the biggest centrality values connects many of the shortest paths for two reasons, one: it is the primary road, and two: it is close to the Old Town and center of the city.

### Closeness centrality
Closeness centrality measures how close a node is to all other nodes in a network, based on the average shortest path length from the node to all other nodes. Nodes with high closeness centrality are more in centrum, and can easily interact with all other nodes.

<p align="center">
  <img src="https://github.com/kifur2/CityGraph/blob/main/DataRetriever/img/closesness_1.png" width="75%">
</p>

It is observable that the highest values again are through the biggest roads in the city. This time it means that they are in the center and it is easy to connect with all other places.
There are some suspiciously green points, after analysis of roads, it has  occurred that they are one-way roads and that is why closeness centrality had a problem with directed graph. It means that from these points it is impossible or very hard to transport to another part of the city.


### Random walk betweenness
It is similar to closeness centrality but shows how often nodes are visited during random walks by graph. A high value can indicate that a node is easily reachable, meaning numerous paths traverse through it, and it is not positioned at the network's periphery.

<p align="center">
  <img src="https://github.com/kifur2/CityGraph/blob/main/DataRetriever/img/random_walk.png" width="75%">
</p>

The highest random walk betweenness is in the south-east of the city, where there is a motorway. A motorway has the lowest weight so most random walks go through it. There is a piece of the missing road it can be caused by the missing data or mislabelled and that is why filters have deleted it. It can have an impact on the interpretation.

### Eigenvector centrality
It shows the importance of the nodes based on the amount of links and their quality(eigenvector centrality of other nodes). Most of the nodes have less than 4 linked nodes. Only on Zywiecka Street is there a residential area with many small crossings nearby. 

### Pagerank centrality
This is a variant of eigenvector centrality. Similarly, it shows the importance of nodes based on the number of links and their quality, but adds node weights.

### Local Clustering Coefficient
This indicator is in the range between 0 and 1. When it is closer to one, it means the graph is closer to be a Clique (every node has a connection with all others). In the whole city there are around ten 2-point cliques. They are mostly residential roads, not very mobile.

## Coloring Nodes Based on Calculated Centralities

To identify key areas in the road network where new connections can improve traffic flow, we use a visualization technique that colors the city graph based on centrality values. This is done with the `color_nodes(c_measures)` function, which assigns colors to nodes according to their centrality measures (`c_measures`), making it easier to see which parts of the network are most loaded.

### Creating Histogram and Coloring Nodes

We use a histogram to show the distribution of centrality values across the nodes. This histogram uses a logarithmic scale to make the wide range of values more readable. The nodes are colored as follows:

- **Green**: Nodes with the lowest centrality values
- **Yellow**: Nodes with moderate centrality values
- **Red**: Nodes with the highest centrality values

This gradient color scheme makes it easy to see which nodes are most critical for maintaining traffic flow.

### Applying the Color Scheme

Here's how we apply the color scheme:

1. **Compute Centralities**: Calculate the centrality measures for each node.
2. **Create a Log-Scaled Histogram**: Based on the minimum and maximum centrality values, create a log-scaled histogram.
3. **Map Colors**: Assign colors to nodes based on their centrality values from the histogram, with green for low centrality values and red for high centrality values.

The log-scaled gradient histogram provides a clear and effective way to visualize centrality measures. This helps identify potential new edges in the road network that can improve graph flow, leading to a more efficient road network.

## Identification of Potential New Edges that Set Traffic in Motion

To understand and optimize traffic flow in the road network, it is essential to identify and modify edges that can significantly impact traffic dynamics. This involves adding new edges or removing existing ones to assess how these changes influence the overall connectivity and efficiency of the network.

### Adding Edges

The `add_edge` function allows users to add new edges to the road network.

```python
def add_edge(road_graph):
   edge_id = parse_edge_id_input()
   if edge_id:
       weight = float(input("Enter weight for the edge: "))
       road_graph.add_edge(*edge_id, weight=weight)
       road_graph_sum.add_edge(*edge_id, weight=weight)
       added_edges.append(edge_id)
       print(f"Edge {edge_id} added with weight {weight}.")
```
Here's how the process works:

- **Parse Edge ID**: The `parse_edge_id_input` function prompts the user to enter the edge ID in the format (node1, node2, key). This ID specifies the two nodes and a unique key that define the edge.
- **Enter Edge Weight**: The user is then prompted to enter a weight for the new edge, which reflects its importance or capacity.
- **Add Edge to Graphs**: The edge is added to both `road_graph` and the auxiliary graph `road_graph_sum` with the specified weight. The edge ID is also appended to the `added_edges` list for tracking purposes.

This function enables the introduction of new connections within the road network, allowing for the simulation and analysis of potential improvements in traffic flow.

### Removing Edges

The `delete_edge` function allows users to remove existing edges from the road network.

```python
def delete_edge(road_graph):
    edge_id = parse_edge_id_input()
    if edge_id and road_graph.has_edge(*edge_id):
        road_graph.remove_edge(*edge_id)
        deleted_edges.append(edge_id)
        print(f"Edge {edge_id} removed.")
    else:
        print("Edge does not exist.")
```

The process is as follows:

1. **Parse Edge ID**: Similar to adding an edge, the `parse_edge_id_input` function is used to specify the edge to be removed.
2. **Check Edge Existence**: The function checks if the specified edge exists in the `road_graph`.
3. **Remove Edge from Graph**: If the edge exists, it is removed from `road_graph`, and the edge ID is appended to the `deleted_edges` list.

Removing edges allows for the analysis of how the absence of certain connections affects traffic flow, helping to identify potential bottlenecks or redundant routes.

### Interactive Edge Identification

The process of adding or removing edges is interactive. Users can identify the nodes that compose an edge by clicking on the edges within the visualization tool. When an edge is selected, a pop-up displays the nodes that compose the edge, aiding in accurate and intuitive modifications.

### Creating Difference Graph

To evaluate the impact of modifications to the road network, we generate a difference graph that highlights changes in centrality measures resulting from the addition or removal of edges. This process provides an analysis of how these modifications affect traffic flow.

To compute the difference between both centralities, we need to keep track of three graphs: `old_graph`, `road_graph`, and `road_graph_sum`. 
- The `old_graph` represents the original road network as initially read and remains unchanged throughout the process. 
- The `road_graph` includes all added edges and excludes removed edges, reflecting the current state of the network. 
- The `road_graph_sum` tracks all modifications, including both added and removed edges.

Next, we compute the centrality measures for both `old_graph` and `road_graph`. The `_compute_centralities` function calculates these measures based on the specified algorithm type, such as betweenness, closeness, or eigenvector. If centrality measures for the `old_graph` are not already available, they are computed first. The centrality measures for the `road_graph` are always computed to reflect its current state.

```python
def _compute_difference(old_measure, new_measure):
    old_measure = dict(old_measure)
    new_measure = dict(new_measure)
    diff_measure = {}
    for id, _ in old_measure.items():
        diff_measure[id] = new_measure[id] - old_measure[id]
    return list(diff_measure.items())
```

After computing the centralities, we calculate the differences between the centrality measures of old_graph and road_graph which is done with the _compute_difference function by subtracting the old_graph centrality values from road_graph measures for each node, resulting in a list of differences.

<p align="center">
  <img src="https://github.com/kifur2/CityGraph/blob/main/DataRetriever/img/difference_graph.png" width="75%">
</p>

The generate_difference function then visualizes these differences. It uses the color_nodes(diff_measures) function which assigns colors to the nodes based on differences, with green indicating improved centrality, red indicating worsened centrality, and yellow indicating minimal or zero change. 
The color_edges(added_edges, deleted_edges) function marks newly added edges in green and removed edges in red. At the end the create_map function generates an HTML map with these color codings, which is then displayed in a web browser. 

## Usage Examples

To illustrate the process of identifying and optimizing critical parts of a road network, we will use the examples of Krakow and Wroclaw cities, located in Poland. In first scenario, we will focus on closeness centrality for Krakow and it the second, on the betweenness centrality for Wroclaw. Then, after removing some edges in graphs, we will create a difference graph, which will visualize the impact of these changes.


### Load Initial Krakow Road Network

To begin, we load the road network data for Krakow by defining the location	as:
```
initial_place = "Krakow, Lesser Poland, Poland"
```
We then use the OSMnx library to retrieve the road network graph. After applying the closeness_centrality function to it as a result we get the map of Krakow shown below:

<p align="center">
  <img src="https://github.com/kifur2/CityGraph/blob/main/DataRetriever/img/krakow_1.png" width="75%">
</p>


The initial centrality values are visualized on a map of Krakow, with nodes colored from green (low centrality) to red (high centrality). This visualization helps us identify the most important nodes in terms of accessibility.


### Removing an Existing Edge

OOne of the highest values (marked in red) of closeness centrality in the initial road network is the edge containing the Nowohucki Bridge, which links two sides of the city. This bridge is a crucial connection point, as many people traveling from one part of Krakow to another must pass through it.

To understand the impact of this critical edge on the overall network, we simulate its removal. This process demonstrates how the removal of such a key connection can affect the network's connectivity and centrality measures.

First, we identify the ID of the edge we want to remove. This can be done by clicking on the edge in the visualization tool, which displays the necessary information needed to remove the edge:

<p align="center">
  <img src="https://github.com/kifur2/CityGraph/blob/main/DataRetriever/img/krakow_2.png" width="50%">
</p>


As depicted in the image, there are two roads on the bridge. Therefore, we need to remove both of them to simulate the impact accurately.

### Generating and Visualizing the Difference Graph

Next, we compute the differences in closeness centrality between the original and modified graphs. This allows us to visualize how the removal of the edge affects the network:
<p align="center">
  <img src="https://github.com/kifur2/CityGraph/blob/main/DataRetriever/img/krakow_3.png" width="75%">
</p>

After removing an edge corresponding to Nowohucki bridge we can observe a slightly better closeness centrality values (marked in green and yellow) in the neighborhood of this bridge. Nodes marked in yellow signify areas where the closeness centrality remained the same.

This scenario demonstrates that our graph modification has a limited impact. The most significant effects are observed closest to the modification point, and the impact gradually decreases further away from the bridge.


### Load Initial Wroclaw Road Network

We load the road network data for Wroclaw by changing the initial location as:

```
initial_place = "Wroclaw, Poland"
```

We then again retrieve the road network graph of the city and apply to it betweeness_centrality function. As the result we get the Wroclaw road network shown below: 


<p align="center">
  <img src="https://github.com/kifur2/CityGraph/blob/main/DataRetriever/img/wroclaw_1.png" width="75%">
</p>

On the map above we can see how the traffic is distributed throughout the whole city; The nodes marked as red indicate that these crossings are the most important for the network, and so there will probably be bigger traffic intensity compared to nodes marked green or yellow. CBy comparing the graph with the actual traffic behavior, we can observe many similarities, so we can say that betweeness_centrality properly shows how the road flow of the Wroclaw is generated. 

### Difference Graph After Removal of Edge

After the removal of the Krakowsa street, we can see below the part of the graph that got affected because of that change.

<p align="center">
  <img src="https://github.com/kifur2/CityGraph/blob/main/DataRetriever/img/wroclaw_2.png" width="75%">
</p>

The most significant positive impact is seen near the deleted edges, where some neighboring nodes have experienced a reduction in traffic. However, this change has also negatively affected other parts of the graph. The traffic that previously traveled through Krakowska Street has been redirected through other nodes, increasing their load.

## Summary

In this research, we presented an application to identify critical parts of city road networks using graph centrality measures. We used the OSMnx library to create and analyze road graphs for specific areas, focusing on measures like betweenness, closeness, and eigenvector centrality.

We started by gathering road data from OpenStreetMap, refining it to focus on car travel. We simplified the graph by merging nodes with only two neighbors and assigned weights to different road types based on their importance. This made our analysis faster and more accurate.

Our centrality measures revealed key roads and intersections: betweenness centrality identified crucial paths, closeness centrality highlighted central, accessible roads, and eigenvector centrality pointed out important roads based on their connections. We visualized these results with color-coded maps to show critical network parts clearly.
Applying our method to the cities of Krakow and Wroclaw, we successfully identified critical road segments and demonstrated how modifications could impact overall traffic dynamics. Our research provides valuable insights for traffic management, offering tools and methodologies to enhance the resilience of urban transportation systems.


### Resources
1. Michele Borassi and Emanuele Natale (2019), “KADABRA is an ADaptive Algorithm for Betweenness via Random Approximation”
2. [OpenStreetMap: Key:highway](https://wiki.openstreetmap.org/wiki/Key:highway)
3. Evans Tim S., Chen Bingsheng (2022), "Linking the network centrality measures closeness and degree". Communications Physics
4. White Scott, Smyth Padhraic (2003), Algorithms for Estimating Relative Importance in Networks, ACM SIGKDD International Conference on Knowledge Discovery and Data Mining
5. M. E. J. Newman, "The mathematics of networks"
6. Wang Ziyang. "Improved Link-Based Algorithms for Ranking Web Pages", New York University, Department of Computer Science
7. Kemper Andreas (2009). Valuation of Network Effects in Software Markets: A Complex Networks Approach, Springer. p. 142. ISBN 9783790823660




