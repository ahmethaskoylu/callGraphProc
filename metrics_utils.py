import networkx as nx

def calculate_metrics(G):
    # Degree centrality as a simple metric
    degree_centrality = nx.degree_centrality(G)
    return degree_centrality
