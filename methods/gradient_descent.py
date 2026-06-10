"""
Module for the gradient descent
"""

# gradient_line_search.py
import time
import numpy as np
from core.core import LineSearchMethod
from operator import add


class GradientLineSearch(LineSearchMethod):
    def __init__(self, use_linear_search: bool = True):
        super().__init__(use_linear_search)
        self.evaluation_numbers = [0, 0, 0]  # val, gradient, hessian
        self.line_step_function = None

    def set_line_step_function(self, ls_function):
        # Sets linear step function
        self.linear_step_function = ls_function

    def calculate_step_size(self, input_function, direction, params):
        # NOTE. Dumb, I know
        return self.linear_step_function(input_function, direction, params)

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
            print(eval_function.starting_point)
            print(eval_function.starting_point.shape)
            val, grad, _ = eval_function.calculate(
                value=True, gradient=True, hessian=False
            )
            self.evaluation_numbers = list(map(add, self.evaluation_numbers, [1, 1, 0]))

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
            step_size, eval_numbers = self.calculate_step_size(
                input_function=eval_function,
                direction=-grad,
                params=params,
            )
            self.evaluation_numbers = list(
                map(add, self.evaluation_numbers, eval_numbers)
            )

            # Update starting point/input array
            eval_function.set_starting_point(
                eval_function.starting_point + step_size * (-grad)
            )

        # END OF PROCESS
        cpu_time = time.process_time() - start_time
        fmin, _, _ = eval_function.calculate(value=True, gradient=True, hessian=False)
        self.evaluation_numbers[0] += 1  # Increase value evaluation num

        return {
            "current_point": eval_function.get_starting_point(),
            "fmin": fmin,
            "iteration": iter,
            "function_values": function_values,
            "gradient_values": gradient_values,
            "grad_norm": gradient_values[iter],
            "eval_numbers": self.evaluation_numbers,
            "exec_time": cpu_time,
        }
