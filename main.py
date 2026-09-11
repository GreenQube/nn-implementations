import tkinter as tk
from tkinter import ttk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from gui.gui import (
    combobox_row,
    insert_row,
    gui_container,
    label_row,
    ParameterForm,
    ScrollableFrame,
)
from utils import utils


class OptimizationGUI:
    def __init__(
        self,
        root,
        gui_config,
        test_functions,
        optimization_methods,
        line_search_functions,
    ):
        self.root = root
        self.gui_config = gui_config
        self.test_functions = test_functions
        self.optimization_methods = optimization_methods
        self.line_search_functions = line_search_functions

        self.test_function = None
        self.optimization_method = None
        self.line_search_function = None
        self.root.title("Numerical Optimization GUI")

        # Initialize Variables No
        self.initial_variables_no = 100  # Set initial to 100
        self.ls_gui_parameters = None

        # Select Function
        self.function_label, self.function_dropdown = combobox_row(
            root,
            label="Select Function:",
            grid_params=gui_config["root"]["select_function"],
            combobox_values=list(test_functions.keys()),
        )
        self.function_dropdown.bind("<<ComboboxSelected>>", self.set_test_function)  #

        # Select Method Group
        self.method_group_label, self.method_group_dropdown = combobox_row(
            root,
            label="Select Method Group:",
            grid_params=gui_config["root"]["opt_method_group"],
            combobox_values=list(optimization_methods.keys()),
        )
        self.method_group_dropdown.bind(
            "<<ComboboxSelected>>", self.update_method_options
        )  #

        # Select Method
        self.method_label, self.method_dropdown = combobox_row(
            root,
            label="Select Method:",
            grid_params=gui_config["root"]["opt_method"],
        )
        self.method_dropdown.bind("<<ComboboxSelected>>", self.update_method_settings)

        # Starting Point
        self.starting_point_label, self.starting_point_entry = insert_row(
            root,
            label="Starting Point:",
            grid_params=gui_config["root"]["starting_point"],
            initial_value="Select Testing Function",
        )
        # Variables No
        self.variables_label, self.variables_entry = insert_row(
            root,
            label="Variables No:",
            grid_params=gui_config["root"]["variables_num"],
            initial_value=str(self.initial_variables_no),
        )

        # Line Search Params Container
        self.line_search_frame = gui_container(
            root,
            label="Line Search Params",
            grid_params=gui_config["root"]["line_search_container"],
        )
        self.line_search_label, self.line_search_dropdown = combobox_row(
            root=self.line_search_frame,
            label="Select Line Search:",
            grid_params=self.gui_config["line_search_container"]["select"],
        )
        self.line_search_dropdown.bind(
            "<<ComboboxSelected>>", self.set_line_search_function
        )
        self.ls_frame_params = ParameterForm(  # dict[str, tuple]
            root=self.line_search_frame, starting_row=2
        )

        # Checkbox
        self.ls_check_var = tk.BooleanVar(value=True)
        self.ls_checkbox = tk.Checkbutton(
            self.line_search_frame,
            text="Show Params",
            variable=self.ls_check_var,
            command=self.toggle_ls_visibility,
        )
        # self.toggle_ls_visibility()
        self.ls_checkbox.grid(row=0, column=0, padx=10, pady=10)

        # Stopping Condition Params Container
        stopping_condition_frame = gui_container(
            root,
            label="Stopping Condition Params",
            grid_params=gui_config["root"]["stop_condition_container"],
        )

        self.max_iter_label, self.max_iter_entry = insert_row(
            root=stopping_condition_frame,
            label="Max Iterations:",
            grid_params=gui_config["stop_condition_container"]["max_iter"],
            initial_value="1000",
        )
        # Line search parameters
        self.epsilon_label, self.epsilon_entry = insert_row(
            root=stopping_condition_frame,
            label="Epsilon:",
            grid_params=gui_config["stop_condition_container"]["epsilon"],
            initial_value="1e-6",
        )
        self.work_precision_label, self.work_precision_entry = insert_row(
            root=stopping_condition_frame,
            label="Work Precision:",
            grid_params=gui_config["stop_condition_container"]["work_precision"],
            initial_value="1e-12",
        )

        # Results Container
        results_frame = gui_container(
            root, label="Results", grid_params=gui_config["root"]["results_container"]
        )

        # Set the Method and function rows
        self.method_result_label, self.method_result_value = label_row(
            root=results_frame,
            label_1="Method:",
            label_2="",
            grid_params=gui_config["results_container"]["method_result"],
            columnspan=3,
        )

        self.function_result_label, self.function_result_value = label_row(
            root=results_frame,
            label_1="Function:",
            label_2="",
            grid_params=gui_config["results_container"]["function_result"],
            columnspan=3,
        )

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

        # ################### PLOTING ###################
        # Plot for Function Value per Iteration

        # Gradient Value per Iteration Label
        self.gradient_plot_label = tk.Label(root, text="Gradient Value:")
        self.gradient_plot_label.grid(row=1, column=2, sticky=tk.W, padx=10, pady=5)

        # Plot for Gradient Value per Iteration
        self.gradient_fig = Figure(figsize=(5, 4), dpi=100)
        self.gradient_ax = self.gradient_fig.add_subplot(111)
        self.gradient_canvas = FigureCanvasTkAgg(self.gradient_fig, master=root)
        self.gradient_canvas.get_tk_widget().grid(row=5, column=2, padx=10, pady=5)

        ###############    TOOLBAR    ###############
        toolbar_frame_gradient = tk.Frame(root)
        # toolbar_frame_gradient.grid(row=6, column=3)  # row was 21
        toolbar_frame_gradient.grid(
            row=6, column=3, padx=10, pady=5, sticky="nw"
        )  # row was 21
        gradient_toolbar = NavigationToolbar2Tk(
            self.gradient_canvas, toolbar_frame_gradient
        )

        # Function Value per Iteration Label
        self.function_plot_label = tk.Label(root, text="Function Value:")
        self.function_plot_label.grid(row=1, column=3, sticky=tk.W, padx=10, pady=5)

        self.function_fig = Figure(figsize=(5, 4), dpi=100)
        self.function_ax = self.function_fig.add_subplot(111)
        self.function_canvas = FigureCanvasTkAgg(self.function_fig, master=root)
        self.function_canvas.get_tk_widget().grid(row=5, column=3, padx=10, pady=5)
        ###############    TOOLBAR    ###############
        toolbar_frame_function = tk.Frame(root)
        toolbar_frame_function.grid(
            row=6, column=2, padx=10, pady=5, sticky="nw"
        )  # row was 21
        function_toolbar = NavigationToolbar2Tk(
            self.function_canvas, toolbar_frame_function
        )

        # ###### FIND MINIMUM BUTTON TODO.#######
        # Add Find Minimum Button
        self.find_min_button = tk.Button(
            root, text="Find Minimum", command=self.on_find_minimum, width=20, height=2
        )
        self.find_min_button.grid(row=7, column=0, padx=10, pady=10)

    ######################################################################################################################################
    # Function for setting the test function. NOTE. There is probably a bug here setting the init values.
    def set_test_function(self, event=None):
        # Select and Set the test function
        selected_function_name = self.function_dropdown.get()  # (string, functions)
        function_name, selected_function = self.test_functions.get(
            selected_function_name
        )

        dimension = int(self.variables_entry.get())
        # If the selected test function is not the same instance of the shown one
        if not isinstance(self.test_function, selected_function):
            self.test_function = selected_function(input_array=dimension)
            starting_point = self.test_function.set_starting_point(
                input_array=dimension
            )
        # If it is, (i've selected QT1 as QT1)
        else:
            starting_point = self.test_function.set_starting_point(
                input_array=dimension
            )

        # Get dimension from "Variables No" text box
        try:
            # Set starting point
            self.starting_point_entry.delete(0, tk.END)
            self.starting_point_entry.insert(0, str(starting_point))
        except ValueError:
            self.starting_point_entry.delete(0, tk.END)
            self.starting_point_entry.insert(0, "Invalid Dimension")

    # Updates the method group thingy -> chosing the method you want
    def update_method_options(self, event=None):
        """
        When a method is picked, shows the list of methods
        as well as updates the line search parameters.
        """
        selected_method_group = self.method_group_dropdown.get()
        self.method_dropdown["values"] = list(
            self.optimization_methods[selected_method_group][1].keys()
        )
        self.method_dropdown.current(0)  # Set first option selected
        self.update_method_settings(event)

    # Function for updating method settings - ls fields
    def update_method_settings(self, event=None):
        """
        Updates the Line Search Parameters, when selected in GUI,
        sets all of the values. As well as checking if you should use LS Parameters

        If the method picked has line search, enables them.
        If not, disables them and grays them out.
        """
        # 1) Get the selected method from the method group
        selected_method_group = self.method_group_dropdown.get()
        selected_method_name = self.method_dropdown.get()
        selected_method = self.optimization_methods[selected_method_group][1][
            selected_method_name
        ]()  # instance of class

        # 2) Check if the selected method uses line_search
        if selected_method.use_line_search:
            # Turn on checkbox config
            self.ls_checkbox.config(state="normal")
            self.line_search_dropdown.config(state="normal")

            # 2.1) Populate Line Search Dropdown and enable parameters
            if not self.line_search_dropdown["values"]:
                self.line_search_dropdown["values"] = list(
                    self.line_search_functions.keys()
                )

                self.line_search_dropdown.current(0)  # Default to first option

            # 2.2) Set the line search function.
            self.set_line_search_function(event)

            # 2.3) Enables The GUI Interaction
            self.ls_frame_params.enable_gui()
        else:
            # Disables the GUI Interaction and Grays out the fields for the Selection.
            self.ls_checkbox.config(state="disabled")
            self.line_search_dropdown.config(state="disabled")
            # Disables the GUI Interaction and Grays out the fields For Line Search
            # This doesen't work sometimes, probably when I select a non method ->
            # it gets removed -> so disable_gui has nothing to disable
            self.ls_frame_params.disable_gui()

    # Function for setting the variables for the Line Search Parameters
    def set_line_search_function(self, event=None):
        # Get the line search function
        self.line_search_function = self.line_search_functions[
            self.line_search_dropdown.get()  # dropdopwn value
        ]()

        # Set global ls_gui_parameters
        self.ls_gui_parameters = self.line_search_function.get_parameters()

        # Erase the last things from gui so the new pick doesen't overlap
        self.ls_frame_params.erase_from_gui()
        # Set the frame parameters using the chokes line search
        self.ls_frame_params.set_vars(gui_parameters=self.ls_gui_parameters)
        if not self.ls_check_var.get():
            self.ls_frame_params.erase_from_gui()

    def toggle_ls_visibility(self, event=None):
        # Make them appear and dissapear
        if self.ls_check_var.get():
            # Set the values again
            self.set_line_search_function(event)
        else:
            self.ls_frame_params.erase_from_gui()

    def on_find_minimum(self, event=None):

        # Collecting parameters from GUI
        # Remove bracket
        input_str = self.starting_point_entry.get().strip("[]")
        starting_point = [float(x) for x in input_str.split() if x]
        starting_point = np.asarray(starting_point)

        # Get stopping parameters
        max_iterations = int(self.max_iter_entry.get())
        epsilon = float(self.epsilon_entry.get())
        work_precision = float(self.work_precision_entry.get())

        # NOTE.NEED THIS UPDATED? Creating object params
        # start_point = (
        #     float(self.start_point_entry.get())
        #     if self.start_point_entry.get()
        #     else None
        # )
        # variables_no = int(self.variables_entry.get())

        # params = {
        #     "variables_no": variables_no,  #  NOTE. might be useful later?. Ask Jana
        #     "start_point": start_point,  #  NOTE. might be useful later?
        # }
        # NOTE.NEED THIS UPDATED? Creating object params

        stopping_condition_params = {
            "max_iterations": max_iterations,  # USED
            "epsilon": epsilon,  # USED
            "work_precision": work_precision,  # USED
        }

        # Make object of optimization class
        op_method_group = self.optimization_methods[self.method_group_dropdown.get()][1]
        self.optimization_method = op_method_group[self.method_dropdown.get()]()

        # Gets and sets the Line Step Function depending on which it is.
        if self.optimization_method.use_line_search:
            # Update the values in the line search with the values entered.
            self.line_search_function.set_parameters(self.ls_frame_params.get_values())
            self.optimization_method.set_line_step_function(self.line_search_function)

        verbose = False
        if verbose:
            print()
            print("Showing Verbose Data:")
            print("Optimization Method Group")
            print(type(op_method_group))
            print("Optimization Method")
            print(type(self.optimization_method))
            print("Test Function")
            print(type(self.test_function))
            print("Line Search Function")
            print(type(self.line_search_function))
            if self.line_search_function is not None:
                print("LS Params")
                print(self.line_search_function.parameters)
            print()

        # Get the find minimum.
        results = self.optimization_method.find_minimum(
            self.test_function, starting_point, stopping_condition_params
        )

        # Updating results in GUI
        self.method_result_label.config(text=f"Method: {self.method_dropdown.get()}")
        self.function_result_label.config(
            text=f"Function: {self.function_dropdown.get()}"
        )

        self.fmin_entry.delete(0, tk.END)
        self.fmin_entry.insert(0, results.get("fmin").round(6))

        self.xmin_entry.delete(0, tk.END)
        self.xmin_entry.insert(0, results.get("current_point").round(6))

        self.iter_entry.delete(0, tk.END)
        self.iter_entry.insert(0, results.get("iteration"))

        self.grad_norm_entry.delete(0, tk.END)
        self.grad_norm_entry.insert(0, results.get("grad_norm").round(6))

        self.f_eval_entry.delete(0, tk.END)
        self.f_eval_entry.insert(0, results.get("eval_numbers")[0])

        self.g_eval_entry.delete(0, tk.END)
        self.g_eval_entry.insert(0, results.get("eval_numbers")[1])

        self.hess_eval_entry.delete(0, tk.END)
        self.hess_eval_entry.insert(0, results.get("eval_numbers")[2])

        self.cpu_entry.delete(0, tk.END)
        self.cpu_entry.insert(0, results.get("exec_time"))

        # Visualization for Function Value
        self.function_ax.clear()
        self.function_ax.plot(results.get("function_values"), linestyle="-", color="b")
        self.function_ax.set_title("Function Value")
        self.function_ax.set_xlabel("Iterations")
        self.function_ax.set_ylabel("Function")
        self.function_ax.grid(True)
        self.function_ax.ticklabel_format(
            axis="y", style="sci", scilimits=(0, 0), useOffset=False
        )
        self.function_canvas.draw()  # Refreshing Plot

        # Visualization for Gradient Value
        self.gradient_ax.clear()
        self.gradient_ax.plot(results.get("gradient_values"), linestyle="-", color="r")
        self.gradient_ax.set_title("Gradient Value")
        self.gradient_ax.set_xlabel("Iterations")
        self.gradient_ax.set_ylabel("Gradient")
        self.gradient_ax.grid(True)
        self.gradient_ax.ticklabel_format(
            axis="y", style="sci", scilimits=(0, 0), useOffset=False
        )
        self.gradient_canvas.draw()  # Refreshing Plot


if __name__ == "__main__":
    # Get all of the gui configs, functions and optimization methods
    gui_config = utils.get_gui_configs()
    # Test Functions
    test_functions = utils.get_test_functions(use_classes=True)
    test_functions = utils.map_fancier_dict_keys(test_functions)

    # Optimization Methods
    optimization_methods = utils.get_all_optimization_methods()
    optimization_methods = utils.map_fancier_dict_keys(optimization_methods)

    # Line Search Methods
    ls_functions = utils.get_line_search_functions()
    ls_functions = {k.capitalize(): v for k, v in ls_functions.items()}

    root = tk.Tk()
    scrollable = True
    if scrollable:
        root.geometry("1200x800")  # optional starting size
        scroll = ScrollableFrame(root)
        scroll.pack(fill="both", expand=True)

        scroll.body.title = root.title  # <-- forwards .title() calls to the real window

        app = OptimizationGUI(
            scroll.body,
            gui_config,
            test_functions,
            optimization_methods,
            ls_functions,
        )
    else:
        app = OptimizationGUI(
            root,
            gui_config,
            test_functions,
            optimization_methods,
            ls_functions,
        )
    root.mainloop()
