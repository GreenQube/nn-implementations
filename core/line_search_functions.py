"""
Module for line search methods.
"""

from operator import add
import math
import numpy as np
from core.core import TestFunction, LineSearchFunction


class Backtrack(LineSearchFunction):
    """
    Armijo Backtrack Line Search Method used to calculate a step parameter.

    args:
        beta: Backtracking factor used to shrink the step size
            when the decrease condition is not satisfied.
        sigma: Sufficient decrease parameter controlling how strict
            the decrease condition is.
        **kwargs: Additional parameters passed to the base LineSearchFunction.
    """

    def __init__(self, beta=0.3, sigma=1e-4, **kwargs):
        parameters = {"sigma": sigma, "beta": beta, **kwargs}
        super().__init__(parameters)
        self.prev_val = None

    def calculate_function(
        self,
        input_function: TestFunction,
        direction: np.ndarray,
    ):
        """
        Armijo Line Search Method used to calculated a step parameter

        args:
            input_function (TestFunction): Function for which we are using line search.
            direction (np.ndarray): Direction vector used for calculating the step.

        returns:
            Necessary step, fullfiling the line search criterium.
        """
        evaluation_numbers = [0, 0, 0]
        beta = self.parameters["beta"]
        sigma = self.parameters["sigma"]

        starting_point = input_function.get_starting_point()
        val, grad, _ = input_function.calculate(
            value=True, gradient=True, hessian=False
        )
        evaluation_numbers = list(map(add, evaluation_numbers, [1, 1, 0]))

        # NOTE. This should be taking in the second last value!
        if self.prev_val is None:
            step = self.default_step
            self.prev_val = val
        else:
            prev_val = self.prev_val  # value from previous outer iteration
            step = self._compute_line_search_start_point(val, prev_val, grad, direction)
            self.prev_val = val

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

    def _compute_line_search_start_point(self, val, val_prev, grad, direction):
        """
        Nocedal-style initial step-size guess.
        Uses the Nocedal & Wright, Numerical Optimization.
        Estimates the step size that would give the same decrease
        as the previous outer iteration, based on a linear model of f.
        Falls back to 1.0 if the estimate is non-positive or undefined/
        """
        denominator = np.dot(grad, direction)

        if denominator == 0:
            return 1.0

        new_sp = 2.0 * (val - val_prev) / denominator

        # Guard against a non-sensible (non-positive) initial guess
        if new_sp <= 0:
            new_sp = 1.0

        return new_sp


class Armijo(LineSearchFunction):
    """
    Armijo Line Search Method used to calculate a step parameter.

    Uses quadratic interpolation to pick the first trial step and cubic
    interpolation for subsequent trials, instead of a blind backtracking
    shrink, this converges faster and more reliably than plain
    backtracking while still satisfying the same sufficient decrease rule.

    args:
        sigma: Sufficient decrease parameter controlling how strict
            the decrease condition is.
        beta: Fallback shrink factor, used only if interpolation produces
            a degenerate or invalid step.
        **kwargs: Additional parameters passed to the base LineSearchFunction.
    """

    def __init__(self, sigma=1e-4, beta=0.3, **kwargs):
        parameters = {"sigma": sigma, "beta": beta, **kwargs}
        super().__init__(parameters)

    def calculate_function(self, input_function: TestFunction, direction: np.ndarray):
        """
        Armijo Line Search Method used to calculated a step parameter

        args:
            input_function (TestFunction): Function for which we are using line search.
            direction (np.ndarray): Direction vector used for calculating the step.

        returns:
            Necessary step, fullfiling the line search criterium.
        """
        evaluation_numbers = [0, 0, 0]
        sigma = self.parameters["sigma"]
        beta = self.parameters["beta"]
        step = self.default_step  # is 1.0?

        # For starting point calculation
        starting_point = input_function.get_starting_point()
        # Starting Point Value
        sp_val, grad, _ = input_function.calculate(
            value=True, gradient=True, hessian=False
        )
        evaluation_numbers = list(map(add, evaluation_numbers, [1, 1, 0]))

        # Take a step and calculate
        input_function.set_starting_point(
            starting_point + step * direction  # update starting point
        )
        val, _, _ = input_function.calculate(True, False, False)
        evaluation_numbers[0] += 1  # Increase value evaluation num

        # Set prev step to step, and prev val to current val
        prev_step = step
        prev_val = val  # NOTE. shouldn't this be  = sp_val?
        count = 1

        while val > (  # f(x + step*g) <= f(x) + step*sigma*<grad, p>
            sp_val + sigma * step * np.dot(grad, direction)
        ):  # spin while, so one can determine the necessary step

            if count == 1:  # if just entered while
                step = self._interpolate_quadratic(
                    step, sp_val, val, np.dot(grad, direction)
                )
            else:
                new_step = self._interpolate_cubic(
                    prev_step,  # previous step
                    step,  # current step
                    sp_val,  # sp_value
                    prev_val,  # previous value
                    val,  # current value
                    np.dot(grad, direction),
                )
                prev_step = step
                prev_val = val
                step = new_step

            # update starting point
            input_function.set_starting_point(starting_point + step * direction)
            val, _, _ = input_function.calculate(True, False, False)
            evaluation_numbers[0] += 1  # Increase value evaluation num

            # Increase the count
            count += 1

        return step, evaluation_numbers

    def _interpolate_quadratic(self, step, sp_val, val, grad_dot_dir):
        """
        Fits a quadratic to phi(0), phi'(0), phi(step) and returns the
        step minimizing it -- a much better first guess than blindly
        shrinking by beta.
        """
        denominator = 2 * (val - sp_val - grad_dot_dir * step)
        if denominator == 0:
            return step * self.parameters["beta"]  # fallback if degenerate
        return -grad_dot_dir * step**2 / denominator

    def _interpolate_cubic(
        self,
        prev_step,
        step,
        sp_val,  # sp_val
        prev_val,
        val,  # val
        grad_dot_dir,
    ):
        """
        Fits a cubic to phi(0), phi'(0), phi(prev_step), phi(step) and
        returns the step minimizing it, used once we have two prior
        trial points.
        """
        denom = (prev_step**2) * (step**2) * (step - prev_step)
        if denom == 0:
            return step * self.parameters["beta"]  # fallback if degenerate

        a = (
            prev_step**2 * (val - sp_val - grad_dot_dir * step)
            - step**2 * (prev_val - sp_val - grad_dot_dir * prev_step)
        ) / denom
        b = (
            -(prev_step**3) * (val - sp_val - grad_dot_dir * step)
            + step**3 * (prev_val - sp_val - grad_dot_dir * prev_step)
        ) / denom

        radicand = b**2 - 3 * a * grad_dot_dir
        if a == 0 or radicand < 0:
            # Default to StepBack if a == 0 /
            return step * self.parameters["beta"]

        return (-b + math.sqrt(radicand)) / (3 * a)


