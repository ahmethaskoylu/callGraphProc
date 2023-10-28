import subprocess

def generate_call_graph(repo_name):
    # Find all C files in the repo
    c_files = subprocess.check_output(["find", repo_name, "-name", "*.c"]).decode("utf-8").strip().split("\n")

    # Initialize an empty byte string to store the output
    output = b""

    # Generate the call graph for each C file
    for c_file in c_files:
        try:
            output += subprocess.check_output(["cflow", c_file])
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while processing {c_file}: {e}")

    # Write the output to a file
    callgraph_file = f"{repo_name}_callgraph.txt"
    with open(callgraph_file, "wb") as f:
        f.write(output)

    return callgraph_file

if __name__ == "__main__":
    repo_name = input("Enter the repository name: ")
    callgraph_file = generate_call_graph(repo_name)
    print(f"Call graph has been generated and saved to {callgraph_file}.")
