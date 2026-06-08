"""
Module for the gradient descent
"""

# gradient_line_search.py
import time
import numpy as np
from copy import copy
from core.core import LineSearchMethod
from operator import add


class ArmijoSearch(LineSearchMethod):
    def __init__(self, step: float = 1.0):
        super().__init__()
        self.step = step

    def calculate_step_size(self, input_function, direction, params):
        beta = params["beta"]
        sigma = params["sigma"]
        step = copy(self.step)

        starting_point = input_function.get_starting_point()
        val, grad, _ = input_function.calculate(
            value=True, gradient=True, hessian=False
        )
        self.evaluation_numbers = list(map(add, self.evaluation_numbers, [1, 1, 0]))

        while True:
            input_function.set_starting_point(
                starting_point + step * direction  # update starting point
            )
            value_after_step = input_function.calculate(True, False, False)[0]

            if value_after_step <= (  # f(x + step*g) <= f(x) - step*sigma*<grad, p>
                val + sigma * step * np.dot(grad, direction)
            ):  # spin while, so one can determine the necessary step
                break

            self.evaluation_numbers[0] += 1  # Increase value evaluation num
            step *= beta

        return step
