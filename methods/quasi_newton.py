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
        self.evaluation_numbers = [0, 0, 0]

    def find_minimum(self, eval_function, starting_point, params):
        epsilon = params["epsilon"]
        max_iter = params["max_iterations"]
        work_precision = params["work_precision"]

        self.evaluation_numbers = [0, 0, 0]

        eval_function.set_starting_point(starting_point)

        eye_matrix = np.eye(starting_point.shape[0])
        inverse_hess_apr = eye_matrix.copy()

        function_values = []
        gradient_values = []

        start_time = time.process_time()

        val, grad, _ = eval_function.calculate(value=True, gradient=True, hessian=False)
        self.evaluation_numbers = list(map(add, self.evaluation_numbers, [1, 1, 0]))

        function_values.append(val)
        gradient_values.append(np.linalg.norm(grad))

        iteration = 0

        while iteration < max_iter:

            grad_norm = np.linalg.norm(grad)

            if grad_norm < epsilon:
                break

            direction = -np.matmul(inverse_hess_apr, grad)

            step_size, eval_numbers = self.calculate_step_size(
                input_function=eval_function,
                direction=direction,
                params=params,
            )

            self.evaluation_numbers = list(
                map(add, self.evaluation_numbers, eval_numbers)
            )

            starting_point = eval_function.get_starting_point()

            next_step = step_size * direction
            next_point = starting_point + next_step

            eval_function.set_starting_point(next_point)

            f_prev = val

            f_curr, grad_next, _ = eval_function.calculate(
                value=True, gradient=True, hessian=False
            )

            self.evaluation_numbers = list(map(add, self.evaluation_numbers, [1, 1, 0]))

            iteration += 1

            function_values.append(f_curr)
            gradient_values.append(np.linalg.norm(grad_next))

            gradient_delta = grad_next - grad
            sTy = np.dot(gradient_delta, next_step)

            if sTy > 1e-12:
                rho = 1.0 / sTy

                term1 = eye_matrix - rho * np.outer(next_step, gradient_delta)

                term2 = eye_matrix - rho * np.outer(gradient_delta, next_step)

                term3 = rho * np.outer(next_step, next_step)

                inverse_hess_apr = (
                    np.dot(term1, np.dot(inverse_hess_apr, term2)) + term3
                )

            relative_function_change = abs(f_curr - f_prev) / (1 + abs(f_curr))

            val = f_curr
            grad = grad_next

            if np.linalg.norm(grad) < epsilon:
                break

            if relative_function_change < work_precision:
                break

        cpu_time = time.process_time() - start_time

        return {
            "current_point": eval_function.get_starting_point(),
            "fmin": val,
            "iteration": iteration,
            "function_values": function_values,
            "gradient_values": gradient_values,
            "grad_norm": gradient_values[-1],
            "eval_numbers": self.evaluation_numbers,
            "exec_time": cpu_time,
        }


