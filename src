# This is a sample Python script.



import subprocess
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('MacOSX')



def fetch_github_repo(repo_url, commit_hash=None):
    # Clone the repo
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    subprocess.run(["git", "clone", repo_url])

    # Checkout to a specific commit if provided
    if commit_hash:
        subprocess.run(["git", "-C", repo_name, "checkout", commit_hash])

    return repo_name

def generate_call_graph(repo_name, entry_file):
    output = subprocess.check_output(["cflow", f"{repo_name}/{entry_file}"])
    with open(f"{repo_name}_callgraph.txt", "wb") as f:
        f.write(output)
    return f"{repo_name}_callgraph.txt"


def process_call_graph(callgraph_file):
    G = nx.DiGraph()
    stack = []  # This will help us keep track of function hierarchy

    with open(callgraph_file, 'r') as f:
        for line in f:
            stripped = line.rstrip()
            indent = len(line) - len(stripped)  # Calculate the whitespace at the start
            function_name = stripped.split(" ")[0]  # Get the function name from the stripped line

            # If the stack is empty or the indent has increased, we just add to the stack
            if not stack or indent > stack[-1][1]:
                stack.append((function_name, indent))
            else:
                while stack and indent <= stack[-1][1]:
                    stack.pop()
                stack.append((function_name, indent))

            # If there are at least two functions in the stack, add an edge
            if len(stack) > 1:
                G.add_edge(stack[-2][0], stack[-1][0])

    # Visualize
    pos = nx.spring_layout(G)  # Positioning of nodes
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=10, width=2, edge_color="gray")
    plt.savefig("graph_output.png")
    #print("Nodes:", G.nodes())
    #print("Edges:", G.edges())

    return G



def calculate_metrics(G):
    # Degree centrality as a simple metric
    degree_centrality = nx.degree_centrality(G)
    return degree_centrality

def main():
    repo_url = "https://github.com/Chetan496/cpp-algortihms.git"
    repo_name = fetch_github_repo(repo_url)
    callgraph_file = generate_call_graph(repo_name, "heapSort.c")
    G = process_call_graph(callgraph_file)
    metrics = calculate_metrics(G)
    print(metrics)

if __name__ == "__main__":
    main()






