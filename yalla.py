import os

def generate_file_tree(directory):
    """Generate a tree structure of files in the given directory."""
    tree_lines = []
    
    for root, dirs, files in os.walk(directory):
        depth = root.count(os.sep) - directory.count(os.sep)
        indent = '  ' * depth
        
        # Add directories and files to the tree
        tree_lines.extend(f"{indent}- {d}/" for d in dirs)
        tree_lines.extend(f"{indent}- {f}" for f in files)

    return '\n'.join(tree_lines)

def write_to_output(outfile, content):

    outfile.write(content + '\n\n')

def combine_files(output_file):
    """Combine all files in the current directory into a single output file."""
    current_directory = os.getcwd()
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # write tree:
        file_tree = generate_file_tree(current_directory)
        write_to_output(outfile, f"File Tree:\n{file_tree}")
        
        # write contents of all files:
        for root, _, files in os.walk(current_directory):
            for filename in files:
                file_path = os.path.join(root, filename)
                if os.path.isfile(file_path):
                    write_to_output(outfile, f"# {filename}")
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                        write_to_output(outfile, infile.read())

def main():
    output_file = os.path.join(os.getcwd(), 'output.txt')
    combine_files(output_file)
    print(f"Combined files into '{output_file}' in the current directory.")

if __name__ == '__main__':
    main()