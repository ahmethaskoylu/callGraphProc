import subprocess

def fetch_github_repo(repo_url, commit_hash=None):
    # Clone the repo
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    subprocess.run(["git", "clone", repo_url])

    if commit_hash:
        subprocess.run(["git", "-C", repo_name, "checkout", commit_hash])

    return repo_name
