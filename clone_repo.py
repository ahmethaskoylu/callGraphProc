import subprocess
import shutil
import os
import time

def count_lines_of_code(repo_name):
    c_files = subprocess.check_output(["find", repo_name, "-name", "*.c"]).decode("utf-8").strip().split("\n")

    total_lines = 0
    for c_file in c_files:
        # Use wc command to count lines in each file
        line_count_output = subprocess.check_output(["wc", "-l", c_file]).decode("utf-8").strip()
        # Extract the line count from the output
        lines = int(line_count_output.split()[0])
        total_lines += lines

    return total_lines

def fetch_github_repo(repo_url, commit_hashes=None):
    start_time = time.time()

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

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")

    return repo_name

if __name__ == "__main__":
    repo_url = input("Enter the GitHub repository URL: ")
    commit_hashes = input("Enter the commit hashes (oldest to newest one) (optional, separated by spaces): ")
    commit_hashes = commit_hashes.split() if commit_hashes else None
    repo_name = fetch_github_repo(repo_url, commit_hashes)
    print(f"Repository {repo_name} has been cloned.")
    # Count lines of code
    total_lines = count_lines_of_code(repo_name)
    print(f"Total lines of code in .c files: {total_lines}")

#https://github.com/Chetan496/cpp-algortihms
#bf28bdf7a2d32050d7369d933e2de1cff4c8988e
#4fb2dbd7e30efe882c4f867fcaab149e69698dee

#https://github.com/Theemiss/simple_shell
#newest
#51082d48358afec10f5d86f8153781fc1fe9b6a7
#oldest
#4112ae1221a7c5ad732161e60b79b92d151ff05d

#https://github.com/emirhancavusoglu/cLang2
#newest
#3f5bf70084ab165fd9fcd0b815b4cf34cfe30e34
#oldest
#28a9821247808f80f92d57db18b6fd469224b749

