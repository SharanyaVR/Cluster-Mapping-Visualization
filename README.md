# Cluster-Mapping-Visualization
This project aims at visualizing the relations between different feature clusters.

Lot of times, we have multiple features and their individual clusters.
This visualization is a great way to visually analyze the co-relation between different feature clusters.

It implements Force-Directed algorithm for the graph.

#How-to-use
Input:
Run the python program and provide as input the paths to the following three directories, respectively:
D1) Path to directory containing cluster mapping files
  ex: ClusterMappingFiles
D2) Path to directory that contains files indicating the mapping between every node and its cluster, per feature
  ex: NodeIdandClusterIdMapping 
D3) Path to directory that contains files detailing every node id with the values
  ex: FeatureDetails

Output:
A json file which contains processed cluster information read y to use by the html file.
You can now view your visualization by opening the html file

Note: Both the html and the json file should be saved in the same folder.
