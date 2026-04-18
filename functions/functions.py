# quad_qf1.py
import numpy as np

class QuadQf1:
    def __init__(self, input_array:np.ndarray | int | tuple):
        if not isinstance(input_array, np.ndarray):
            input_array = np.ones(input_array)
        self.starting_point = input_array
        self.value = 0.0
        self.gradient = np.zeros(len(self.starting_point))
        self.hessian = 0.0
        
    def calculate(self, value:bool = False, gradient:bool = False, hessian:bool = False):
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
            self.value = 0.5 * sum(i * self.starting_point[i] ** 2 for i in range(n)) - self.starting_point[-1]

        if gradient:
            self.gradient = np.array([i * self.starting_point[i] for i in range(n)])
            self.gradient[-1] -= 1

        if hessian:
            self.hessian = np.diag(np.arange(1, n + 1))

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
        
#  # quad_qf1.py
# import numpy as np
        
# def quad_qf1(
#     function_input:np.array | int | tuple, 
#     value:bool = False, 
#     gradient:bool = False, 
#     hessian:bool = False
# ):
#     """
#     TODO

#     Args:
#         value (bool, optional): _description_. Defaults to False.
#         gradient (bool, optional): _description_. Defaults to False.
#         hessian (bool, optional): _description_. Defaults to False.

#     Returns:
#         _type_: _description_
#     """
#     if not isinstance(function_input, np.array):
#         function_input = np.ones(function_input)
    
#     n = len(function_input)
#     out_value = 0.0
#     out_gradient = np.zeros(n)
#     out_hessian = 0

#     if value:
#         out_value = 0.5 * sum(i * function_input[i] ** 2 for i in range(n)) - function_input[-1]

#     if gradient:
#         out_gradient = np.array([i * function_input[i] for i in range(n)])
#         out_gradient[-1] -= 1

#     if hessian:
#         out_hessian = np.diag(np.arange(1, n + 1))

#     return out_value, out_gradient, out_hessian

        
# def quad_qf2(
#     function_input:np.array | int | tuple, 
#     value:bool = False, 
#     gradient:bool = False, 
#     hessian:bool = False
# ):
#     """
#     TODO

#     Args:
#         value (bool, optional): _description_. Defaults to False.
#         gradient (bool, optional): _description_. Defaults to False.
#         hessian (bool, optional): _description_. Defaults to False.

#     Returns:
#         _type_: _description_
#     """
#     if not isinstance(function_input, np.array):
#         function_input = np.ones(function_input)
    
#     n = len(function_input)
#     out_value = 0.0
#     out_gradient = np.zeros(n)
    
#     c = 0.5
#     if value:
#         out_value = c * sum((i + 1) * (function_input[i] ** 2 - 1) ** 2 for i in range(n)) - function_input[-1]

#     if gradient:
#         for i in range(n):
#             out_gradient[i] = 4 * c * (i + 1) * function_input[i] * (function_input[i] ** 2 - 1)
#         out_gradient[-1] -= 1

#     if hessian:
#         out_hessian = np.zeros((n, n))
#         for i in range(n):
#             out_hessian[i, i] = 12 * c * (i + 1) * function_input[i] ** 2 - 4 * c * (i + 1)
#     else:
#         out_hessian = 0

#     return out_value, out_gradient, out_hessian