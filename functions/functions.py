# quad_qf1.py
import numpy as np


class Quad_Qf1:
    def __init__(self, input_array: np.ndarray | int | tuple):
        if not isinstance(input_array, np.ndarray):
            input_array = np.ones(input_array)
        self.starting_point = input_array
        self.value = 0.0
        self.gradient = np.zeros(len(self.starting_point))
        self.hessian = 0.0

    def calculate(
        self, value: bool = False, gradient: bool = False, hessian: bool = False
    ):
        """TODO

        Args:
            value (bool, optional): _description_. Defaults to False.
            gradient (bool, optional): _description_. Defaults to False.
            hessian (bool, optional): _description_. Defaults to False.

        Returns:
            _type_: _description_
        """
        n = len(self.starting_point)

        if value:
            self.value = (
                0.5 * sum(np.arange(1, n + 1) * np.square(self.starting_point))
                - self.starting_point[-1]
            )

        if gradient:
            self.gradient = np.arange(1, n + 1) * self.starting_point
            self.gradient[-1] -= 1

        if hessian:
            self.hessian = np.diag(np.arange(1, n + 1))

        return self.value, self.gradient, self.hessian

    def set_starting_point(self, input_array: np.ndarray | int | tuple):
        if not isinstance(input_array, np.ndarray):
            input_array = np.ones(input_array)
        self.starting_point = input_array
        return self.starting_point

    def get_function_values(self):
        return self.value, self.gradient, self.hessian

    def get_starting_point(self):
        return self.starting_point


class Quad_Qf2:
    def __init__(self, input_array: np.ndarray | int | tuple):
        if not isinstance(input_array, np.ndarray):
            input_array = np.ones(input_array)
        self.starting_point = input_array
        self.value = 0.0
        self.gradient = np.zeros(len(self.starting_point))
        self.hessian = 0.0

    def calculate(
        self, value: bool = False, gradient: bool = False, hessian: bool = False
    ):

        n = len(self.starting_point)

        if value:
            self.value = (
                0.5
                * sum(
                    np.arange(1, n + 1) * np.square(np.square(self.starting_point) - 1)
                )
                - self.starting_point[-1]
            )

        if gradient:
            self.gradient = (
                2
                * np.arange(1, n + 1)
                * self.starting_point
                * (np.square(self.starting_point) - 1)
            )
            self.gradient[-1] += -1

        if hessian:
            self.hessian = np.diag(
                2 * np.arange(1, n + 1) * (3 * np.square(self.starting_point) - 1)
            )

        return self.value, self.gradient, self.hessian

    def set_starting_point(self, input_array: np.ndarray | int | tuple):
        if not isinstance(input_array, np.ndarray):
            input_array = np.ones(input_array) * 0.5
        self.starting_point = input_array
        return self.starting_point

    def get_function_values(self):
        return self.value, self.gradient, self.hessian

    def get_starting_point(self):
        return self.starting_point


class Raydan_1:
    def __init__(self, input_array: np.ndarray | int | tuple):
        if not isinstance(input_array, np.ndarray):
            input_array = np.ones(input_array)
        self.starting_point = input_array
        self.value = 0.0
        self.gradient = np.zeros(len(self.starting_point))
        self.hessian = 0.0

    def calculate(
        self, value: bool = False, gradient: bool = False, hessian: bool = False
    ):

        n = len(self.starting_point)

        if value:
            self.value = (
                1
                / 10
                * sum(
                    np.arange(1, n + 1)
                    * (np.exp(self.starting_point) - self.starting_point)
                )
            )

        if gradient:
            self.gradient = (
                1 / 10 * np.arange(1, n + 1) * (np.exp(self.starting_point) - 1)
            )

        if hessian:
            self.hessian = np.diag(
                1 / 10 * np.arange(1, n + 1) * np.exp(self.starting_point)
            )

        return self.value, self.gradient, self.hessian

    def set_starting_point(self, input_array: np.array | int | tuple):
        if not isinstance(input_array, np.ndarray):
            input_array = np.ones(input_array) * 0.5
        self.starting_point = input_array
        return self.starting_point

    def get_function_values(self):
        return self.value, self.gradient, self.hessian

    def get_starting_point(self):
        return self.starting_point


