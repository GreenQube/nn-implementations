"""
Module for the quasi-newton method implementations.
"""

# gradient_line_search.py
import time
from core.core import OptimizationMethod, LineSearchMethod
from utils.utils import get_array_inv
import numpy as np
from operator import add


class BFGS(LineSearchMethod):
    def __init__(self):
        super().__init__()
        self.evaluation_numbers = [0, 0, 0]  # val, gradient, hessian

    def find_minimum(self, eval_function, starting_point, params):
        """
        Minimizes a function using the BFGS quasi-Newton method.
        """

        epsilon = params["epsilon"]  # get the epsilon
        max_iter = params["max_iterations"]  # get maximum iterations
        work_precision = params["work_precision"]  # get work precision
        eval_function.set_starting_point(starting_point)  # set initial starting point

        eye_matrix = np.eye(starting_point.shape[0])
        inverse_hess_apr = eye_matrix

        function_values = []  # List for keeping track of values
        gradient_values = []  # List for keeping track of gradients
        start_time = time.process_time()
        for iter in range(max_iter):
            starting_point = eval_function.get_starting_point()
            val, grad, __ = eval_function.calculate(
                value=True, gradient=True, hessian=False
            )
            self.evaluation_numbers = list(map(add, self.evaluation_numbers, [1, 1, 0]))

            function_values.append(val)
            gradient_values.append(np.linalg.norm(grad))

            # Check for convergence, the gradient not changing
            if np.linalg.norm(grad) < epsilon:
                print(f"Converged in {iter} iterations.")
                break

            # Compute search direction: p_k = -B_inv * g_k
            direction = -np.matmul(inverse_hess_apr, grad)

            # Use the line search method to calculate the step size. Wolfe is the usual one
            step_size, eval_numbers = self.calculate_step_size(
                input_function=eval_function,
                direction=-grad,
                params=params,
            )
            self.evaluation_numbers = list(
                map(add, self.evaluation_numbers, eval_numbers)
            )

            # Update step
            next_step = step_size * direction
            next_val = starting_point + next_step

            # Calculate for the next value
            eval_function.set_starting_point(next_val)
            _, grad_next, __ = eval_function.calculate(
                value=False, gradient=True, hessian=False
            )

            if np.sum(np.abs((next_step))) < work_precision:
                print(
                    f"Stopped because of a small change in funcion values ({np.sum(np.abs((next_step)))} < {work_precision})"
                )
                break
            # Compute change in gradient: y_k = g_{k+1} - g_k
            gradient_delta = grad_next - grad

            # BFGS inverse Hessian update formula
            rho = 1.0 / np.dot(gradient_delta, next_step)

            # Use the inverse, Sherman-Morrison formula
            term1 = eye_matrix - rho * np.outer(next_step, gradient_delta)
            term2 = eye_matrix - rho * np.outer(gradient_delta, next_step)
            term3 = rho * np.outer(next_step, next_step)

            inverse_hess_apr = np.dot(term1, np.dot(inverse_hess_apr, term2)) + term3

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


class Broyden(LineSearchMethod):
    def __init__(self):
        super().__init__()
        self.evaluation_numbers = [0, 0, 0]  # val, gradient, hessian

    def find_minimum(self, eval_function, starting_point, params):
        """
        Minimizes a function using the BFGS quasi-Newton method.
        """

        epsilon = params["epsilon"]  # get the epsilon
        max_iter = params["max_iterations"]  # get maximum iterations
        work_precision = params["work_precision"]  # get work precision
        eval_function.set_starting_point(starting_point)  # set initial starting point

        inverse_hess_apr = np.eye(starting_point.shape[0])

        function_values = []  # List for keeping track of values
        gradient_values = []  # List for keeping track of gradients
        start_time = time.process_time()
        for iter in range(max_iter):
            starting_point = eval_function.get_starting_point()
            val, grad, __ = eval_function.calculate(
                value=True, gradient=True, hessian=False
            )
            self.evaluation_numbers = list(map(add, self.evaluation_numbers, [1, 1, 0]))

            function_values.append(val)
            gradient_values.append(np.linalg.norm(grad))

            # Check for convergence, the gradient not changing
            if np.linalg.norm(grad) < epsilon:
                print(f"Converged in {iter} iterations.")
                break

            # Compute search direction: p_k = -B_inv * g_k
            direction = -np.matmul(inverse_hess_apr, grad)

            # Use the line search method to calculate the step size. Wolfe is the usual one
            step_size, eval_numbers = self.calculate_step_size(
                input_function=eval_function,
                direction=-grad,
                params=params,
            )
            self.evaluation_numbers = list(
                map(add, self.evaluation_numbers, eval_numbers)
            )

            # Update step
            next_step = step_size * direction
            next_val = starting_point + next_step

            # Calculate for the next value
            eval_function.set_starting_point(next_val)
            _, grad_next, __ = eval_function.calculate(
                value=False, gradient=True, hessian=False
            )

            if np.sum(np.abs((next_step))) < work_precision:
                print(
                    f"Stopped because of a small change in funcion values ({np.sum(np.abs((next_step)))} < {work_precision})"
                )
                break
            # Compute change in gradient: y_k = g_{k+1} - g_k
            gradient_delta = grad_next - grad

            # BFGS inverse Hessian update formula
            # Use the inverse, Sherman-Morrison formula
            step_mul_term = np.squeeze(
                np.matmul(next_step[np.newaxis, :], inverse_hess_apr)
            )
            denominator = 1.0 / np.dot(step_mul_term, gradient_delta)
            nominator = np.outer(
                (next_step - np.matmul(inverse_hess_apr, grad)), step_mul_term
            )
            inverse_hess_apr = inverse_hess_apr + denominator * nominator

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
