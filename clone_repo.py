import subprocess

def fetch_github_repo(repo_url, commit_hash=None):
    # Clone the repo
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    subprocess.run(["git", "clone", repo_url])

    if commit_hash:
        subprocess.run(["git", "-C", repo_name, "checkout", commit_hash])

    return repo_name

if __name__ == "__main__":
    repo_url = input("Enter the GitHub repository URL: ")
    commit_hash = input("Enter the commit hash (optional): ")
    repo_name = fetch_github_repo(repo_url, commit_hash)
    print(f"Repository {repo_name} has been cloned.")
