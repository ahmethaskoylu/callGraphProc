import subprocess
import shutil
import os


def fetch_github_repo(repo_url, commit_hashes=None):
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    subprocess.run(["git", "clone", repo_url])

    if commit_hashes:
        for commit_hash in commit_hashes:
            # Checkout the specific commit
            subprocess.run(["git", "-C", repo_name, "checkout", commit_hash])

            # Create a directory for this specific commit
            commit_dir = f"{repo_name}_{commit_hash}"
            if os.path.exists(commit_dir):
                shutil.rmtree(commit_dir)
            os.makedirs(commit_dir)

            # Copy the contents of the repo (excluding the .git folder) to the commit directory
            for item in os.listdir(repo_name):
                s = os.path.join(repo_name, item)
                d = os.path.join(commit_dir, item)
                if os.path.isdir(s):
                    if ".git" not in s:
                        shutil.copytree(s, d, False, None)
                else:
                    shutil.copy2(s, d)

            print(f"Repository content at commit {commit_hash} has been copied to {commit_dir}")

    return repo_name

#https://github.com/Chetan496/cpp-algortihms

if __name__ == "__main__":
    repo_url = input("Enter the GitHub repository URL: ")
    commit_hashes = input("Enter the commit hashes (optional, separated by spaces): ")
    commit_hashes = commit_hashes.split() if commit_hashes else None
    repo_name = fetch_github_repo(repo_url, commit_hashes)
    print(f"Repository {repo_name} has been cloned.")
