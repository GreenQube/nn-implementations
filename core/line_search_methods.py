"""
Module for line search methods
"""

# gradient_line_search.py
import numpy as np
from operator import add


def armijo(input_function, direction, params):
    evaluation_numbers = [0, 0, 0]
    beta = params["beta"]
    sigma = params["sigma"]
    step = 1.0

    starting_point = input_function.get_starting_point()
    val, grad, _ = input_function.calculate(value=True, gradient=True, hessian=False)
    evaluation_numbers = list(map(add, evaluation_numbers, [1, 1, 0]))

    while True:
        input_function.set_starting_point(
            starting_point + step * direction  # update starting point
        )
        value_after_step = input_function.calculate(True, False, False)[0]

        if value_after_step <= (  # f(x + step*g) <= f(x) - step*sigma*<grad, p>
            val + sigma * step * np.dot(grad, direction)
        ):  # spin while, so one can determine the necessary step
            break

        evaluation_numbers[0] += 1  # Increase value evaluation num
        step *= beta

    return step, evaluation_numbers
