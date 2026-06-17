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
    def __init__(self, input_array:np.ndarray | int | tuple):
        if not isinstance(input_array, np.ndarray):
            input_array = np.ones(input_array)
        self.starting_point = input_array
        self.value = 0.0
        self.gradient = np.zeros(len(self.starting_point))
        self.hessian = 0.0

    def calculate(self, value:bool = False, gradient:bool = False, hessian:bool = False):

        n = len(self.starting_point)

        if value:
            self.value = 1/10 * sum(np.arrange(1, n + 1)*(np.exp(self.starting_point) - self.starting_point))

        if gradient:
            self.gradient =  1/10 *np.arrange(1, n + 1)* (np.exp(self.starting_point) - 1)

        if hessian:
            self.hessian = np.diag(1/10 * np.arange(1, n + 1) * np.exp(self.starting_point))

        return self.value, self.gradient, self.hessian

    def set_starting_point(self, input_array:np.array | int | tuple):
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
        return self.starting_point

    def get_function_values(self):
        return self.value, self.gradient, self.hessian

    def get_starting_point(self):
        return self.starting_point

class Diagonal_4:
    def __init__(self, input_array:np.ndarray | int | tuple):
        if not isinstance(input_array, np.ndarray):
            input_array = np.ones(input_array)
        self.starting_point = input_array
        self.value = 0.0
        self.gradient = np.zeros(len(self.starting_point))
        self.hessian = 0.0

    def calculate(self, value:bool = False, gradient:bool = False, hessian:bool = False):

        n = len(self.starting_point)

        if value:
            self.value = 1/2 * sum(np.square(self.set_starting_point[1::2])+100*np.square(self.starting_point[::2]))
        if gradient:
            self.gradient = self.starting_point
            self.gradient[::2] *= 100 
        if hessian:
            dijagonala = np.ones(n)
            dijagonala[1::2] = 100
            self.hessian = np.diagonal(dijagonala)

        return self.value, self.gradient, self.hessian

    def set_starting_point(self, input_array:np.array | int | tuple):
        if not isinstance(input_array, np.ndarray):
            input_array = np.ones(input_array)
        self.starting_point = input_array
        return self.starting_point 
    
    def get_function_values(self):
        return self.value, self.gradient, self.hessian
    
    def get_starting_point(self):
        return self.starting_point


class Almost_Perturbed_Quardratic:

    def __init__(self, input_array:np.ndarray | int | tuple):
        if not isinstance(input_array, np.ndarray):
            input_array = np.ones(input_array)
        self.starting_point = input_array
        self.value = 0.0
        self.gradient = np.zeros(len(self.starting_point))
        self.hessian = 0.0

    def calculate(self, value:bool = False, gradient:bool = False, hessian:bool = False):

        n = len(self.starting_point)

        if value:
            self.value = sum(np.arrange(1, n + 1) * np.square(self.starting_point)) + 1/100 * np.square(self.starting_point[0] + self.set_starting_point[-1])

        if gradient:
            self.gradient = 2 * self.starting_point * np.arrange(1, n + 1)
            self.gradient[0] += 1/100 * 2 * (self.starting_point[0] + self.starting_point[-1])
            self.gradient[-1] += 1/100 * 2 * (self.starting_point[0] + self.starting_point[-1])
        if hessian:
            self.hessian = np.diag( 2 * np.arrange(1, n + 1)) 
            self.hessian[0,0] += 2/100
            self.hessian[0, n-1] += 2 * np.arrange(1, n + 1) + 2/100
            self.hessian[n-1, n-1] += 2/100
            self.hessian[n-1, 0] += 2 * np.arrange(1, n + 1) + 2/100

        return self.value, self.gradient, self.hessian

    def set_starting_point(self, input_array:np.array | int | tuple):
        if not isinstance(input_array, np.ndarray):
            input_array = np.ones(input_array) 
        self.starting_point = input_array
        return self.starting_point 
    
    def get_function_values(self):
        return self.value, self.gradient, self.hessian
    
    def get_starting_point(self):
        return self.starting_point

class Hager:
    def __init__(self, input_array:np.ndarray | int | tuple):
        if not isinstance(input_array, np.ndarray):
            input_array = np.ones(input_array)
        self.starting_point = input_array
        self.value = 0.0
        self.gradient = np.zeros(len(self.starting_point))
        self.hessian = 0.0

    def calculate(self, value:bool = False, gradient:bool = False, hessian:bool = False):

        n = len(self.starting_point)

        if value:
            self.value = sum(np.exp(self.starting_point) - np.sqrt(np.arrange(1, n + 1) * (self.starting_point)))

        if gradient:
            self.gradient =  np.exp(self.starting_point) - np.arrange(1, n + 1) / 2 / np.sqrt(np.arrange(1, n + 1) * (self.starting_point))
        if hessian:
            self.hessian = np.diag(np.exp(sel.starting_point) - np.arrange(1, n + 1) * self.starting_point**(-3/2) / 2 ) 

        return self.value, self.gradient, self.hessian

    def set_starting_point(self, input_array:np.array | int | tuple):
        if not isinstance(input_array, np.ndarray):
            input_array = np.ones(input_array) 
        self.starting_point = input_array
        return self.starting_point 
    
    def get_function_values(self):
        return self.value, self.gradient, self.hessian
    
    def get_starting_point(self):
        return self.starting_point

# class FH1:
#     def __init__(self, input_array:np.ndarray | int | tuple):
#         if not isinstance(input_array, np.ndarray):
#             input_array = np.ones(input_array)
#         self.starting_point = input_array
#         self.value = 0.0
#         self.gradient = np.zeros(len(self.starting_point))
#         self.hessian = 0.0

#     def calculate(self, value:bool = False, gradient:bool = False, hessian:bool = False):

#         n = len(self.starting_point)

#         if value:
#             self.value = (self.starting_point[0] - 3)**2 + np.sum((self.starting_point[0] - 3 - 2* np.cumsum(self.startingpoint)[1:]))

#         if gradient:
#             self.gradient[0] = 2* (x[0] - 3) + 2 * np.sum((self.starting_point[0] - 3 - 2*np.cumsum(self.starting_point)[1:] ** 2) * (1 - 4 * np.cumsum(self.starting_point)[1:]))
#             self.gradient[n-1] = -8 * ((self.starting_point[0] - 3)*np.cumsum(self.starting_point)[n-1] - 2*np.cumsum(np.cumsum(self.starting_point)**3)[::-1])[::-1]
#             self.gradient[] = -8 * (self.starting_point[0]-3)*((n-np.arange(1,n-1)*np.cumsum[np.arange(1,n-1) + np.cumsum(np.arange(n,0,-1)*self.starting_point)[::-1]]) - 2*np.cumsum(np.cumsum(self.starting_point)[1:]**3)[::-1][::-1]
#         if hessian:
#             self.hessian[n-1, np.arange(1,n)] = -8 * x[0] -3 -6* np.cumsum(self.starting_point)[n-1]**2
#             self.hessian[np.arange(1,n), n-1] = -8 * x[0] -3 -6* np.cumsum(self.starting_point)[n-1]**2

#         return self.value, self.gradient, self.hessian

#     def set_starting_point(self, input_array:np.array | int | tuple):
#         if not isinstance(input_array, np.ndarray):
#             input_array = np.ones(input_array) 
#         self.starting_point = input_array
#         return self.starting_point 
    
#     def get_function_values(self):
#         return self.value, self.gradient, self.hessian
    
#     def get_starting_point(self):
#         return self.starting_point
    
