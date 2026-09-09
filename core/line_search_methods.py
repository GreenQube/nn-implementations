"""
Module for line search methods.
"""

import numpy as np
from operator import add
from core.core import TestFunction, LineStepFunction


class Armijo(LineStepFunction):
    def __init__(self, beta=0.5, sigma=1.0, **kwargs):
        parameters = {"sigma": sigma, "beta": beta, **kwargs}
        super().__init__(parameters)

    def calculate_function(self, input_function: TestFunction, direction: np.ndarray):
        """
        Armijo Line Search Method used to calculated a step parameter

        args:
            input_function (TestFunction): Function for which we are using line search.
            direction (np.ndarray): Direction vector used for calculating the step.
            params (dict[str, any]): Various parameters used for caclulating step

        returns:
            Necessary step, fullfiling the line search criterium.
        """
        evaluation_numbers = [0, 0, 0]
        beta = self.parameters["beta"]
        sigma = self.parameters["sigma"]
        step = 1.0

        starting_point = input_function.get_starting_point()
        val, grad, _ = input_function.calculate(
            value=True, gradient=True, hessian=False
        )
        evaluation_numbers = list(map(add, evaluation_numbers, [1, 1, 0]))

        while True:
            input_function.set_starting_point(
                starting_point + step * direction  # update starting point
            )
            value_after_step, _, _ = input_function.calculate(True, False, False)

            if value_after_step <= (  # f(x + step*g) <= f(x) - step*sigma*<grad, p>
                val + sigma * step * np.dot(grad, direction)
            ):  # spin while, so one can determine the necessary step
                break

            evaluation_numbers[0] += 1  # Increase value evaluation num
            step *= beta

        return step, evaluation_numbers


class Goldstein(LineStepFunction):
    def __init__(self, alpha=1.0, beta=0.5, **kwargs):
        parameters = {"alpha": alpha, "beta": beta, **kwargs}
        super().__init__(parameters)

    def calculate_function(self, input_function: TestFunction, direction: np.ndarray):
        """
        Goldstein Line Search Method used to calculate a step parameter.

        args:
            input_function (TestFunction): Function for which we are using line search.
            direction (np.ndarray): Direction vector used for calculating the step.
            params (dict[str, any]): Various parameters used for calculating step.

        returns:
            Necessary step, fulfilling the line search criterium.
        """

        evaluation_numbers = [0, 0, 0]

        alpha = self.parameters["alpha"]
        beta = self.parameters["beta"]
        step = 1.0

        starting_point = input_function.get_starting_point()
        val, grad, _ = input_function.calculate(
            value=True, gradient=True, hessian=False
        )
        evaluation_numbers = list(map(add, evaluation_numbers, [1, 1, 0]))

        input_function.set_starting_point(starting_point + step * direction)
        next_val, _, _ = input_function.calculate(
            value=True, gradient=False, hessian=False
        )
        evaluation_numbers[0] += 1

        # NOTE, how is this different than Armijo?
        while next_val > val + alpha * step * np.dot(grad, direction):
            step *= beta
            input_function.set_starting_point(starting_point + step * direction)
            next_val, _, _ = input_function.calculate(
                value=True, gradient=False, hessian=False
            )
            evaluation_numbers[0] += 1

        return step, evaluation_numbers


class Wolfe(LineStepFunction):
    def __init__(self, c1=1.0, c2=0.5, **kwargs):
        parameters = {"c1": c1, "c2": c2, **kwargs}
        super().__init__(parameters)

    def calculate_function(self, input_function: TestFunction, direction: np.ndarray):
        """
        Wolfe Line Search Method used to calculate a step parameter.

        args:
            input_function (TestFunction): Function for which we are using line search.
            direction (np.ndarray): Direction vector used for calculating the step.
            params (dict[str, any]): Various parameters used for calculating step,
                expected keys:
                    - "sigma" (float): c1 constant for the sufficient decrease (Armijo) condition.
                    - "rho" (float): c2 constant for the curvature condition.

        returns:
            Necessary step, fulfilling the line search criterium.
        """
        evaluation_numbers = [0, 0, 0]
        c1 = self.parameters["c1"]
        c2 = self.parameters["c2"]
        step = 1.0

        starting_point = input_function.get_starting_point()
        val, grad, _ = input_function.calculate(
            value=True, gradient=True, hessian=False
        )
        evaluation_numbers = list(map(add, evaluation_numbers, [1, 1, 0]))

        input_function.set_starting_point(starting_point + step * direction)
        next_val, grad_next, _ = input_function.calculate(
            value=True, gradient=True, hessian=False
        )
        evaluation_numbers = list(map(add, evaluation_numbers, [1, 1, 0]))
        grad_next = np.dot(grad_next, direction)

        while next_val > val + c1 * step * np.dot(grad, direction):
            step *= 0.5
            input_function.set_starting_point(starting_point + step * direction)
            next_val, grad_next, _ = input_function.calculate(
                value=True, gradient=True, hessian=False
            )
            grad_next = np.dot(grad_next, direction)
            evaluation_numbers = list(map(add, evaluation_numbers, [1, 1, 0]))

        while grad_next < c2 * np.dot(grad, direction):
            step *= 2
            input_function.set_starting_point(starting_point + step * direction)
            next_val, grad_next, _ = input_function.calculate(
                value=True, gradient=True, hessian=False
            )
            grad_next = np.dot(grad_next, direction)
            evaluation_numbers = list(map(add, evaluation_numbers, [1, 1, 0]))

        return step, evaluation_numbers
