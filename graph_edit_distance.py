import networkx as nx
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
def calculate_edit_distance(graph1, graph2):
    # Eklenen düğümleri bulmak için iki grafın farkını al
    added_nodes = set(graph2.nodes) - set(graph1.nodes)
    removed_nodes = set(graph1.nodes) - set(graph2.nodes)

    return added_nodes, removed_nodes
def compare_call_graphs_similarity(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        content1 = f1.read()
        content2 = f2.read()

    distance = Levenshtein.distance(content1, content2)
    max_len = max(len(content1), len(content2))

    similarity_percentage = ((max_len - distance) / max_len) * 100
    return similarity_percentage

if __name__ == "__main__":
    try:
        # İki dosya adını kullanıcıdan al
        file1 = input("Enter the first call graph file name (previous txt): ")
        file2 = input("Enter the second call graph file name (current txt): ")

        # Çağrı grafiklerini oluştur
        G1 = process_call_graph(file1)
        G2 = process_call_graph(file2)

        # Edit mesafesini hesapla
        added_nodes, removed_nodes = calculate_edit_distance(G1, G2)

        # Görselleştirme için benzerlik yüzdesini hesapla
        similarity_percentage = compare_call_graphs_similarity(file1, file2)
        print(f"Similarity percentage between the two call graphs: {similarity_percentage:.2f}%")

        # Eklenen ve çıkan düğümleri ekrana yazdır
        print("Added Nodes:", added_nodes)
        print("Removed Nodes:", removed_nodes)
    except FileNotFoundError:
        print("One or both of the call graph files not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
