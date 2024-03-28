import re
from collections import defaultdict
import heapq


def build_graph_from_file(file_path):
    graph = defaultdict(dict)
    with open(file_path, 'r') as f:
        for line in f:
            src, _, dest = line.strip().partition(' -> ')
            graph[src][dest] = 1  # Ağırlık varsayılan olarak 1
            if dest not in graph:  # Hedef düğüm grafiğe eklenirse
                graph[dest] = {}
    return graph


def dijkstra(graph, start, end, stop_functions):
    distances = {vertex: float('infinity') for vertex in graph}
    previous = {vertex: None for vertex in graph}
    distances[start] = 0
    pq = [(0, start)]

    while pq:
        current_distance, current_vertex = heapq.heappop(pq)

        if current_vertex == end:
            break

        for neighbor, weight in graph[current_vertex].items():
            # Stop if the current node is any of the stop functions
            if neighbor in stop_functions:
                break

            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_vertex
                heapq.heappush(pq, (distance, neighbor))

    # Yolu geriye doğru izle
    path = []
    current_vertex = end
    while current_vertex is not None:
        path.append(current_vertex)
        current_vertex = previous[current_vertex]
    path.reverse()

    return path, distances[end]


if __name__ == "__main__":
    file_path = input("Basitleştirilmiş call graph dosyasının yolu: ")
    graph = build_graph_from_file(file_path)

    start_vertex = input("Başlangıç düğümü: ")
    end_vertex = input("Bitiş düğümü: ")

    # List of stop functions
    stop_functions = ["free()", "malloc()", "calloc()"]

    path, distance = dijkstra(graph, start_vertex, end_vertex, stop_functions)

    if distance == float('infinity'):
        print(f"{end_vertex} düğümüne ulaşılamıyor.")
    else:
        print(f"{start_vertex} ile {end_vertex} arası en kısa yol: {' -> '.join(path)}, Uzunluk: {distance}")

