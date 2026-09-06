"""
Module for core classes.
"""

import numpy as np


class OptimizationMethod:
    """
    Core class for Optimization Methods.
    """

    def __init__(self, use_linear_search: bool = False):
        self.use_linear_search = use_linear_search

    def find_minimum(
        self, function: TestFunction, starting_point: np.ndarray, params: dict[str, any]
    ):
        raise NotImplementedError("This method should be overridden")


class LineSearchMethod(OptimizationMethod):
    """
    Core class when using any method which uses Line Search.
    Is a child of class OptimizationMethod.
    """

    def __init__(self, use_linear_search: bool = True):
        super().__init__(use_linear_search)
        self.evaluation_numbers = [0, 0, 0]  # val, gradient, hessian
        self.line_step_function = None

    def calculate_step_size(self, **kwargs):
        raise NotImplementedError("Calculate step size method should be overridden")

    def find_minimum(
        self,
        eval_function: TestFunction,
        starting_point: np.ndarray,
        params: dict[str, any],
    ):
        raise NotImplementedError("Calculate step size method should be overridden")

    def set_line_step_function(self, ls_function: TestFunction):
        # Sets linear step function
        self.linear_step_function = ls_function

    def calculate_step_size(
        self,
        input_function: TestFunction,
        direction: np.ndarray,
        params: dict[str, any],
    ):
        # NOTE. Dumb, I know.
        return self.linear_step_function(input_function, direction, params)


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
