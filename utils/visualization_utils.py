import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('MacOSX')

def visualize_graph(G, metrics):
    pos = nx.shell_layout(G)

    # Create a list of node sizes based on degree centrality
    node_sizes = [metrics[node] * 5000 for node in G.nodes()]

    # Draw nodes with sizes based on degree centrality
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, alpha=0.6)

    # Draw labels with smaller font size
    labels = {node: f"{node}\n({metrics[node]:.2f})" for node in G.nodes()}  # Add metric value to label
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8)

    # Draw edges with reduced width
    nx.draw_networkx_edges(G, pos, width=0.5, alpha=0.6)

    # Show the graph
    plt.figure(figsize=(12, 12))  # Increase the size of the figure for better visualization
    plt.show()

#s