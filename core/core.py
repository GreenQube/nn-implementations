"""
Module for core classes.
"""

import numpy as np


class OptimizationMethod:
    """
    Core class for Optimization Methods.
    """

    def __init__(self, use_line_search: bool = False):
        self.use_line_search = use_line_search

    def find_minimum(
        self, function: TestFunction, starting_point: np.ndarray, params: dict[str, any]
    ):
        raise NotImplementedError("This method should be overridden")


class LineSearchMethod(OptimizationMethod):
    """
    Core class when using any method which uses Line Search.
    Is a child of class OptimizationMethod.
    """

    def __init__(self, use_line_search: bool = True):
        super().__init__(use_line_search)
        self.evaluation_numbers = [0, 0, 0]  # val, gradient, hessian
        self.line_step_function = None

    def set_line_step_function(self, ls_function: TestFunction):
        # Sets line step function
        self.line_step_function = ls_function

    def calculate_step_size(
        self,
        input_function: TestFunction,
        direction: np.ndarray,
        params: dict[str, any] | None = None,
    ):
        # Set new parameters if provided
        if params is not None:
            self.line_step_function.set_parameters(params)
        return self.line_step_function.calculate_function(input_function, direction)


class TestFunction:
    """
    Core class when making a Function Class which are used
    for testing methods.
    """

    def calculate(
        self, value: bool = False, gradient: bool = False, hessian: bool = False
    ):
        """

        Args:
            value (bool, optional): Flag if the value of the function needs to be calculated.
                                    Defaults to False.
            gradient (bool, optional): Flag if the gradient of the function needs to be calculated.
                                       Defaults to False.
            hessian (bool, optional): Flag if the hessian of the function needs to be calculated.

                                      Defaults to False.

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError("This method should be overridden")

    def starting_points(self, input_array: np.ndarray | int | tuple):
        raise NotImplementedError("This method should be overridden")


class LineSearchFunction:
    def __init__(self, parameters: dict[str, str]):
        temp_params = {}
        for k, v in parameters.items():
            temp_params[k] = float(v)
        self.parameters = temp_params
        self.default_step = 1.0

    def calculate_function(self, input_functon: TestFunction, direction: np.ndarray):
        raise NotImplementedError("This method should be overridden")

    def get_parameters(self):  # NOTE. might not even need this lol
        return self.parameters

    def set_parameters(self, new_params: dict[str, any]):
        temp_params = {}
        for k, v in new_params.items():
            temp_params[k] = float(v)
        self.parameters = temp_params
