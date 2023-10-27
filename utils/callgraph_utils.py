import subprocess
import networkx as nx

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

    return G  # Return the processed graph
