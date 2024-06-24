import subprocess
import os
import re
import pkg_resources

def convert_notebooks_to_scripts(directory):
    """
    Converts all Jupyter notebooks (.ipynb) in the specified directory to Python scripts (.py) using jupytext.

    Args:
        directory (str): The root directory to search for Jupyter notebooks.

    Returns:
        None
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.ipynb'):
                notebook_path = os.path.join(root, file)
                subprocess.run(['jupytext', '--to', 'py', notebook_path], check=True)

def extract_imports_from_py(file_path):
    """
    Extracts all import statements from a Python file, trying multiple encodings.

    Args:
        file_path (str): The path to the Python file.

    Returns:
        list: A list of imported module names.
    """
    encodings = ['utf-8', 'latin1', 'iso-8859-1']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                content = file.read()
            return re.findall(r'^\s*(?:import|from)\s+([^\s.]+)', content, re.MULTILINE)
        except (UnicodeDecodeError, FileNotFoundError):
            continue
    print(f"Could not read file {file_path} with available encodings.")
    return []

def gather_imports(directory):
    """
    Gathers all unique import statements from Python files in the specified directory.

    Args:
        directory (str): The root directory to search for Python files.

    Returns:
        set: A set of imported module names.
    """
    imports = set()
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                imports.update(extract_imports_from_py(os.path.join(root, file)))
    return imports

def filter_third_party_imports(imports):
    """
    Filters out standard library imports, retaining only third-party imports.

    Args:
        imports (set): A set of imported module names.

    Returns:
        set: A set of third-party imported module names.
    """
    installed_packages = {pkg.key for pkg in pkg_resources.working_set}
    third_party_imports = {imp for imp in imports if imp in installed_packages}
    return third_party_imports

def write_requirements_in(imports, filename='requirements.in'):
    """
    Writes the third-party imports to a requirements.in file.

    Args:
        imports (set): A set of third-party imported module names.
        filename (str): The name of the output file (default is 'requirements.in').

    Returns:
        None
    """
    with open(filename, 'w') as file:
        for imp in sorted(imports):
            file.write(f"{imp}\n")

def generate_requirements_txt():
    """
    Orchestrates the process of converting notebooks to scripts, gathering imports,
    filtering third-party imports, writing them to requirements.in, and generating
    requirements.txt using pip-compile.

    Args:
        None

    Returns:
        None
    """
    directory = '.'
    convert_notebooks_to_scripts(directory)
    imports = gather_imports(directory)
    third_party_imports = filter_third_party_imports(imports)
    write_requirements_in(third_party_imports)
    subprocess.run(['pip-compile', '--no-annotate', '--strip-extras'], check=True)

if __name__ == "__main__":
    generate_requirements_txt()

"""
Instructions:

1. Ensure you have the required packages installed in your Python environment:
   - jupytext
   - pip-tools

   You can install them using pip:
   ```
   pip install jupytext pip-tools
   ```

2. Save this script to a file, for example, `generate_requirements.py`.

3. Run the script:
   ```
   python generate_requirements.py
   ```

This will:
1. Convert all Jupyter notebooks (.ipynb) in the current directory to Python scripts (.py).
2. Gather all import statements from these Python scripts.
3. Filter out standard library imports to retain only third-party imports.
4. Write these third-party imports to a `requirements.in` file.
5. Use pip-compile to generate a `requirements.txt` file.
"""