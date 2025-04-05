# Project Structure Generator

A simple Python script to create directory and file structures based on a text definition file.

## Input File

The script reads a text file that defines the desired project structure using indentation.

*   **Default Name:** `structure_definition.txt`
*   By default, the script looks for `structure_definition.txt` in the same directory where the script (`create_structure.py` - rename yours accordingly) is located. You can provide a path to a different file as an argument.
*   **Format:**
    *   Use indentation (spaces or tabs) to define hierarchy.
    *   Lines ending with `/` are explicitly treated as directories.
    *   Lines containing `.` (and not just `.` at the start) are generally treated as files.
    *   Lines starting with `#`, or content after `#` on a line, are ignored as comments.

**How to Create `structure_definition.txt`:**

Create a plain text file (UTF-8 encoding is recommended) named `structure_definition.txt` (or any name you prefer) in your project or script directory. Define your structure like this:

```txt
my_cool_project/
    ├── README.md
    ├── requirements.txt    # foo
    ├── .gitignore          # blah-blah
    ├── src/
    │   ├── __init__.py
    │   ├── main.py
    │   ├── core/
    │   │   ├── __init__.py
    │   │   └── logic.py
    │   └── utils/
    │       ├── __init__.py
    │       └── helpers.py
    ├── tests/
    │   ├── __init__.py
    │   └── test_logic.py
    ├── docs/
    │   └── index.md
    └── data/
        └── raw/
        └── processed/