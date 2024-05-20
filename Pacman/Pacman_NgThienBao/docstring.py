

import os
import ast
def extract_docstrings(folder_path, output_file):
    '''Extracts docstrings from all Python files in a folder and writes them to an output file.'''
    with open(output_file, 'w', encoding='utf-8') as file:
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                if file_name.endswith('.py'):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r', encoding='utf-8') as py_file:
                        try:
                            tree = ast.parse(py_file.read())
                            file.write(f"!!____________________File: {file_path}____________________!!\n")
                            for node in ast.walk(tree):
                                if isinstance(node, ast.ClassDef):
                                    docstring = ast.get_docstring(node)
                                    if docstring:
                                        file.write(f"****** Class: {node.name} ******\n")
                                        file.write(f"{docstring}\n\n")
                                        for subnode in ast.walk(node):
                                            if isinstance(subnode, ast.FunctionDef):
                                                sub_docstring = ast.get_docstring(subnode)
                                                if sub_docstring:
                                                    file.write(f"**Function: {subnode.name} **\n")
                                                    file.write(f"{sub_docstring}\n\n")
                                elif isinstance(node, ast.FunctionDef):
                                    docstring = ast.get_docstring(node)
                                    if docstring:
                                        file.write(f"**Function: {node.name} **\n")
                                        file.write(f"{docstring}\n\n")
                        except UnicodeDecodeError:
                            print(f"Cannot decode file: {file_path}")
                        except Exception as e:
                            print(f"Error processing file: {file_path}. Error: {str(e)}")

# Usage example
folder_path = 'D:\\DSA\\Pacman\\Pacman_NgThienBao'
output_file = 'D:\\DSA\\Pacman\\Pacman_NgThienBao\\docstrings.txt'
extract_docstrings(folder_path, output_file)