class Raydan_2:
    def __init__(self, input_array: np.ndarray | int | tuple):
        if not isinstance(input_array, np.ndarray):
            input_array = np.ones(input_array)
        self.starting_point = input_array
        self.value = 0.0
        self.gradient = np.zeros(len(self.starting_point))
        self.hessian = 0.0

    def calculate(
        self, value: bool = False, gradient: bool = False, hessian: bool = False
    ):

        n = len(self.starting_point)

        if value:
            self.value = sum(np.exp(self.starting_point) - self.starting_point)

        if gradient:
            self.gradient = np.exp(self.starting_point) - 1

        if hessian:
            self.hessian = np.diag(np.exp(self.starting_point))

        return self.value, self.gradient, self.hessian

    def set_starting_point(self, input_array: np.ndarray | int | tuple):
        if not isinstance(input_array, np.ndarray):
            input_array = np.ones(input_array) * 0.5
        self.starting_point = input_array
        return self.starting_point

    def get_function_values(self):
        return self.value, self.gradient, self.hessian

    def get_starting_point(self):
        return self.starting_point


class Diagonal_1:
    def __init__(self, input_array: np.ndarray | int | tuple):
        if not isinstance(input_array, np.ndarray):
            input_array = np.ones(input_array)
        self.starting_point = input_array
        self.value = 0.0
        self.gradient = np.zeros(len(self.starting_point))
        self.hessian = 0.0

    def calculate(
        self, value: bool = False, gradient: bool = False, hessian: bool = False
    ):

        n = len(self.starting_point)

        if value:
            self.value = sum(
                np.exp(self.starting_point) - np.arange(1, n + 1) * self.starting_point
            )

        if gradient:
            self.gradient = np.exp(self.starting_point) - np.arange(1, n + 1)

        if hessian:
            self.hessian = np.diag(np.exp(self.starting_point))

        return self.value, self.gradient, self.hessian

    def set_starting_point(self, input_array: np.ndarray | int | tuple):
        if not isinstance(input_array, np.ndarray):
            input_array = np.ones(input_array) * (1 / len(self.starting_point))
        self.starting_point = input_array
        # proveri ovo
        return self.starting_point

    def get_function_values(self):
        return self.value, self.gradient, self.hessian

    def get_starting_point(self):
        return self.starting_point


class Diagonal_4:
    def __init__(self, input_array: np.ndarray | int | tuple):
        if not isinstance(input_array, np.ndarray):
            input_array = np.ones(input_array)
        self.starting_point = input_array
        self.value = 0.0
        self.gradient = np.zeros(len(self.starting_point))
        self.hessian = 0.0

    def calculate(
        self, value: bool = False, gradient: bool = False, hessian: bool = False
    ):

        n = len(self.starting_point)

        if value:
            self.value = (
                1
                / 2
                * sum(
                    np.square(self.starting_point[1::2])
                    + 100 * np.square(self.starting_point[::2])
                )
            )
        if gradient:
            self.gradient = self.starting_point.copy()
            self.gradient[::2] *= 100
        if hessian:
            dijagonala = np.ones(n)
            dijagonala[::2] = 100
            self.hessian = np.diag(dijagonala)

        return self.value, self.gradient, self.hessian

    def set_starting_point(self, input_array: np.array | int | tuple):
        if not isinstance(input_array, np.ndarray):
            input_array = np.ones(input_array)
        self.starting_point = input_array
        return self.starting_point

    def get_function_values(self):
        return self.value, self.gradient, self.hessian

    def get_starting_point(self):
        return self.starting_point


class Diagonal_6:
    def __init__(self, input_array: np.ndarray | int | tuple):
        if not isinstance(input_array, np.ndarray):
            input_array = np.ones(input_array)
        self.starting_point = input_array
        self.value = 0.0
        self.gradient = np.zeros(len(self.starting_point))
        self.hessian = 0.0

    def calculate(
        self, value: bool = False, gradient: bool = False, hessian: bool = False
    ):

        n = len(self.starting_point)

        if value:
            self.value = sum(np.exp(self.starting_point) - 1 + self.starting_point)
        if gradient:
            self.gradient = np.exp(self.starting_point) + np.ones(n)
        if hessian:
            self.hessian = np.diag(np.exp(self.starting_point))

        return self.value, self.gradient, self.hessian

    def set_starting_point(self, input_array: np.array | int | tuple):
        if not isinstance(input_array, np.ndarray):
            input_array = np.ones(input_array)
        self.starting_point = input_array
        return self.starting_point

    def get_function_values(self):
        return self.value, self.gradient, self.hessian

    def get_starting_point(self):
        return self.starting_point


