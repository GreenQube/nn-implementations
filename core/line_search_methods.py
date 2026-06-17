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
        value_after_step, _, _ = input_function.calculate(True, False, False)

        if value_after_step <= (  # f(x + step*g) <= f(x) - step*sigma*<grad, p>
            val + sigma * step * np.dot(grad, direction)
        ):  # spin while, so one can determine the necessary step
            break

        evaluation_numbers[0] += 1  # Increase value evaluation num
        step *= beta

    return step, evaluation_numbers


# def goldstein(self, func, x, direction, params):
def goldstein(input_function, direction, params):
    evaluation_numbers = [0, 0, 0]
    alpha = params["sigma"]
    beta = params["beta"]
    step = 1.0

    starting_point = input_function.get_starting_point()
    val, grad, _ = input_function.calculate(value=True, gradient=True, hessian=False)
    evaluation_numbers = list(map(add, evaluation_numbers, [1, 1, 0]))

    input_function.set_starting_point(starting_point + step * direction)
    next_val, _, _ = input_function.calculate(value=True, gradient=False, hessian=False)
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


def wolfe(input_function, direction, params):
    evaluation_numbers = [0, 0, 0]
    c1 = params["sigma"]  # You can use sigma as c1
    c2 = params["rho"]  # Assuming rho is for c2
    step = 1.0

    starting_point = input_function.get_starting_point()
    val, grad, _ = input_function.calculate(value=True, gradient=True, hessian=False)
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
