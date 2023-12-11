import matplotlib
matplotlib.use('MacOSX')
import networkx as nx
import matplotlib.pyplot as plt
import sys
import Levenshtein
import json


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

def compare_call_graphs(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        content1 = f1.read()
        content2 = f2.read()

    distance = Levenshtein.distance(content1, content2)
    return distance

def graph_edit_distance(graph1, graph2):
    return nx.graph_edit_distance(graph1, graph2)
def compare_call_graphs_similarity(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        content1 = f1.read()
        content2 = f2.read()

    distance = Levenshtein.distance(content1, content2)
    max_len = max(len(content1), len(content2))

    similarity_percentage = ((max_len - distance) / max_len) * 100
    return similarity_percentage


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
    distance = graph_edit_distance(G_previous, G_current)
    plt.title(f"Call Graph Comparison (Edit Distance: {distance:.2f})")

    plt.legend()
    plt.show()

if __name__ == "__main__":
    visualization_type = input("Enter the visualization type (1 for comparison, 2 for single): ")
    if visualization_type == "1":
        config_file = input("Enter the path to the configuration file (config.json): ")
        try:
            with open(config_file, 'r') as config_f:
                config = json.load(config_f)

            callgraph_file_previous = config["call_graphs"]["previous"]
            callgraph_file_current = config["call_graphs"]["current"]

            G_previous = process_call_graph(callgraph_file_previous)
            G_current = process_call_graph(callgraph_file_current)
            visualize_graph_comparison(G_previous, G_current)

            distance = compare_call_graphs(callgraph_file_previous, callgraph_file_current)
            print(f"Levenshtein distance between the two call graphs: {distance}")
            similarity_percentage = compare_call_graphs_similarity(callgraph_file_previous, callgraph_file_current)
            print(f"Similarity percentage between the two call graphs: {similarity_percentage:.2f}%")

        except FileNotFoundError:
            print(f"Config file {config_file} not found.")
        except KeyError:
            print("Invalid or incomplete config file format.")
        except Exception as e:
            print(f"An error occurred: {e}")

    elif visualization_type == "2":
        callgraph_file = input("Enter the call graph file name: ")
        G = process_call_graph(callgraph_file)
        metrics = calculate_metrics(G)
        visualize_graph(G, metrics)
    else:
        print("Invalid visualization type.")