class Almost_Perturbed_Quardratic:

    def __init__(self, input_array: np.ndarray | int | tuple):
        if not isinstance(input_array, np.ndarray):
            input_array = np.ones(input_array)
        self.starting_point = input_array
        self.value = 0.0
        self.gradient = np.zeros(len(self.starting_point))
        self.hessian = 0.0

    def calculate(
        self, value: bool = False, gradient: bool = False, hessian: bool = False
    ):

        n = len(self.starting_point)

        if value:
            self.value = sum(
                np.arange(1, n + 1) * np.square(self.starting_point)
            ) + 1 / 100 * np.square(self.starting_point[0] + self.starting_point[-1])

        if gradient:
            self.gradient = 2 * self.starting_point * np.arange(1, n + 1)
            self.gradient[0] += (
                1 / 100 * 2 * (self.starting_point[0] + self.starting_point[-1])
            )
            self.gradient[-1] += (
                1 / 100 * 2 * (self.starting_point[0] + self.starting_point[-1])
            )
        if hessian:
            self.hessian = np.diag(2 * np.arange(1, n + 1)).astype(float)
            self.hessian[0, 0] += 2 / 100
            self.hessian[0, n - 1] += 2 / 100
            self.hessian[n - 1, n - 1] += 2 / 100
            self.hessian[n - 1, 0] += 2 / 100

        return self.value, self.gradient, self.hessian

    def set_starting_point(self, input_array: np.array | int | tuple):
        if not isinstance(input_array, np.ndarray):
            input_array = np.ones(input_array)
        self.starting_point = input_array
        return self.starting_point

    def get_function_values(self):
        return self.value, self.gradient, self.hessian

    def get_starting_point(self):
        return self.starting_point


class Hager:
    def __init__(self, input_array: np.ndarray | int | tuple):
        if not isinstance(input_array, np.ndarray):
            input_array = np.ones(input_array)
        self.starting_point = input_array
        self.value = 0.0
        self.gradient = np.zeros(len(self.starting_point))
        self.hessian = 0.0

    def calculate(
        self, value: bool = False, gradient: bool = False, hessian: bool = False
    ):

        n = len(self.starting_point)

        if value:
            self.value = sum(
                np.exp(self.starting_point)
                - np.sqrt(np.arange(1, n + 1) * (self.starting_point))
            )

        if gradient:
            self.gradient = np.exp(self.starting_point) - np.arange(
                1, n + 1
            ) / 2 / np.sqrt(np.arange(1, n + 1) * (self.starting_point))
        if hessian:
            self.hessian = np.diag(
                np.exp(self.starting_point)
                + np.sqrt(np.arange(1, n + 1)) / 4 * self.starting_point ** (-3 / 2)
            )

        return self.value, self.gradient, self.hessian

    def set_starting_point(self, input_array: np.array | int | tuple):
        if not isinstance(input_array, np.ndarray):
            input_array = np.ones(input_array)
        self.starting_point = input_array
        return self.starting_point

    def get_function_values(self):
        return self.value, self.gradient, self.hessian

    def get_starting_point(self):
        return self.starting_point


class Full_Hessian_2:
    def __init__(self, input_array: np.ndarray | int | tuple):
        if not isinstance(input_array, np.ndarray):
            input_array = np.ones(input_array)
        self.starting_point = input_array
        self.value = 0.0
        self.gradient = np.zeros(len(self.starting_point))
        self.hessian = 0.0

    def calculate(
        self, value: bool = False, gradient: bool = False, hessian: bool = False
    ):
        """TODO

        Args:
            value (bool, optional): _description_. Defaults to False.
            gradient (bool, optional): _description_. Defaults to False.
            hessian (bool, optional): _description_. Defaults to False.

        Returns:
            _type_: _description_
        """
        n = len(self.starting_point)
        isum = np.cumsum(self.starting_point)  # isum[i] = x[0] + x[1] + ... + x[i]

        if value:
            self.value = (self.starting_point[0] - 5) ** 2 + np.sum((isum[1:] - 1) ** 2)

        if gradient:
            S = isum[1:] - 1
            self.gradient[0] = 2 * (self.starting_point[0] - 5) + 2 * np.sum(S)
            self.gradient[1:] = 2 * np.cumsum(S[::-1])[::-1]

        if hessian:
            idx = np.arange(n)
            M = np.maximum(np.maximum.outer(idx, idx), 1)  # bar 1, ne 0
            self.hessian = 2 * (n - M)
            self.hessian[0, 0] += 2

        return self.value, self.gradient, self.hessian

    def set_starting_point(self, input_array: np.ndarray | int | tuple):
        if not isinstance(input_array, np.ndarray):
            input_array = np.ones(input_array)
        self.starting_point = input_array
        return self.starting_point

    def get_function_values(self):
        return self.value, self.gradient, self.hessian

    def get_starting_point(self):
        return self.starting_point


