from utils.callgraph_utils import *
from utils.github_utils import *
from utils.metrics_utils import *
from utils.visualization_utils import *

def main():
    repo_url = "https://github.com/Chetan496/cpp-algortihms.git"
    repo_name = fetch_github_repo(repo_url)
    callgraph_file = generate_call_graph(repo_name, "fibonacci.c")
    G = process_call_graph(callgraph_file)
    metrics = calculate_metrics(G)
    visualize_graph(G, metrics)  # Pass both G and metrics to the function
    print(metrics)


if __name__ == "__main__":
    main()
