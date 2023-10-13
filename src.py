


import subprocess
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('MacOSX')



def fetch_github_repo(repo_url, commit_hash=None):
    # Clone the repo
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    subprocess.run(["git", "clone", repo_url])

    if commit_hash:
        subprocess.run(["git", "-C", repo_name, "checkout", commit_hash])

    return repo_name

def generate_call_graph(repo_name, entry_file):
    output = subprocess.check_output(["cflow", f"{repo_name}/{entry_file}"])
    with open(f"{repo_name}_callgraph.txt", "wb") as f:
        f.write(output)
    return f"{repo_name}_callgraph.txt"


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







def calculate_metrics(G):
    # Degree centrality as a simple metric
    degree_centrality = nx.degree_centrality(G)
    return degree_centrality

def main():
    repo_url = "https://github.com/Chetan496/cpp-algortihms.git"
    repo_name = fetch_github_repo(repo_url)
    callgraph_file = generate_call_graph(repo_name, "fibonacci.c")
    G = process_call_graph(callgraph_file)
    metrics = calculate_metrics(G)
    visualize_graph(G, metrics)  # Pass both G and metrics to the function
    print(metrics)
    #a



if __name__ == "__main__":
    main()






