"""
Module for core classes. NOTE. Need, OPT method, OPT Method, OPT Controller - used for the Optimization process
"""
from utils.utils import get_classes_from_file, get_functions_from_file


class OptimizationMethod:
    def find_minimum(self, function, starting_point, params):
        raise NotImplementedError("This method should be overridden")
    
# test functions class
class TestFunction:
    def calculate(self, value:bool = False, gradient:bool = False, hessian:bool = False):
        raise NotImplementedError("This method should be overridden")
    def starting_points(self, starting_value: int | float | list):
        raise NotImplementedError("This method should be overridden")
        