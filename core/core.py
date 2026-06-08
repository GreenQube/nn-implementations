"""
Module for core classes. NOTE. Need, OPT method, OPT Method, OPT Controller - used for the Optimization process
"""

from utils.utils import get_classes_from_file, get_functions_from_file
import time
from copy import copy
import numpy as np
from operator import add


class OptimizationMethod:
    def find_minimum(self, function, starting_point, params):
        raise NotImplementedError("This method should be overridden")


class LineSearchMethod(OptimizationMethod):
    def __init__(self):
        super().__init__()
        self.evaluation_numbers = [0, 0, 0]  # val, gradient, hessian

    def calculate_step_size(self, **kwargs):
        raise NotImplementedError("Calculate step size method should be overridden")

    def find_minimum(self, eval_function, starting_point, params):
        epsilon = params["epsilon"]  # get the epsilon
        max_iter = params["max_iterations"]  # get maximum iterations
        work_precision = params["work_precision"]  # get work precision
        eval_function.set_starting_point(starting_point)  # set initial starting point

        function_values = []  # List for keeping track of values
        gradient_values = []  # List for keeping track of gradients
        prev_val = None

        start_time = time.process_time()
        # START THE PROCESS OF FINDING THE MINIMUM
        for iter in range(max_iter):
            val, grad, _ = eval_function.calculate(
                value=True, gradient=True, hessian=False
            )

            function_values.append(val)
            gradient_values.append(np.linalg.norm(grad))

            # IF gradient smaller than epsilon end convergance
            if np.linalg.norm(grad) < epsilon:
                break

            if prev_val is not None and abs(prev_val - val) < work_precision:
                print(
                    f"Stopped because of a small change in funcion values ({abs(prev_val - val)} < {work_precision})"
                )
                break
            prev_val = val

            # Use the line search method to calculate the step size.
            step_size = self.calculate_step_size(
                input_function=eval_function,
                direction=-grad,
                params=params,
            )
            # Update starting point/input array
            eval_function.set_starting_point(
                eval_function.starting_point + step_size * (-grad)
            )

        # END OF PROCESS
        cpu_time = time.process_time() - start_time
        fmin, _, _ = eval_function.calculate(value=True, gradient=True, hessian=False)
        result_metrics = {
            "current_point": eval_function.get_starting_point(),
            "fmin": fmin,
            "iteration": iter,
        }

        # Return results, including evaluations
        # return (
        #     x,
        #     fmin,
        #     it,
        #     function_values,
        #     gradient_values,
        #     grad_norm,
        #     evaluation_numbers,
        #     cpu_time,
        # )


# test functions class
class TestFunction:
    def calculate(
        self, value: bool = False, gradient: bool = False, hessian: bool = False
    ):
        raise NotImplementedError("This method should be overridden")

    def starting_points(self, starting_value: int | float | list):
        raise NotImplementedError("This method should be overridden")
