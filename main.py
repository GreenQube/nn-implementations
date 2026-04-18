import tkinter as tk
from tkinter import ttk
import numpy as np
from gui.gui import combobox_row, insert_row, gui_container
from utils import utils


class OptimizationGUI:
    def __init__(self, root, gui_config, test_functions, optimization_methods):
        self.root = root
        self.gui_config = gui_config
        self.test_functions = test_functions
        self.optimization_methods = optimization_methods
        
        self.test_function = None
        self.optimization_method = None
        self.root.title("Numerical Optimization GUI")

        # Initialize Variables No
        self.initial_variables_no = 100  # Set initial to 100

        # Select Function
        self.function_label, self.function_dropdown = combobox_row(
            root, 
            label="Select Function:", 
            grid_params=gui_config["root"]["select_function"],
            combobox_values=list(test_functions.keys())
        )
        self.function_dropdown.bind("<<ComboboxSelected>>", self.set_test_function) #

        # Select Method Group
        self.method_group_label, self.method_group_dropdown = combobox_row(
            root, 
            label="Select Method Group:", 
            grid_params=gui_config["root"]["opt_method_group"],
            combobox_values=list(optimization_methods.keys())
        )
        self.method_group_dropdown.bind("<<ComboboxSelected>>", self.update_method_options) #

        # Select Method
        self.method_label, self.method_dropdown = combobox_row(
            root, 
            label="Select Method:", 
            grid_params=gui_config["root"]["opt_method"],
        )
        self.method_dropdown.bind("<<ComboboxSelected>>", self.update_line_search_params) # 


        # Starting Point
        self.starting_point_label, self.starting_point_entry = insert_row(
            root, 
            label="Starting Point:", 
            grid_params=gui_config["root"]["starting_point"],
        )
        self.starting_point_entry.insert(0, "Select Testing Function")
        # Variables No
        self.variables_label, self.variables_entry = insert_row(
            root, 
            label="Variables No:", 
            grid_params=gui_config["root"]["variables_num"],
        )
        self.variables_entry.insert(0, str(self.initial_variables_no))  # Set initial to 100

        # Line Search Params Container
        line_search_frame = gui_container(
            root, label="Line Search Params", grid_params=gui_config["root"]["line_search_container"]
        )

        self.line_search_label, self.line_search_dropdown = combobox_row(
            root=line_search_frame, 
            label="Select Line Search:", 
            grid_params=gui_config["line_search_container"]["select"],
        )
        # Line search parameters
        self.beta_label, self.beta_entry = insert_row(
            root=line_search_frame, 
            label="Beta:", 
            grid_params=gui_config["line_search_container"]["beta"],
        )
        self.start_point_label, self.start_point_entry = insert_row(
            root=line_search_frame, 
            label="Start Point:", 
            grid_params=gui_config["line_search_container"]["starting_point"],
        )
        self.m_label, self.m_entry = insert_row(
            root=line_search_frame, 
            label="M:", 
            grid_params=gui_config["line_search_container"]["m"],
        )
        self.sigma_label, self.sigma_entry = insert_row(
            root=line_search_frame, 
            label="Sigma:", 
            grid_params=gui_config["line_search_container"]["sigma"],
        )
        self.rho_label, self.rho_entry = insert_row(
            root=line_search_frame, 
            label="Rho:", 
            grid_params=gui_config["line_search_container"]["rho"],
        )

        # Function Value per Iteration Label
        self.function_plot_label = tk.Label(root, text="Function Value:")
        self.function_plot_label.grid(row=1, column=2, sticky=tk.W, padx=10, pady=5)

        # Stopping Condition Params Container
        stopping_condition_frame = gui_container(
            root, 
            label="Stopping Condition Params", 
            grid_params=gui_config["root"]["stop_condition_container"]
        )
        
        self.max_iter_label, self.max_iter_entry = insert_row(
            root=stopping_condition_frame, 
            label="Max Iterations:", 
            grid_params=gui_config["stop_condition_container"]["max_iter"],
            initial_value="1000"
        )
        # Line search parameters
        self.beta_label, self.beta_entry = insert_row(
            root=stopping_condition_frame, 
            label="Epsilon:", 
            grid_params=gui_config["stop_condition_container"]["epsilon"],
            initial_value="1e-6"
        )
        self.start_point_label, self.start_point_entry = insert_row(
            root=stopping_condition_frame, 
            label="Work Precision:", 
            grid_params=gui_config["stop_condition_container"]["work_precision"],
            initial_value="1e-16"
        )

        # Results Container
        results_frame = gui_container(
            root, 
            label="Results", 
            grid_params=gui_config["root"]["results_container"]
        )

        # Set the Method and function rows
        self.method_result_label = tk.Label(results_frame, text="Method:")
        self.method_result_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.method_result_value = tk.Label(results_frame, text="")
        self.method_result_value.grid(row=0, column=1, padx=5, pady=5)

        self.function_result_label = tk.Label(results_frame, text="Function:")
        self.function_result_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.function_result_value = tk.Label(results_frame, text="")
        self.function_result_value.grid(row=1, column=1, padx=5, pady=5)

        # Set other results box
        self.fmin_label, self.fmin_entry = insert_row(
            root=results_frame, 
            label="Fmin:", 
            grid_params=gui_config["results_container"]["fmin"],
        )
        self.xmin_label, self.xmin_entry = insert_row(
            root=results_frame, 
            label="Xmin:", 
            grid_params=gui_config["results_container"]["xmin"],
        )
        self.iter_label, self.iter_entry = insert_row(
            root=results_frame, 
            label="Iterations:", 
            grid_params=gui_config["results_container"]["iter"],
        )
        self.grad_norm_label, self.grad_norm_entry = insert_row(
            root=results_frame, 
            label="Gradient norm:", 
            grid_params=gui_config["results_container"]["gradient_norm"],
        )
        self.f_eval_label, self.f_eval_entry = insert_row(
            root=results_frame, 
            label="Function eval no:", 
            grid_params=gui_config["results_container"]["function_eval_num"],
        )
        self.g_eval_label, self.g_eval_entry = insert_row(
            root=results_frame, 
            label="Gradient eval no:", 
            grid_params=gui_config["results_container"]["gradient_eval_num"],
        )
        self.hess_eval_label, self.hess_eval_entry = insert_row(
            root=results_frame, 
            label="Hessian eval no:", 
            grid_params=gui_config["results_container"]["hessian_eval_num"],
        )
        self.cpu_label, self.cpu_entry = insert_row(
            root=results_frame, 
            label="CPU Time:", 
            grid_params=gui_config["results_container"]["cpu_time"],
        )

        # NOTE TODO
        # ################### PLOTING ###################
        # # Plot for Function Value per Iteration
        # self.function_fig = Figure(figsize=(5, 4), dpi=100)
        # self.function_ax = self.function_fig.add_subplot(111)
        # self.function_canvas = FigureCanvasTkAgg(self.function_fig, master=root)
        # self.function_canvas.get_tk_widget().grid(row=5, column=2, padx=10, pady=5)

        # # Gradient Value per Iteration Label
        # self.gradient_plot_label = tk.Label(root, text="Gradient Value:")
        # self.gradient_plot_label.grid(row=1, column=3, sticky=tk.W, padx=10, pady=5)

        # # Plot for Gradient Value per Iteration
        # self.gradient_fig = Figure(figsize=(5, 4), dpi=100)
        # self.gradient_ax = self.gradient_fig.add_subplot(111)
        # self.gradient_canvas = FigureCanvasTkAgg(self.gradient_fig, master=root)
        # self.gradient_canvas.get_tk_widget().grid(row=5, column=3, padx=10, pady=5)
        
        ################### PLOTING ###################
        # NOTE TODO END!

        # ###### FIND MINIMUM BUTTON TODO.#######
        # # Add Find Minimum Button
        # # self.find_min_button = tk.Button(root, text="Find Minimum", command=self.on_find_minimum)
        # # self.find_min_button.grid(row=8, column=0, padx=10, pady=10)
        
        
    def set_test_function(self, event):
        # Select and Set the test function
        selected_function_name = self.function_dropdown.get() # (string, functions)
        function_name, selected_function = self.test_functions.get(selected_function_name)
        if not isinstance(self.test_function, selected_function):
            self.test_function = selected_function(input_array=self.initial_variables_no)
            starting_point = self.test_function.get_starting_point()
        else:
            dimension = int(self.variables_entry.get())
            starting_point = self.test_function.set_starting_point(input_array=dimension)
        # Get dimension from "Variables No" text box
        try:
            # Set starting point
            self.starting_point_entry.delete(0, tk.END)
            self.starting_point_entry.insert(0, str(starting_point))
        except ValueError:
            self.starting_point_entry.delete(0, tk.END)
            self.starting_point_entry.insert(0, "Invalid Dimension")

    def update_method_options(self, event):
        selected_method_group = self.method_group_dropdown.get()
        self.method_dropdown['values'] = list(self.optimization_methods[selected_method_group][1].keys())
        self.method_dropdown.current(0)  # Set first option selected

    def update_line_search_params(self, event):
        return
        
        selected_method = self.method_dropdown.get()

        if selected_method == "GradientLineSearch":
            # Populate Line Search Dropdown and enable parameters
            self.line_search_dropdown['values'] = ["Armijo", "Goldstein", "Wolfe", "FixedStepSize"]
            self.line_search_dropdown.current(0)  # Default to first option

            self.beta_entry.config(state='normal')
            self.start_point_entry.config(state='normal')
            self.m_entry.config(state='normal')
            self.sigma_entry.config(state='normal')
            self.rho_entry.config(state='normal')

            # Optionally, set default values for the entries
            self.beta_entry.delete(0, tk.END)
            self.beta_entry.insert(0, "0.5")

            self.start_point_entry.delete(0, tk.END)
            self.start_point_entry.insert(0, "1.0")

            self.m_entry.delete(0, tk.END)
            self.m_entry.insert(0, "10")

            self.sigma_entry.delete(0, tk.END)
            self.sigma_entry.insert(0, "1e-4")

            self.rho_entry.delete(0, tk.END)
            self.rho_entry.insert(0, "0.1")
        else:
            # Reset line search dropdown and disable parameters
            self.line_search_dropdown['values'] = ["Armijo", "Goldstein", "Wolfe", "FixedStepSize"]
            self.line_search_dropdown.current(2)

            self.beta_entry.config(state='normal')
            self.start_point_entry.config(state='normal')
            self.m_entry.config(state='normal')
            self.sigma_entry.config(state='normal')
            self.rho_entry.config(state='normal')

            # Optionally, set default values for the entries
            self.beta_entry.delete(0, tk.END)
            self.beta_entry.insert(0, "0.8")

            self.start_point_entry.delete(0, tk.END)
            self.start_point_entry.insert(0, "1.0")

            self.m_entry.delete(0, tk.END)
            self.m_entry.insert(0, "10")

            self.sigma_entry.delete(0, tk.END)
            self.sigma_entry.insert(0, "0.9")

            self.rho_entry.delete(0, tk.END)
            self.rho_entry.insert(0, "0.0001")

    def on_find_minimum(self):
        return
        # Collecting parameters from GUI
        variables_no = int(self.variables_entry.get())
        input_str = self.starting_point_entry.get().strip("[]")  # Remove brackets if they exist
        starting_point = [float(x) for x in input_str.split() if x]
        max_iterations = int(self.max_iter_entry.get())
        epsilon = float(self.epsilon_entry.get())
        work_precision = float(self.work_precision_entry.get())

        # Line Search parameters
        beta = float(self.beta_entry.get()) if self.beta_entry.get() else None
        sigma = float(self.sigma_entry.get()) if self.sigma_entry.get() else None
        rho = float(self.rho_entry.get()) if self.rho_entry.get() else None
        start_point = float(self.start_point_entry.get()) if self.start_point_entry.get() else None

        # Creating object params
        params = OptimizationParameters(
            variables_no=variables_no,
            starting_point=starting_point,
            max_iterations=max_iterations,
            epsilon=epsilon,
            work_precision=work_precision,
            beta=beta,
            sigma=sigma,
            rho=rho,
            start_point=start_point
        )

        # Calling function for finding minimum
        selected_function = self.function_dropdown.get()
        selected_method = self.method_dropdown.get()
        selected_line_search = self.line_search_dropdown.get()
        evaluation_numbers=EvaluationNumbers(0,0,0)

        xmin, fmin, iterations,function_values,gradient_values,grad_norm,evaluation_numbers,cpu_time = controller.find_minimum(selected_function, selected_method, selected_line_search,
                                                         params)

        # Updating results in GUI
        self.method_result_label.config(text=f"Method: {selected_method}")
        self.function_result_label.config(text=f"Function: {selected_function}")

        self.fmin_entry.delete(0, tk.END)
        self.fmin_entry.insert(0, fmin)

        self.xmin_entry.delete(0, tk.END)
        self.xmin_entry.insert(0, xmin)

        self.iter_entry.delete(0, tk.END)
        self.iter_entry.insert(0, iterations)

        self.grad_norm_entry.delete(0, tk.END)
        self.grad_norm_entry.insert(0, grad_norm)

        self.f_eval_entry.delete(0, tk.END)
        self.f_eval_entry.insert(0, evaluation_numbers.function_eval_no)

        self.g_eval_entry.delete(0, tk.END)
        self.g_eval_entry.insert(0, evaluation_numbers.gradient_eval_no)

        self.hess_eval_entry.delete(0, tk.END)
        self.hess_eval_entry.insert(0, evaluation_numbers.hessian_eval_no)

        self.cpu_entry.delete(0, tk.END)
        self.cpu_entry.insert(0, cpu_time)

        print(f"Fmin: {fmin}, Xmin: {xmin}, Iterations: {iterations}")


        # Visualization for Function Value

        self.function_ax.clear()
        self.function_ax.plot(function_values, linestyle='-', color='b')
        self.function_ax.set_title("Function Value")
        self.function_ax.set_xlabel("Iterations")
        self.function_ax.set_ylabel("Function")
        self.function_ax.grid(True)
        self.function_canvas.draw()  # Refreshing Plot

        # Visualization for Gradient Value

        self.gradient_ax.clear()
        self.gradient_ax.plot(gradient_values, linestyle='-', color='r')
        self.gradient_ax.set_title("Gradient Value")
        self.gradient_ax.set_xlabel("Iterations")
        self.gradient_ax.set_ylabel("Gradient")
        self.gradient_ax.grid(True)
        self.gradient_canvas.draw()  # Refreshing Plot




if __name__ == "__main__":
    # Get all of the gui configs, functions and optimization methods
    gui_config = utils.get_gui_configs()
    test_functions = utils.get_test_functions(use_classes=True)
    test_functions = utils.map_fancier_dict_keys(test_functions)
    optimization_methods = utils.get_all_optimization_methods()
    optimization_methods = utils.map_fancier_dict_keys(optimization_methods)
    print(gui_config, "\n")
    print(test_functions, "\n")
    print(optimization_methods, "\n")
    root = tk.Tk()
    app = OptimizationGUI(root, gui_config, test_functions, optimization_methods)
    root.mainloop()
    
    
    
    
    