class Goldstein(LineSearchFunction):
    """
    Goldstein Line Search Method used to calculate a step parameter.

    args:
        alpha: Sufficient decrease parameter controlling both the upper
            (Armijo) and lower (Goldstein) bounds on acceptable decrease.
            Must satisfy 0 < alpha < 0.5 for the two bounds to be
            compatible with each other.
        gamma: Expansion factor used to grow the step when the lower
            bound is violated and no finite upper bracket has been
            found yet.
        **kwargs: Additional parameters passed to the base LineSearchFunction.
    """

    def __init__(self, alpha=1e-4, gamma=1.1, **kwargs):
        parameters = {"alpha": alpha, "gamma": gamma, **kwargs}
        super().__init__(parameters)

    def calculate_function(self, input_function: TestFunction, direction: np.ndarray):
        """
        Goldstein Line Search Method used to calculate a step parameter.

        args:
            input_function (TestFunction): Function for which we are using line search.
            direction (np.ndarray): Direction vector used for calculating the step.

        returns:
            Necessary step, fulfilling the line search criterium.
        """

        evaluation_numbers = [0, 0, 0]

        alpha = self.parameters["alpha"]
        gamma = self.parameters["gamma"]
        step = self.default_step

        starting_point = input_function.get_starting_point()
        val, grad, _ = input_function.calculate(
            value=True, gradient=True, hessian=False
        )
        evaluation_numbers = list(map(add, evaluation_numbers, [1, 1, 0]))
        grad_dot_dir = np.dot(grad, direction)

        input_function.set_starting_point(starting_point + step * direction)
        next_val, _, _ = input_function.calculate(
            value=True, gradient=False, hessian=False
        )
        evaluation_numbers[0] += 1

        lower_step = 0.0
        upper_step = math.inf

        while (
            next_val > val + alpha * step * grad_dot_dir  # upper bound violated
            or next_val
            < val + (1 - alpha) * step * grad_dot_dir  # lower bound violated
        ):
            # Update to in between step between 0 and inf
            if next_val > val + alpha * step * grad_dot_dir:
                # For when step too big
                upper_step = step
                step = (lower_step + upper_step) / 2
            else:
                # For when step too small
                lower_step = step
                if upper_step < math.inf:
                    step = (lower_step + upper_step) / 2
                else:
                    step *= gamma

            input_function.set_starting_point(starting_point + step * direction)
            next_val, _, _ = input_function.calculate(
                value=True, gradient=False, hessian=False
            )
            evaluation_numbers[0] += 1

        return step, evaluation_numbers


class Wolfe(LineSearchFunction):
    """
    Wolfe Line Search Method used to calculate a step parameter.

    args:
        c1: Sufficient decrease parameter controlling the strictness
            of the Armijo (decrease) condition.
        c2: Curvature condition parameter controlling the strictness
            of the curvature condition.
        **kwargs: Additional parameters passed to the base LineSearchFunction.
    """

    def __init__(self, c1=1e-4, c2=0.9, **kwargs):
        parameters = {"c1": c1, "c2": c2, **kwargs}
        super().__init__(parameters)

    def calculate_function(self, input_function: TestFunction, direction: np.ndarray):
        """
        Wolfe Line Search Method used to calculate a step parameter.

        args:
            input_function (TestFunction): Function for which we are using line search.
            direction (np.ndarray): Direction vector used for calculating the step.

        returns:
            Necessary step, fulfilling the line search criterium.
        """
        evaluation_numbers = [0, 0, 0]
        c1 = self.parameters["c1"]
        c2 = self.parameters["c2"]
        step = self.default_step  # is 1.0

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
