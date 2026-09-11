"""
Module for the gradient descent
"""

# gradient_descent.py
import time
import numpy as np
from core.core import LineSearchMethod
from operator import add
from utils.utils import relative_error


class GradientLineSearch(LineSearchMethod):
    """
    Gradient Descent optimization method that uses a line search technique
    to determine the step size at each iteration.

    args:
        use_linear_search: Whether using a line search
            strategy for determining the step size at each iteration.
    """

    def __init__(self, use_line_search: bool = True):
        super().__init__(use_line_search)
        self.evaluation_numbers = [0, 0, 0]  # val, gradient, hessian
        self.line_step_function = None

    def find_minimum(self, eval_function, starting_point, params):
        """
        Runs the Gradient Descent algorithm to find the minimum of the given
        function, using a line search method to determine the step size at
        each iteration.

        args:
            eval_function (TestFunction): Function whose minimum we are searching for.
            starting_point (np.ndarray): Initial point from which the search starts.
            params (dict): Dictionary of algorithm parameters. Expected keys:
                - epsilon (float): Gradient norm threshold used as a stopping criterion.
                - max_iterations (int): Maximum number of iterations to perform.
                - work_precision (float): Minimum change in function value between
                  iterations required to continue the search.

        returns:
            dict: Dictionary containing the results of the optimization.
        """
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
            self.evaluation_numbers = list(map(add, self.evaluation_numbers, [1, 1, 0]))

            function_values.append(val)
            gradient_values.append(np.linalg.norm(grad))

            # IF gradient smaller than epsilon end convergance
            if np.linalg.norm(grad) < epsilon:
                break

            if prev_val is not None and relative_error(prev_val, val) < work_precision:
                print(
                    f"Stopped because of a small change in funcion values ({relative_error(prev_val, val)} < {work_precision})"
                )
                break
            prev_val = val

            # Use the line search method to calculate the step size.
            current_point = eval_function.get_starting_point()
            step_size, eval_numbers = self.calculate_step_size(
                input_function=eval_function,
                direction=-grad,
            )
            self.evaluation_numbers = list(
                map(add, self.evaluation_numbers, eval_numbers)
            )

            # Update starting point/input array
            eval_function.set_starting_point(current_point + step_size * (-grad))

        # END OF PROCESS
        cpu_time = time.process_time() - start_time

        return {
            "current_point": eval_function.get_starting_point(),
            "fmin": val,
            "iteration": iter,
            "function_values": function_values,
            "gradient_values": gradient_values,
            "grad_norm": gradient_values[iter],
            "eval_numbers": self.evaluation_numbers,
            "exec_time": cpu_time,
        }
