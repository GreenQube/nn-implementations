"""
Module for the modified newton implementations.
"""

# gradient_line_search.py
import time
from core.core import OptimizationMethod
from utils.utils import get_array_inv
import numpy as np
from operator import add


class ModifiedNewton(OptimizationMethod):
    def __init__(self):
        super().__init__()
        self.evaluation_numbers = [0, 0, 0]  # val, gradient, hessian

    def find_minimum(self, eval_function, starting_point, params):
        """
        NOTE
        """
        epsilon = params["epsilon"]  # get the epsilon
        max_iter = params["max_iterations"]  # get maximum iterations
        work_precision = params["work_precision"]  # get work precision
        eval_function.set_starting_point(starting_point)  # set initial starting point

        function_values = []  # List for keeping track of values
        gradient_values = []  # List for keeping track of gradients
        start_time = time.process_time()
        for iter in range(max_iter):
            starting_point = eval_function.get_starting_point()
            val, grad, hess = eval_function.calculate(
                value=True, gradient=True, hessian=True
            )
            self.evaluation_numbers = list(map(add, self.evaluation_numbers, [1, 1, 0]))

            function_values.append(val)
            gradient_values.append(np.linalg.norm(grad))

            # Prevent division by zero if derivative is too close to 0
            if np.linalg.norm(grad) < epsilon:
                print("Derivative is zero. No unique tangent line.")
                break
                raise ZeroDivisionError("Derivative is zero. No unique tangent line.")

            # Newton-Raphson update step
            inv_hess = get_array_inv(hess)
            next_step = np.matmul(inv_hess, grad)
            next_val = starting_point - next_step

            # Check if the result has converged within our tolerance limit
            if np.sum(np.abs(next_val - starting_point)) < work_precision:
                break

            eval_function.set_starting_point(next_val)  # set initial starting point

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
