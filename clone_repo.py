import subprocess

repo_url = "https://github.com/Chetan496/cpp-algortihms.git"


def clone_github_repo(repo_url, commit_hash=None):
    # Clone the repo
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    subprocess.run(["git", "clone", repo_url])

    if commit_hash:
        subprocess.run(["git", "-C", repo_name, "checkout", commit_hash])

    return repo_name

if __name__ == "__main__":

    repo_name = clone_github_repo(repo_url)
