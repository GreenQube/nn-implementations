"""
Module for the modified newton implementations.
"""

# gradient_line_search.py
import time
from core.core import OptimizationMethod
from utils.utils import get_array_inv, relative_error
import numpy as np
from operator import add


class Levenberg_Marquard(OptimizationMethod):
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
        lmbd = 10
        beta = 2
        n_eye = np.eye(len(starting_point))
        eval_function.set_starting_point(starting_point)  # set initial starting point

        function_values = []  # List for keeping track of values
        gradient_values = []  # List for keeping track of gradients
        start_time = time.process_time()
        for iter in range(max_iter):
            current_point = eval_function.get_starting_point()

            val, grad, hess = eval_function.calculate(
                value=True, gradient=True, hessian=True
            )
            self.evaluation_numbers = list(map(add, self.evaluation_numbers, [1, 1, 1]))

            function_values.append(val)
            gradient_values.append(np.linalg.norm(grad))

            # Prevent division by zero if derivative is too close to 0
            if np.linalg.norm(grad) < epsilon:
                print("Derivative is zero. No unique tangent line.")

            old_value = val

            # Levenberg_Marquard update step
            while True:
                try:
                    next_step = np.linalg.solve(
                        (hess + lmbd * np.abs(np.diag(np.diag(hess)))), grad
                    )
                except np.linalg.LinAlgError:
                    lmbd *= beta
                    continue

                next_point = current_point - next_step

                eval_function.set_starting_point(
                    next_point
                )  # set initial starting point
                next_value, _, __ = eval_function.calculate(
                    value=True, gradient=False, hessian=False
                )

                self.evaluation_numbers = list(
                    map(add, self.evaluation_numbers, [1, 0, 0])
                )

                if next_value < val:
                    lmbd /= beta
                    break
                else:
                    lmbd *= beta
                    eval_function.set_starting_point(current_point)

            val = next_value
            if (
                next_value is not None
                and relative_error(next_value, old_value) < work_precision
            ):
                print(
                    f"Stopped because of a small change in funcion values ({relative_error(next_value, old_value)} < {work_precision})"
                )
                break

            eval_function.set_starting_point(next_point)

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


class Levenberg(OptimizationMethod):
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
        lmbd = 10 ** (-4)
        lmbd_min = 10 ** (-10)
        lmbd_max = 10**7

        n_eye = np.eye(len(starting_point))
        eval_function.set_starting_point(starting_point)  # set initial starting point

        function_values = []  # List for keeping track of values
        gradient_values = []  # List for keeping track of gradients
        start_time = time.process_time()

        val, grad, hess = eval_function.calculate(
            value=True, gradient=True, hessian=True
        )
        self.evaluation_numbers = list(map(add, self.evaluation_numbers, [1, 1, 1]))

        for iter in range(max_iter):

            current_point = eval_function.get_starting_point()

            function_values.append(val)
            gradient_values.append(np.linalg.norm(grad))

            # Prevent division by zero if derivative is too close to 0
            if np.linalg.norm(grad) < epsilon:
                print("Derivative is zero. No unique tangent line.")
                break

            old_val = val

            # Levenberg update step
            while True:
                try:
                    next_step = np.linalg.solve(
                        (hess + lmbd * np.eye(len(starting_point))), grad
                    )
                except np.linalg.LinAlgError:
                    lmbd = min(10 * lmbd, lmbd_max)

                    if lmbd == lmbd_max:
                        break

                    continue

                next_point = current_point - next_step

                eval_function.set_starting_point(
                    next_point
                )  # set initial starting point

                next_value, _, __ = eval_function.calculate(
                    value=True, gradient=False, hessian=False
                )

                self.evaluation_numbers = list(
                    map(add, self.evaluation_numbers, [1, 0, 0])
                )

                if next_value >= old_val:
                    eval_function.set_starting_point(current_point)
                    lmbd = min(10 * lmbd, lmbd_max)
                    if lmbd == lmbd_max:
                        break
                else:
                    lmbd = max(lmbd / 10, lmbd_min)
                    break

            if next_value >= old_val:
                break

            val = next_value

            if (
                next_value is not None
                and relative_error(next_value, old_val) < work_precision
            ):
                print(
                    f"Stopped because of a small change in funcion values ({relative_error(next_value, old_val)} < {work_precision})"
                )
                break

            if iter < max_iter - 1:
                _, grad, hess = eval_function.calculate(
                    value=False, gradient=True, hessian=True
                )

                self.evaluation_numbers = list(
                    map(add, self.evaluation_numbers, [0, 1, 1])
                )

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
