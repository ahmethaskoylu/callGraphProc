import json


def process_call_graph(callgraph_file):
    G = {}
    with open(callgraph_file, 'r') as f:
        lines = f.readlines()

    stack = []
    for line in lines:
        level = len(line) - len(line.lstrip())
        func_name = line.strip().split()[0]
        while len(stack) > level:
            stack.pop()
        if stack:
            if stack[-1] not in G:
                G[stack[-1]] = {}
            G[stack[-1]][func_name] = 1  # Kenar ağırlığı varsayılan olarak 1
        stack.append(func_name)

    return G


def _shortest_path(G, start_node, end_node):
    visited = {start_node: 0}
    path = {}

    nodes = set(G.keys())

    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node

        if min_node is None:
            break

        nodes.remove(min_node)
        current_weight = visited[min_node]

        for neighbor in G[min_node]:
            weight = current_weight + G[min_node][neighbor]
            if neighbor not in visited or weight < visited[neighbor]:
                visited[neighbor] = weight
                path[neighbor] = min_node

    shortest_path, current_node = [], end_node
    while current_node != start_node:
        shortest_path.insert(0, current_node)
        current_node = path.get(current_node)
        if current_node is None:
            return None
    shortest_path.insert(0, start_node)

    return shortest_path


def find_shortest_path(callgraph_file):
    G = process_call_graph(callgraph_file)

    start_node = input("Enter the start node (or press Enter for automatic detection(main())): ")
    end_node = input("Enter the end node (or press Enter for automatic detection(main()): ")

    if not start_node:
        start_node = min(G, key=lambda node: len(G[node]))
        print(f"Start node automatically detected: {start_node}")

    if not end_node:
        end_node = max(G, key=lambda node: len(G[node]))
        print(f"End node automatically detected: {end_node}")

    try:
        shortest_path = _shortest_path(G, start_node, end_node)
        if shortest_path:
            print(f"Shortest path from {start_node} to {end_node}: {shortest_path}")
            print(f"Length of the shortest path: {len(shortest_path) - 1}")
        else:
            print(f"No path found between {start_node} and {end_node}")
    except KeyError:
        print(f"No path found between {start_node} and {end_node}")


if __name__ == "__main__":
    config_file = input("Enter the path to the configuration file (config.json): ")
    try:
        with open(config_file, 'r') as config_f:
            config = json.load(config_f)

        print("1- " + config["call_graphs"]["previous"])
        print("2- " + config["call_graphs"]["current"])

        choice = input("Enter the number of the call graph file you want to use: ")
        callgraph_file = config["call_graphs"]["current"] if choice == '2' else config["call_graphs"]["previous"]

        find_shortest_path(callgraph_file)

    except FileNotFoundError:
        print("Configuration file or call graph file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
