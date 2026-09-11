# Numerical Optimization Project

## Python GUI Application for Numerical Optimization

Numerical Optimization Project is a GUI framework for executing and testing different unconstrained optimization algorithms in Python.
The application contains a library of various test functions with pre-defined starting points. 
A several known classes of methods as well as different classes of line search procedures are covered. This application is easily extensible and contains simple API for adding new functions, methods and line searches. 

To run the application just run **main.py** file

## Adding New Functions

Functions are located in the functions/functions.py folder.
To add a new function, it is necessary to create a new class of type TestFunction, making it the child of the parent TestFunction (found in GUI). 
It is recommended that the name of the function reflects the name of the test function. 
When making the function, the user ought to define how it calculates the functions value, gradient and hessian. 
Additionally the TestFunctions class contains the current information about the point at which it is calculated, so when writing optimizers keep in mind that one ought to write the logic for "moving the starting point"

## Adding New Line Search Functions

Functions are located in the core/line_search_functions.py folder.
To add a new line search function one must add a class which inherits the LineSearchFunction class.
It is recommended that the name of the line search function reflects the name of its' implementation. 
When making the function, the user should define what the calculate_function() method should do as it is the way LineSearchMethods use it to calculate the necessary step they use for point updating. 

## Adding New methods

Methods are split across method groups, depending on which type of method group the method belongs to, that's where the method class should be written.
Incase the method written is a method which uses Line Search Functions, it is necessary to inherit the class LineSearchMethod.
Otherwise the method should inherit the OptimizationMethod class. (both are found in core/core.py)

### Adding New Methods To Existing Method Groups

If one wants to add new Methods to a Method group (ex. GradientDescent), one must add a Class named after the method one wants to make which inherits either the LineSearchMethod or OptimizationMethod parent class.
Then the user should define what the find_minimum() method in it does for that is the main way the system caclulates and finds the minimum of a given test function

### Adding New Methods To Existing Method Groups

If one wants to add a whole new Method Group, they will have to make a file in the methods folder in the following path: "methods/{method_group_name}.py". Then import the necessary modules and libraries from core and other modules.
Afterwards see the section on Adding New Methods to Existing Method Groups.


## Inspiration/Mimic

This project mimics/follows and is supported by the more robust MATLAB equivalent found on the following repo:
https://github.com/markomil/vilin-numerical-optimization/tree/master