class Full_Hessian_1:
    def __init__(self, input_array: np.ndarray | int | tuple):
        if not isinstance(input_array, np.ndarray):
            input_array = np.ones(input_array)
        self.starting_point = input_array
        self.value = 0.0
        self.gradient = np.zeros(len(self.starting_point))
        self.hessian = np.zeros((len(self.starting_point), len(self.starting_point)))

    def calculate(
        self, value: bool = False, gradient: bool = False, hessian: bool = False
    ):
        """TODO

        Args:
            value (bool, optional): _description_. Defaults to False.
            gradient (bool, optional): _description_. Defaults to False.
            hessian (bool, optional): _description_. Defaults to False.

        Returns:
            _type_: _description_
        """
        n = len(self.starting_point)
        isum = np.cumsum(self.starting_point)  # isum[i] = x[0] + x[1] + ... + x[i]

        if value:
            self.value = (self.starting_point[0] - 3) ** 2 + np.sum(
                (self.starting_point[0] - 3 - 2 * isum[1:] ** 2) ** 2
            )

        if gradient:
            if n > 1:
                r = self.starting_point - 3 - 2 * isum[1:] ** 2
                T = r * isum[1:]
                # suf_T[m] = sum_{k=m+1}^{n-1} T[k-1]
                suf_T = np.cumsum(T[::-1])[::-1]
                self.gradient[1:] = -8 * suf_T
                self.gradient[0] = (
                    2 * (self.starting_point - 3) + 2 * np.sum(r) - 8 * suf_T[0]
                )
            else:
                self.gradient[0] = 2 * (self.starting_point - 3)

        if hessian:
            self.hessian = np.zeros((n, n))
            if n > 1:
                post_sum_pref = np.cumsum(isum[::-1])[
                    ::-1
                ]  # post_sum_pref[k] = isum[k]+isum[k+1]+...+isum[n-1]
                post_quad_pref = np.cumsum(isum[::-1] ** 2)[
                    ::-1
                ]  # post_quad_pref[k] = isum[k]^2+...+isum[n-1]^2

                # unutrasnji blok, indeksi 1..n-2 (bez poslednjeg indeksa n-1)
                if n > 2:
                    rows, cols = np.triu_indices(n - 2)
                    block = np.zeros((n - 2, n - 2))
                    block[rows, cols] = (
                        -8 * (n - (cols + 1)) * (self.starting_point[0] - 3)
                        + 48 * post_quad_pref[cols + 1]
                    )
                    self.hessian[1:-1, 1:-1] = block + block.T - np.diag(np.diag(block))

                # poslednji red/kolona (indeks n-1) je konstantan po celoj duzini,
                # jer je za j=n-1 uvek max(j,l) = n-1
                last_val = -8 * (self.starting_point[0] - 3 - 6 * isum[-1] ** 2)
                self.hessian[-1, 1:] = last_val
                self.hessian[1:, -1] = last_val

                # sad je cela dijagonala (1..n-1) popunjena -> moze trik preko diag()
                self.hessian[0, 1:] = np.diag(self.hessian)[1:] - 8 * post_sum_pref[1:]
                self.hessian[1:, 0] = self.hessian[0, 1:]

                self.hessian[0, 0] = 2 + np.sum(
                    2
                    * (
                        13
                        - 8 * isum[1:]
                        + 24 * isum[1:] ** 2
                        - 4 * self.starting_point[0]
                    )
                )
            else:
                self.hessian[0, 0] = 2.0

        return self.value, self.gradient, self.hessian

    def set_starting_point(self, input_array: np.ndarray | int | tuple):
        if not isinstance(input_array, np.ndarray):
            input_array = np.ones(input_array)
        self.starting_point = input_array
        return self.starting_point

    def get_function_values(self):
        return self.value, self.gradient, self.hessian

    def get_starting_point(self):
        return self.starting_point
