import os
import fnmatch
import logging
from typing import Set, List, Iterator, TextIO, Tuple

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

DEFAULT_IGNORE_PATTERNS = {'.yallaignore', 'output.txt'}
DEFAULT_IGNORE_FILE = '.yallaignore'
DEFAULT_OUTPUT_FILE = 'output.txt'

def read_file_lines(file_path: str) -> list[str]:
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.readlines()


def read_file_content(filepath: str) -> str:
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def write_to_file(filepath: str, content: str) -> None:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def is_valid_pattern_line(line: str) -> bool:
    return bool(line.strip() and not line.startswith('#'))

def extract_patterns_from_file(file_content: list[str]) -> Set[str]:
    return {line.strip() for line in file_content if is_valid_pattern_line(line)}

def get_ignore_patterns(ignore_file: str = DEFAULT_IGNORE_FILE) -> Set[str]:
    patterns = set(DEFAULT_IGNORE_PATTERNS)
    if os.path.exists(ignore_file):
        file_lines = read_file_lines(ignore_file)
        patterns.update(extract_patterns_from_file(file_lines))
    return patterns

def get_path_components(path: str) -> Tuple[str, str]:
    return os.path.basename(path), os.path.relpath(path)

def matches_any_pattern(path_components: Tuple[str, str], patterns: Set[str]) -> bool:
    name, rel_path = path_components
    return any(
        fnmatch.fnmatch(name, pattern) or fnmatch.fnmatch(rel_path, pattern)
        for pattern in patterns
    )

def should_ignore(path: str, patterns: Set[str]) -> bool:
    path_components = get_path_components(path)
    return matches_any_pattern(path_components, patterns)

def get_directory_path(root: str, dir_name: str) -> str:
    return os.path.join(root, dir_name)

def filter_directories(dirs: List[str], root: str, ignore_patterns: Set[str]) -> List[str]:
    return [
        dir_name for dir_name in dirs
        if not should_ignore(get_directory_path(root, dir_name), ignore_patterns)
    ]

def update_directories_list(dirs: List[str], filtered_dirs: List[str]) -> None:
    dirs.clear()
    dirs.extend(filtered_dirs)

def calculate_depth(root: str, base_directory: str) -> int:
    return root.count(os.sep) - base_directory.count(os.sep)

def create_tree_entry(name: str, indent: str, is_directory: bool = False) -> str:
    suffix = '/' if is_directory else ''
    return f"{indent}- {name}{suffix}"

def get_non_ignored_files(root: str, files: List[str], ignore_patterns: Set[str]) -> List[str]:
    return [
        filename for filename in files
        if not should_ignore(os.path.join(root, filename), ignore_patterns)
    ]

def generate_tree_lines(directory: str, ignore_patterns: Set[str]) -> List[str]:
    tree_lines = []
    
    for root, dirs, files in os.walk(directory):
        filtered_dirs = filter_directories(dirs, root, ignore_patterns)
        update_directories_list(dirs, filtered_dirs)
        
        indent = '  ' * calculate_depth(root, directory)
        
        # Add directory entries
        tree_lines.extend(create_tree_entry(d, indent, True) for d in dirs)
        
        # Add file entries
        non_ignored_files = get_non_ignored_files(root, files, ignore_patterns)
        tree_lines.extend(create_tree_entry(f, indent) for f in non_ignored_files)
    
    return tree_lines

def format_file_content(filepath: str, content: str) -> str:
    relative_path = os.path.relpath(filepath)
    return f"# {relative_path}\n{content}\n\n"

def process_single_file(outfile: TextIO, filepath: str) -> None:
    try:
        content = read_file_content(filepath)
        formatted_content = format_file_content(filepath, content)
        outfile.write(formatted_content)
    except Exception as e:
        logging.error(f"Error reading {filepath}: {str(e)}")

def process_files(outfile: TextIO, directory: str, ignore_patterns: Set[str]) -> None:
    for root, dirs, files in os.walk(directory):
        filtered_dirs = filter_directories(dirs, root, ignore_patterns)
        update_directories_list(dirs, filtered_dirs)
        
        for filename in files:
            filepath = os.path.join(root, filename)
            if not should_ignore(filepath, ignore_patterns):
                process_single_file(outfile, filepath)

def generate_output_content(directory: str, ignore_patterns: Set[str]) -> str:
    tree_lines = generate_tree_lines(directory, ignore_patterns)
    return f"File Tree:\n{os.linesep.join(tree_lines)}\n\n"

def process_directory_contents(output_file: str, directory: str, ignore_patterns: Set[str]) -> None:
    try:
        with open(output_file, 'w', encoding='utf-8') as outfile:
            content = generate_output_content(directory, ignore_patterns)
            outfile.write(content)
            process_files(outfile, directory, ignore_patterns)
        logging.info(f"Combined files into '{output_file}'")
    except Exception as e:
        logging.error(f"Error combining files: {str(e)}")

def main() -> None:
    current_directory = os.getcwd()
    ignore_patterns = get_ignore_patterns()
    process_directory_contents(DEFAULT_OUTPUT_FILE, current_directory, ignore_patterns)

if __name__ == '__main__':
    main()
