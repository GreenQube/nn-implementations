"""
Module for the conjugate gradient
"""

# conjugate_gradient.py
import time
import numpy as np
from core.core import LineSearchMethod
from operator import add
from utils.utils import relative_error


class ConjugatedGradient(LineSearchMethod):
    def __init__(self):
        super().__init__()
        self.evaluation_numbers = [0, 0, 0]  # val, gradient, hessian

    def find_minimum(self, eval_function, starting_point, params):
        epsilon = params["epsilon"]  # get the epsilon
        max_iter = params["max_iterations"]  # get maximum iterations
        work_precision = params["work_precision"]  # get work precision
        eval_function.set_starting_point(starting_point)  # set initial starting point

        function_values = []  # List for keeping track of values
        gradient_values = []  # List for keeping track of gradients
        prev_val = None

        direction = None  # conjugate direction, built up across iterations
        prev_grad = None  # gradient from the previous iteration
        beta_restart_lower_bound = (
            0.01  # lower bound used in the beta restart safeguard
        )

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

            if prev_val is not None and relative_error(val, prev_val) < work_precision:
                print(
                    f"Stopped because of a small change in funcion values ({relative_error(val, prev_val)} < {work_precision})"
                )
                break

            # Set prev_val as current
            prev_val = val

            # Build the conjugate direction, Hager-Zhang
            if direction is None:
                direction = -grad
            else:
                # Restart threshold: beta is never allowed to fall below this,
                # which guards against numerically unstable / non-descent steps.
                beta_restart_threshold = -1.0 / (
                    np.linalg.norm(direction)
                    * min(beta_restart_lower_bound, np.linalg.norm(grad))
                )

                grad_diff = grad - prev_grad
                direction_grad_diff = direction @ grad_diff

                beta_hager_zhang = (
                    (1.0 / direction_grad_diff)
                    * (
                        grad_diff
                        - 2
                        * direction
                        * (np.linalg.norm(grad_diff) ** 2 / direction_grad_diff)
                    )
                    @ grad
                )

                # Restart if smaller than threshold
                beta_hager_zhang = max(beta_hager_zhang, beta_restart_threshold)
                # Update direction
                direction = beta_hager_zhang * direction - grad

            # Set previous grad
            prev_grad = grad

            # Use the line search method to calculate the step size.
            current_point = eval_function.get_starting_point()
            step_size, eval_numbers = self.calculate_step_size(
                input_function=eval_function,
                direction=direction,
            )
            self.evaluation_numbers = list(
                map(add, self.evaluation_numbers, eval_numbers)
            )

            # Update starting point/input array
            eval_function.set_starting_point(current_point + step_size * direction)

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


class DaiYuan(LineSearchMethod):
    def __init__(self):
        super().__init__()
        self.evaluation_numbers = [0, 0, 0]  # val, gradient, hessian

    def find_minimum(self, eval_function, starting_point, params):
        epsilon = params["epsilon"]  # get the epsilon
        max_iter = params["max_iterations"]  # get maximum iterations
        work_precision = params["work_precision"]  # get work precision

        eval_function.set_starting_point(starting_point)  # set initial starting point
        val, grad, _ = eval_function.calculate(value=True, gradient=True, hessian=False)

        function_values = []  # List for keeping track of values
        gradient_values = []  # List for keeping track of gradients
        direction = -grad
        prev_val = None

        start_time = time.process_time()
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

            if prev_val is not None and relative_error(val, prev_val) < work_precision:
                print(
                    f"Stopped because of a small change in funcion values ({relative_error(val, prev_val)} < {work_precision})"
                )
                break

            prev_val = val

            # Line search satisfying line search conditions
            current_point = eval_function.get_starting_point()
            step_size, eval_numbers = self.calculate_step_size(
                input_function=eval_function,
                direction=direction,
            )

            # Update starting point/input array
            eval_function.set_starting_point(current_point + step_size * direction)
            # Get the grad for the next starting point
            _, next_grad, _ = eval_function.calculate(
                value=False, gradient=True, hessian=False
            )

            # Dai-Yuan beta
            beta = (next_grad @ next_grad) / (direction @ (next_grad - grad))
            direction = -next_grad + beta * (direction)

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