class L_BFGS(LineSearchMethod):
    def __init__(self):
        super().__init__()
        self.evaluation_numbers = [0, 0, 0]
        self.memory = 10

    def find_minimum(self, eval_function, starting_point, params):
        epsilon = params["epsilon"]
        max_iter = params["max_iterations"]
        work_precision = params["work_precision"]

        self.evaluation_numbers = [0, 0, 0]

        eval_function.set_starting_point(starting_point)

        function_values = []
        gradient_values = []

        s_history = []
        y_history = []
        rho_history = []

        start_time = time.process_time()

        val, grad, _ = eval_function.calculate(value=True, gradient=True, hessian=False)

        self.evaluation_numbers = list(map(add, self.evaluation_numbers, [1, 1, 0]))

        function_values.append(val)
        gradient_values.append(np.linalg.norm(grad))

        iteration = 0

        while iteration < max_iter:

            grad_norm = np.linalg.norm(grad)

            if grad_norm < epsilon:
                break

            q = grad.copy()

            alpha_values = []

            i = len(s_history) - 1

            while i >= 0:
                s = s_history[i]
                y = y_history[i]
                rho = rho_history[i]

                alpha = rho * np.dot(s, q)
                alpha_values.append(alpha)

                q = q - alpha * y

                i -= 1

            if len(s_history) > 0:
                last_s = s_history[-1]
                last_y = y_history[-1]

                yTy = np.dot(last_y, last_y)

                if yTy > 1e-12:
                    gamma = np.dot(last_s, last_y) / yTy
                else:
                    gamma = 1.0
            else:
                gamma = 1.0

            r = gamma * q

            i = 0

            while i < len(s_history):
                s = s_history[i]
                y = y_history[i]
                rho = rho_history[i]

                alpha = alpha_values[len(alpha_values) - 1 - i]

                beta = rho * np.dot(y, r)

                r = r + s * (alpha - beta)

                i += 1

            direction = -r

            step_size, eval_numbers = self.calculate_step_size(
                input_function=eval_function,
                direction=direction,
                params=params,
            )

            self.evaluation_numbers = list(
                map(add, self.evaluation_numbers, eval_numbers)
            )

            starting_point = eval_function.get_starting_point()

            next_step = step_size * direction
            next_point = starting_point + next_step

            eval_function.set_starting_point(next_point)

            f_prev = val

            f_curr, grad_next, _ = eval_function.calculate(
                value=True, gradient=True, hessian=False
            )

            self.evaluation_numbers = list(map(add, self.evaluation_numbers, [1, 1, 0]))

            iteration += 1

            function_values.append(f_curr)
            gradient_values.append(np.linalg.norm(grad_next))

            gradient_delta = grad_next - grad

            sTy = np.dot(next_step, gradient_delta)

            if sTy > 1e-12:
                rho = 1.0 / sTy

                s_history.append(next_step.copy())
                y_history.append(gradient_delta.copy())
                rho_history.append(rho)

                if len(s_history) > self.memory:
                    s_history.pop(0)
                    y_history.pop(0)
                    rho_history.pop(0)

            relative_function_change = abs(f_curr - f_prev) / (1 + abs(f_curr))

            val = f_curr
            grad = grad_next

            if np.linalg.norm(grad) < epsilon:
                break

            if relative_function_change < work_precision:
                break

        cpu_time = time.process_time() - start_time

        return {
            "current_point": eval_function.get_starting_point(),
            "fmin": val,
            "iteration": iteration,
            "function_values": function_values,
            "gradient_values": gradient_values,
            "grad_norm": gradient_values[-1],
            "eval_numbers": self.evaluation_numbers,
            "exec_time": cpu_time,
        }


class Broyden(LineSearchMethod):
    def __init__(self):
        super().__init__()
        self.evaluation_numbers = [0, 0, 0]

    def find_minimum(self, eval_function, starting_point, params):
        epsilon = params["epsilon"]
        max_iter = params["max_iterations"]
        work_precision = params["work_precision"]

        self.evaluation_numbers = [0, 0, 0]

        eval_function.set_starting_point(starting_point)

        eye_matrix = np.eye(starting_point.shape[0])
        inverse_hess_apr = eye_matrix.copy()

        function_values = []
        gradient_values = []

        start_time = time.process_time()

        val, grad, _ = eval_function.calculate(value=True, gradient=True, hessian=False)

        self.evaluation_numbers = list(map(add, self.evaluation_numbers, [1, 1, 0]))

        function_values.append(val)
        gradient_values.append(np.linalg.norm(grad))

        iteration = 0

        while iteration < max_iter:

            grad_norm = np.linalg.norm(grad)

            if grad_norm < epsilon:
                break

            direction = -np.matmul(inverse_hess_apr, grad)

            step_size, eval_numbers = self.calculate_step_size(
                input_function=eval_function,
                direction=direction,
                params=params,
            )

            self.evaluation_numbers = list(
                map(add, self.evaluation_numbers, eval_numbers)
            )

            starting_point = eval_function.get_starting_point()

            next_step = step_size * direction
            next_point = starting_point + next_step

            eval_function.set_starting_point(next_point)

            f_prev = val

            f_curr, grad_next, _ = eval_function.calculate(
                value=True, gradient=True, hessian=False
            )

            self.evaluation_numbers = list(map(add, self.evaluation_numbers, [1, 1, 0]))

            iteration += 1

            function_values.append(f_curr)
            gradient_values.append(np.linalg.norm(grad_next))

            gradient_delta = grad_next - grad

            denom = np.dot(next_step, gradient_delta)

            if abs(denom) > 1e-12:
                inverse_hess_apr = inverse_hess_apr + (
                    np.outer(
                        next_step - np.matmul(inverse_hess_apr, gradient_delta),
                        next_step,
                    )
                    / denom
                )

            relative_function_change = abs(f_curr - f_prev) / (1 + abs(f_curr))

            val = f_curr
            grad = grad_next

            if np.linalg.norm(grad) < epsilon:
                break

            if relative_function_change < work_precision:
                break

        cpu_time = time.process_time() - start_time

        return {
            "current_point": eval_function.get_starting_point(),
            "fmin": val,
            "iteration": iteration,
            "function_values": function_values,
            "gradient_values": gradient_values,
            "grad_norm": gradient_values[-1],
            "eval_numbers": self.evaluation_numbers,
            "exec_time": cpu_time,
        }
