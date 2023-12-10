import networkx as nx

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

def find_shortest_path(callgraph_file):
    G = process_call_graph(callgraph_file)

    # Otomatik olarak başlangıç ve bitiş düğümlerini belirle
    start_node = input("Enter the start node (or press Enter for automatic detection(main())): ")
    end_node = input("Enter the end node (or press Enter for automatic detection(main()): ")

    # Otomatik başlangıç ve bitiş düğümlerini belirle
    if not start_node:
        start_node = min(G.nodes, key=lambda node: G.in_degree(node))
        print(f"Start node automatically detected: {start_node}")

    if not end_node:
        end_node = max(G.nodes, key=lambda node: G.out_degree(node))
        print(f"End node automatically detected: {end_node}")

    try:
        # En kısa yol bul
        shortest_path = nx.shortest_path(G, source=start_node, target=end_node)
        shortest_path_length = nx.shortest_path_length(G, source=start_node, target=end_node)

        print(f"Shortest path from {start_node} to {end_node}: {shortest_path}")
        print(f"Length of the shortest path: {shortest_path_length}")

    except nx.NetworkXNoPath:
        print(f"No path found between {start_node} and {end_node}")

if __name__ == "__main__":
    try:
        # Kullanıcıdan callgraph dosyasını al
        callgraph_file = input("Enter the call graph txt file name: ")

        # Otomatik en kısa yolu bul
        find_shortest_path(callgraph_file)

    except FileNotFoundError:
        print("Call graph file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")