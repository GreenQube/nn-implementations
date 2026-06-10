"""
Module for core classes. NOTE. Need, OPT method, OPT Method, OPT Controller - used for the Optimization process
"""


class OptimizationMethod:
    def __init__(self, use_linear_search: bool = False):
        self.use_linear_search = use_linear_search

    def find_minimum(self, function, starting_point, params):
        raise NotImplementedError("This method should be overridden")


class LineSearchMethod(OptimizationMethod):
    def __init__(self, use_linear_search: bool = True):
        super().__init__(use_linear_search)
        self.evaluation_numbers = [0, 0, 0]  # val, gradient, hessian

    def calculate_step_size(self, **kwargs):
        raise NotImplementedError("Calculate step size method should be overridden")

    def find_minimum(self, eval_function, starting_point, params):
        raise NotImplementedError("Calculate step size method should be overridden")


# test functions class
class TestFunction:
    def calculate(
        self, value: bool = False, gradient: bool = False, hessian: bool = False
    ):
        raise NotImplementedError("This method should be overridden")

    def starting_points(self, starting_value: int | float | list):
        raise NotImplementedError("This method should be overridden")
