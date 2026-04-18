# import inspect
import numpy as np
import os
from utils.utils import get_test_functions

# x = inspect.getmembers(functions, inspect.isfunction)
# # x = dir(functions)
# print(type(x[0][0]))
# print(type(x[0][1]))
# print(x)
z = [1,1,1,1]
z = np.asarray(z)

# import json
# # Open and read the JSON file
# with open(r'E:/programming/ai_ml_master_projects/numerical_optimization_project/functions/function_names.json', 'r', encoding='utf-8') as file:
#     data = json.load(file)

# # Now 'data' is a Python dictionary or list
# print(data)

# import ast

# filename = r"functions/functions.py"
# with open(filename, "r") as file:
#     node = ast.parse(file.read())

# # Extracts both standard and async top-level functions
# x = [(n.name, n) for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
# print(x)

import ast
import inspect

def get_functions_from_file(filepath: str) -> list[tuple[str, object]]:
    with open(filepath, "r") as f:
        source = f.read()
    
    namespace = {}
    exec(compile(source, filepath, "exec"), namespace)
    
    return [
        (name, obj)
        for name, obj in namespace.items()
        if inspect.isfunction(obj)
    ]
    
filename = r"functions/functions.py"
a = get_functions_from_file(filename)
print(a)
x = a[0][1]
y = x(z)
print(y)

project_dir = os.path.dirname(os.path.abspath(__file__))
# print(project_dir)
get_test_functions()