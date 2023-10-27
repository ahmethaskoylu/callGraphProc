import clone_repo
from clone_repo import *

def generate_call_graph(repo_name, entry_file):
    output = subprocess.check_output(["cflow", f"{repo_name}/{entry_file}"])
    with open(f"{repo_name}_callgraph.txt", "wb") as f:
        f.write(output)
    return f"{repo_name}_callgraph.txt"

if __name__ == "__main__":
    repo_name = clone_repo.clone_github_repo(clone_repo.repo_url)
    entry_file = "fibonacci.c"  # Çağrı grafiği oluşturulacak giriş dosyası
    callgraph_file = generate_call_graph(repo_name, entry_file)
