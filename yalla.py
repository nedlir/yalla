import os
import fnmatch
import logging
from typing import Set, List

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Constants
DEFAULT_IGNORE_PATTERNS = {'.yallaignore', 'output.txt'}
DEFAULT_IGNORE_FILE = '.yallaignore'
DEFAULT_OUTPUT_FILE = 'output.txt'

def read_ignore_file(ignore_file: str = DEFAULT_IGNORE_FILE) -> Set[str]:
    patterns = set(DEFAULT_IGNORE_PATTERNS)
    if os.path.exists(ignore_file):
        with open(ignore_file, 'r', encoding='utf-8') as f:
            valid_lines = (
                line.strip() 
                for line in f 
                if line.strip() and not line.startswith('#')
            )
            patterns.update(valid_lines)
    return patterns

def should_ignore(path: str, patterns: Set[str]) -> bool:
    name = os.path.basename(path)
    rel_path = os.path.relpath(path)
    return any(
        fnmatch.fnmatch(name, pattern) or fnmatch.fnmatch(rel_path, pattern)
        for pattern in patterns
    )

def get_non_ignored_directories(dirs: List[str], root: str, ignore_patterns: Set[str]) -> List[str]:
    return [
        dir_name 
        for dir_name in dirs 
        if not is_directory_ignored(dir_name, root, ignore_patterns)
    ]

def is_directory_ignored(dir_name: str, root: str, ignore_patterns: Set[str]) -> bool:
    dir_path = os.path.join(root, dir_name)
    return should_ignore(dir_path, ignore_patterns)

def generate_file_tree(directory: str, ignore_patterns: Set[str]) -> str:
    tree_lines = []
    
    for root, dirs, files in os.walk(directory):
        # Filter directories
        non_ignored_dirs = get_non_ignored_directories(dirs, root, ignore_patterns)
        dirs.clear()
        dirs.extend(non_ignored_dirs)

        # Calculate indentation
        depth = root.count(os.sep) - directory.count(os.sep)
        indent = '  ' * depth
        
        # Add directory entries
        tree_lines.extend(f"{indent}- {dir_name}/" for dir_name in dirs)
        
        # Add non-ignored file entries
        non_ignored_files = [
            f"{indent}- {filename}" 
            for filename in files 
            if not should_ignore(os.path.join(root, filename), ignore_patterns)
        ]
        tree_lines.extend(non_ignored_files)

    return '\n'.join(tree_lines)

def write_file_content(outfile, filepath: str) -> None:
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
            relative_path = os.path.relpath(filepath)
            outfile.write(f"# {relative_path}\n")
            outfile.write(infile.read() + '\n\n')
    except Exception as e:
        logging.error(f"Error reading {filepath}: {str(e)}")

def process_directory(outfile, directory: str, ignore_patterns: Set[str]) -> None:
    for root, dirs, files in os.walk(directory):
        # Filter directories
        non_ignored_dirs = get_non_ignored_directories(dirs, root, ignore_patterns)
        dirs.clear()
        dirs.extend(non_ignored_dirs)

        # Process non-ignored files
        for filename in files:
            filepath = os.path.join(root, filename)
            if not should_ignore(filepath, ignore_patterns):
                write_file_content(outfile, filepath)

def main() -> None:
    output_file = DEFAULT_OUTPUT_FILE
    current_directory = os.getcwd()
    ignore_patterns = read_ignore_file()
    
    try:
        with open(output_file, 'w', encoding='utf-8') as outfile:
            # Generate and write file tree
            file_tree = generate_file_tree(current_directory, ignore_patterns)
            outfile.write(f"File Tree:\n{file_tree}\n\n")
            
            # Process and write file contents
            process_directory(outfile, current_directory, ignore_patterns)
            
        logging.info(f"Combined files into '{output_file}'")
    except Exception as e:
        logging.error(f"Error combining files: {str(e)}")

if __name__ == '__main__':
    main()
