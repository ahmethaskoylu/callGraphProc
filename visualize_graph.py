import matplotlib
matplotlib.use('MacOSX')
import networkx as nx
import matplotlib.pyplot as plt
import sys


def process_call_graph(callgraph_file):
    G = nx.DiGraph()
    with open(callgraph_file, 'r') as f:
        lines = f.readlines()
    stack = []
    for line in lines:
        level = len(line) - len(line.lstrip())
        func_name = line.strip().split()[0]
        while len(stack) > level:
            stack.pop()
        if stack:
            G.add_edge(stack[-1], func_name)
        stack.append(func_name)
    return G

def calculate_metrics(G):
    degree_centrality = nx.degree_centrality(G)
    return degree_centrality

def visualize_graph(G, metrics):
    pos = nx.shell_layout(G)
    node_sizes = [metrics[node] * 5000 for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, alpha=0.6)
    labels = {node: f"{node}\n({metrics[node]:.2f})" for node in G.nodes()}  # Add metric value to label
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8)
    nx.draw_networkx_edges(G, pos, width=0.5, alpha=0.6)
    plt.figure(figsize=(12, 12))
    plt.show()


def visualize_graph_comparison(G_previous, G_current):
    pos = nx.spring_layout(G_current)

    # Nodes
    added_nodes = [node for node in G_current.nodes() if node not in G_previous.nodes()]
    removed_nodes = [node for node in G_previous.nodes() if node not in G_current.nodes()]
    common_nodes = [node for node in G_current.nodes() if node in G_previous.nodes()]

    nx.draw_networkx_nodes(G_current, pos, nodelist=added_nodes, node_color='green', node_size=500, alpha=0.6,
                           label='Added')
    nx.draw_networkx_nodes(G_current, pos, nodelist=removed_nodes, node_color='red', node_size=500, alpha=0.6,
                           label='Removed')
    nx.draw_networkx_nodes(G_current, pos, nodelist=common_nodes, node_color='blue', node_size=500, alpha=0.6,
                           label='Unchanged')

    nx.draw_networkx_labels(G_current, pos, font_size=8)

    # Edges
    added_edges = [edge for edge in G_current.edges() if edge not in G_previous.edges()]
    removed_edges = [edge for edge in G_previous.edges() if edge not in G_current.edges()]
    common_edges = [edge for edge in G_current.edges() if edge in G_previous.edges()]

    nx.draw_networkx_edges(G_current, pos, edgelist=added_edges, edge_color='green', width=1, alpha=0.6)
    nx.draw_networkx_edges(G_current, pos, edgelist=removed_edges, edge_color='red', width=1, alpha=0.6)
    nx.draw_networkx_edges(G_current, pos, edgelist=common_edges, edge_color='blue', width=1, alpha=0.6)

    plt.legend()
    plt.show()

if __name__ == "__main__":
    visualization_type = input("Enter the visualization type (1 for comparison, 2 for single): ")
    if visualization_type == "1":
        callgraph_file_previous = input("Enter the previous call graph file name: ")
        callgraph_file_current = input("Enter the current call graph file name: ")
        G_previous = process_call_graph(callgraph_file_previous)
        G_current = process_call_graph(callgraph_file_current)
        visualize_graph_comparison(G_previous, G_current)
    elif visualization_type == "2":
        callgraph_file = input("Enter the call graph file name: ")
        G = process_call_graph(callgraph_file)
        metrics = calculate_metrics(G)
        visualize_graph(G, metrics)
    else:
        print("Invalid visualization type.")
