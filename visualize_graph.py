import networkx as nx
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('MacOSX')

def process_call_graph(callgraph_file):
    G = nx.DiGraph()  # Create a directed graph

    with open(callgraph_file, 'r') as f:
        lines = f.readlines()

    stack = []
    for line in lines:
        level = len(line) - len(line.lstrip())
        func_name = line.strip().split()[0]

        while len(stack) > level:  # Remove deeper or same level items
            stack.pop()

        if stack:  # if stack is not empty, there is a parent
            G.add_edge(stack[-1], func_name)

        stack.append(func_name)

    return G

def visualize_graph(G, metrics):
    pos = nx.shell_layout(G)
    node_sizes = [metrics[node] * 5000 for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, alpha=0.6)
    labels = {node: f"{node}\n({metrics[node]:.2f})" for node in G.nodes()}  # Add metric value to label
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8)
    nx.draw_networkx_edges(G, pos, width=0.5, alpha=0.6)
    plt.figure(figsize=(12, 12))
    plt.show()

def calculate_metrics(G):
    degree_centrality = nx.degree_centrality(G)
    return degree_centrality

if __name__ == "__main__":
    callgraph_file = input("Enter the call graph file name: ")
    G = process_call_graph(callgraph_file)
    metrics = calculate_metrics(G)
    visualize_graph(G, metrics)
    print(metrics)
