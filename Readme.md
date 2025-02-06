# Yalla - Project to LLM Aggregator 📁

a Python script to prepare your project for LLM interactions. Yalla generates a single-file view, including the directory structure, helping LLMs in understanding the project's context and file structure for more accurate responses.

## How doe it work

Yalla walks through your project directory and:

1. Creates a visual tree of your project structure
2. Combines the contents of all text files into a single output file
3. Follows project's ignore patterns (similar to .gitignore)

## Basic Usage

```
# creates output.txt in current directory
python yalla.py

# Specify custom output file
python yalla.py -o my_output.txt # or --output

# Default behavior (creates output.txt ignoring .yallaignore patterns)
python yalla.py

# Include .gitignore patterns in addition to .yallaignore
python yalla.py -g  # or --gitignore

# Help
python yalla.py -h ## or --help
```

*It is reccomended to add `yalla.py` directory to PATH so that you can run simply *yalla\* from wherever you want.

## Ignore Patterns

By default, Yalla looks for a `.yallaignore` file in your project root. The syntax is similar to .gitignore:

- Each line represents one pattern
- Lines starting with # are comments
- Empty lines are skipped
- Add / at the end of a pattern to match directories only
- Supports standard glob patterns (\* and ?)

Default ignored files:

- Any hidden folder in your OS
- `.yallaignore`
- `output.txt`

## Requirements

- Python 3.x
- std only, no other libraries needed

## Output Format

The generated file includes:

```
Directory Structure:
  folder1/
    - file1.txt
    - file2.py
  folder2/
    subfolder/
      - file3.js

# folder1/file1.txt
[content of file1.txt]

# folder1/file2.py
[content of file2.py]
...
```

## Why "Yalla"? 😎

Because sometimes you just need to get all your code together quickly - yalla! (Hebrew for "let's go" or "hurry up")
