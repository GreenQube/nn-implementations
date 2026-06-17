"""
Module for util functions
"""

import ast
import numpy as np
from numpy.linalg import inv
import os
import inspect
import json

UTILS_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_PATH = os.path.dirname(UTILS_PATH)


def listdir(dir_path: str):
    """
    TODO.
    """
    return [x for x in os.listdir(dir_path) if "pycache" not in x]


def get_functions_from_file(filepath: str) -> dict[str, str]:
    """

    Get all of the functions from a python file.

    Args:
        filepath (str): _description_

    Returns:
        dict[str, str]: _description_
    """
    with open(filepath, "r") as f:
        source = f.read()

    namespace = {}
    exec(compile(source, filepath, "exec"), namespace)

    return {name: obj for name, obj in namespace.items() if inspect.isfunction(obj)}


def get_classes_from_file(filepath: str) -> dict[str, str]:
    """
    TODO.
    Get all of the classes from a python file.

    Args:
        filepath (str): _description_

    Returns:
        dict[str, str]: _description_
    """
    with open(filepath, "r") as f:
        source = f.read()

    namespace = {}
    exec(compile(source, filepath, "exec"), namespace)
    all_classes_dict = {
        name: (obj, obj.__bases__)
        for name, obj in namespace.items()
        if inspect.isclass(obj)
    }
    parent_classes = []
    for value in all_classes_dict.values():
        parent_classes += list(value[1])
    return {
        key: value[0]
        for key, value in all_classes_dict.items()
        if value[0] not in parent_classes
    }


def get_test_functions(use_classes: bool = True) -> dict[str, str]:  # NOTE. IMPORTANT
    """NOTE"""
    get_test_functions_path = os.path.join(PROJECT_PATH, "functions", "functions.py")
    if use_classes:
        return get_classes_from_file(get_test_functions_path)
    else:
        return get_functions_from_file(get_test_functions_path)


def get_line_search_methods():
    """NOTE"""
    get_test_functions_path = os.path.join(
        PROJECT_PATH, "core", "line_search_methods.py"
    )
    return get_functions_from_file(get_test_functions_path)


def get_optimization_methods(method_name: str) -> dict[str, str]:
    """NOTE"""
    methods_dir = os.path.join(PROJECT_PATH, "methods")
    method_group_names = [name[:-3] for name in listdir(methods_dir)]

    mg_string = (",").join(method_group_names)
    assert (
        method_name in method_group_names,
        f"You've provided a bad method, the methods available are: {mg_string}",
    )

    method_path = os.path.join(methods_dir, method_name + ".py")
    return get_classes_from_file(method_path)


def get_all_optimization_methods():  # NOTE. IMPORTANT
    """NOTE"""
    methods_dir = os.path.join(PROJECT_PATH, "methods")
    all_methods = [method[:-3] for method in listdir(methods_dir)]
    print(all_methods)
    return {method: get_optimization_methods(method) for method in all_methods}


def get_gui_configs():
    """NOTE"""
    gui_config_path = os.path.join(PROJECT_PATH, "gui_config.json")
    with open(gui_config_path, "r") as f:
        mappings = json.load(f)

    return mappings


def map_fancier_strings(values: list, all_caps: bool = False):
    """NOTE"""
    mappings = {}
    for value in values:
        fancy_values = value.split("_")
        fancy_values = [f[0].upper() + f[1:] for f in fancy_values]
        fancy_value = "".join(fancy_values)
        if all_caps:
            fancy_value = fancy_value.upper()
        mappings[value] = fancy_value

    return mappings


def map_fancier_dict_keys(input_dict: dict[str, str], all_caps: bool = False):
    fancy_key_mappings = map_fancier_strings(list(input_dict.keys()), all_caps=all_caps)
    return {
        fancy_key_mappings[key]: (key, input_dict[key]) for key in input_dict.keys()
    }


def get_array_inv(input_array: np.ndarray):
    # check if the array is diagonal:
    # Create a copy and zero out the main diagonal
    off_diagonal_elements = input_array.copy()
    np.fill_diagonal(off_diagonal_elements, 0)

    # If all remaining elements are 0, it's a diagonal matrix
    if np.count_nonzero(off_diagonal_elements) == 0:
        if input_array.dtype != np.float64:
            input_array = input_array.astype(np.float64)
        reciprocal = np.reciprocal(input_array)
        inverse = np.where(~np.isinf(reciprocal), reciprocal, 0.0)
        return inverse
    else:
        inverse = inv(input_array)
        return inverse
