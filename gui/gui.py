import tkinter as tk
from tkinter import ttk


def gui_container(root, label: str, grid_params: dict[str, str]):
    # Container params
    row_frame = tk.LabelFrame(root, text=label, padx=10, pady=10)
    row_frame.grid(**grid_params)

    return row_frame


def combobox_row(
    root,  # root or frame
    label: str,
    grid_params: dict[str, str],
    combobox_values: list[str] | None = None,
):
    """NOTE."""
    if "sticky" not in grid_params:
        grid_params["sticky"] = tk.W

    combobox_grid_params = {}
    for key, value in grid_params.items():
        if key == "column":
            combobox_grid_params[key] = value + 1
        elif key == "sticky":
            pass
        else:
            combobox_grid_params[key] = value

    # Set Label
    gui_label = tk.Label(root, text=label)
    gui_label.grid(**grid_params)

    if combobox_values is None:
        dropdown = ttk.Combobox(root)
    else:
        dropdown = ttk.Combobox(root, values=combobox_values)
    dropdown.grid(**combobox_grid_params)

    return gui_label, dropdown


def insert_row(
    root,  # root or frame
    label: str,
    grid_params: dict[str, str],
    initial_value: str | None = None,
):
    """NOTE."""
    if "sticky" not in grid_params:
        grid_params["sticky"] = tk.W
    insert_grid_params = {}
    for key, value in grid_params.items():
        if key == "column":
            insert_grid_params[key] = value + 1
        elif key == "sticky":
            pass
        else:
            insert_grid_params[key] = value

    # Set Lable
    gui_label = tk.Label(root, text=label)
    gui_label.grid(**grid_params)

    insert_value = tk.Entry(root)
    insert_value.grid(**insert_grid_params)
    if initial_value is not None:
        insert_value.insert(0, initial_value)  #

    return gui_label, insert_value


def label_row(
    root,  # root or frame
    label_1: str,
    label_2: str,
    grid_params: dict[str, str],
    columnspan: int | None = None,
):
    """NOTE."""
    if "sticky" not in grid_params:
        grid_params["sticky"] = tk.W
    grid_2_params = {}
    for key, value in grid_params.items():
        if key == "column":
            grid_2_params[key] = value + 1
        elif key == "sticky":
            pass
        else:
            grid_2_params[key] = value

    if columnspan is not None:
        grid_2_params["columnspan"] = columnspan

    # Set Lable
    gui_label_1 = tk.Label(root, text=label_1)
    gui_label_1.grid(**grid_params)
    gui_label_2 = tk.Label(root, text=label_2)
    gui_label_2.grid(**grid_2_params)

    return gui_label_1, gui_label_2


def set_row_value(row, value):
    """NOTE."""
    if type(value) != str:
        str_value = str(value)
    else:
        str_value = value
    row.delete(0, tk.END)
    row.insert(0, str_value)
    return row


def set_multiple_row_values(row_value_pairs: list[tuple]):
    return [set_row_value(rv_pair[0], rv_pair[1]) for rv_pair in row_value_pairs]


class ParameterForm(tk.Frame):
    def __init__(self, root, gui_parameters: dict = None, starting_row: int = 0):
        super().__init__(master=root)
        self.vars = {}  # name -> tk.Variable, keeps track of all fields
        self.starting_row = starting_row
        self.gui_parameters = gui_parameters
        if gui_parameters is not None:
            self.set_vars(gui_parameters=gui_parameters)

    def set_vars(self, gui_parameters: dict[str, any]):
        # Reset vars when you set them again
        self.vars = {}
        for row_count, (label, value) in enumerate(gui_parameters.items()):
            row_label, row_value = insert_row(
                self.master,
                label=label.upper(),
                grid_params={
                    "row": self.starting_row + row_count,
                    "column": 0,
                    "padx": 5,
                    "pady": 5,
                },
                initial_value=value,
            )
            self.vars[label] = (row_label, row_value)
        # Set the internal gui_parameters as the new ones
        self.gui_parameters = gui_parameters

    def get_values(self):
        """Return current parameter dict, reflecting any user edits."""
        if self.vars == {}:
            raise ValueError("First set Variables using set_vars")
        return {name: var[1].get() for name, var in self.vars.items()}

    def set_row_value(self, param_name, value):
        assert param_name in self.vars.keys(), "THE PARAMETER IS NOT IN THE VARS"
        row_value = self.var[param_name][1]
        row_value.insert(0, value)
        self.var[param_name] = (self.var[param_name][0], row_value)

    def set_values_of_rows(self, new_values: dict[str, any]):
        for param_name, value in new_values.items():
            self.set_value(param_name, value)

    def enable_gui(self):
        for param_name, value in self.vars.items():
            row_label, row_value = value
            # Sets all of the values to state normal
            row_value.config(state="normal")
            row_value.delete(0, tk.END)
            row_value.insert(0, str(self.gui_parameters[param_name]))

            self.vars[param_name] = (row_label, row_value)

    def disable_gui(self):
        for param_name, value in self.vars.items():
            row_label, row_value = value
            # Sets all of the values to state normal
            row_value.config(state="disabled")
            row_value.delete(0, tk.END)
            self.vars[param_name] = (row_label, row_value)

    def erase_from_gui(self):
        for param_name, value in self.vars.items():
            row_label, row_value = value
            row_label.grid_forget()
            row_value.grid_forget()
            self.vars[param_name] = (row_label, row_value)


class ScrollableFrame(tk.Frame):
    """
    A drop-in scrollable container for tkinter.

    Usage:
        root = tk.Tk()
        scroll = ScrollableFrame(root)
        scroll.pack(fill="both", expand=True)

        app = OptimizationGUI(
            scroll.body,          # <-- pass this instead of `root`
            gui_config,
            test_functions,
            optimization_methods,
            ls_functions,
        )
        root.mainloop()

    Everything placed on `scroll.body` (via .grid or .pack) will scroll
    vertically and horizontally with the mouse wheel / scrollbars if it
    doesn't fit on screen.
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Canvas + scrollbars
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        self.v_scroll = ttk.Scrollbar(
            self, orient="vertical", command=self.canvas.yview
        )
        self.h_scroll = ttk.Scrollbar(
            self, orient="horizontal", command=self.canvas.xview
        )

        self.canvas.configure(
            yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set
        )

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.v_scroll.grid(row=0, column=1, sticky="ns")
        self.h_scroll.grid(row=1, column=0, sticky="ew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Frame/Window for all widgets and rows/values of rows
        self.body = tk.Frame(self.canvas)
        self._body_id = self.canvas.create_window((0, 0), window=self.body, anchor="nw")

        # Keep scroll region in sync with content size
        self.body.bind("<Configure>", self._on_body_configure)
        # self.canvas.bind("<Configure>", self._on_canvas_configure)

        # Mouse wheel scrolling (Windows/Mac/Linux variants)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)  # Win/Mac
        self.canvas.bind_all("<Button-4>", self._on_mousewheel_linux)  # Linux up
        self.canvas.bind_all("<Button-5>", self._on_mousewheel_linux)  # Linux down

    def _on_body_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(
        self, event
    ):  # NOTE. Do I even need this since I can't make it work
        # Optional: uncomment to make body always at least as wide as canvas
        # self.canvas.itemconfig(self._body_id, width=event.width)
        pass

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_mousewheel_linux(self, event):
        direction = -1 if event.num == 4 else 1
        self.canvas.yview_scroll(direction, "units")
