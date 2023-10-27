import clone_repo
from clone_repo import *

def find_commit_diff(repo_name, commit_id1, commit_id2):
    diff_output = subprocess.check_output(["git", "-C", repo_name, "diff", commit_id1, commit_id2])
    with open("commit_diff.txt", "wb") as f:
        f.write(diff_output)
    return f"{repo_name}_callgraph.txt"


if __name__ == "__main__":
    repo_name = clone_repo.clone_github_repo(clone_repo.repo_url)
    commit_id1 = "4fb2dbd7e30efe882c4f867fcaab149e69698dee"
    commit_id2 = "4137c8df0a21bdb8d0829dc0a1e4b3d73418b1d0"
    find_commit_diff(repo_name, commit_id1, commit_id2)
