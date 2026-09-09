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


def check_box(root, checkbox_gui_params, gui_config, grid_elements):
    def toggle_widget():
        # .get() returns 1 if checked, 0 if unchecked
        if check_var.get() == 1:
            my_label.grid(row=1, column=0, pady=10)  # Show
        else:
            for grid_element in grid_elements:
                grid_element.grid_forget()  # Hide

    # 1. Checkbox and its variable
    check_var = tk.IntVar()
    checkbox = tk.Checkbutton(
        root, text="Show Params", variable=check_var, command=toggle_widget
    )
    checkbox.grid(row=6, column=0, padx=10, pady=10)

    # line_search_label, line_search_dropdown = combobox_row(
    #     root=root,
    #     label=gui_config["select"][0],
    #     grid_params=gui_config["select"][1],
    # )
    # # Line search parameters
    # beta_label, beta_entry = insert_row(
    #     root=root,
    #     label=gui_config["beta"][0],
    #     grid_params=gui_config["beta"][1],
    # )
    # start_point_label, start_point_entry = insert_row(
    #     root=root,
    #     label=gui_config["starting_point"][0],
    #     grid_params=gui_config["starting_point"][1],
    # )
    # m_label, m_entry = insert_row(
    #     root=root,
    #     label=gui_config["m"][0],
    #     grid_params=gui_config["m"][1],
    # )
    # sigma_label, sigma_entry = insert_row(
    #     root=root,
    #     label=gui_config["sigma"][0],
    #     grid_params=gui_config["sigma"][1],
    # )
    # rho_label, rho_entry = insert_row(
    #     root=root,
    #     label=gui_config["rho"][0],
    #     grid_params=gui_config["rho"][1],
    # )


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

        # This is the frame your real widgets get placed on
        self.body = tk.Frame(self.canvas)
        self._body_id = self.canvas.create_window((0, 0), window=self.body, anchor="nw")

        # Keep scroll region in sync with content size
        self.body.bind("<Configure>", self._on_body_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        # Mouse wheel scrolling (Windows/Mac/Linux variants)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)  # Win/Mac
        self.canvas.bind_all("<Button-4>", self._on_mousewheel_linux)  # Linux up
        self.canvas.bind_all("<Button-5>", self._on_mousewheel_linux)  # Linux down

    def _on_body_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        # Optional: uncomment to make body always at least as wide as canvas
        # self.canvas.itemconfig(self._body_id, width=event.width)
        pass

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_mousewheel_linux(self, event):
        direction = -1 if event.num == 4 else 1
        self.canvas.yview_scroll(direction, "units")


def make_responsive(container, max_row=None, max_col=None):
    """
    Makes an existing grid-based layout resize with the window,
    WITHOUT touching the code that created the widgets.

    Call this once, after your GUI class has finished building all
    its widgets on `container` (e.g. after `OptimizationGUI(...)`).

        app = OptimizationGUI(root, gui_config, ...)
        make_responsive(root)   # <-- add this one line

    What it does:
      1. Scans every widget already gridded onto `container`
         (and its child frames, recursively) and re-applies
         sticky="nsew" so each widget stretches to fill its cell.
      2. Configures every used row/column in `container` (and its
         sub-frames) with weight=1 so they grow/shrink proportionally
         instead of staying a fixed pixel size.

    This does NOT change widget creation code or grid_params values,
    it only adjusts stickiness/weight after the fact.
    """
    _apply_sticky_recursive(container)
    _apply_weights_recursive(container)


def _apply_sticky_recursive(widget):
    for child in widget.winfo_children():
        try:
            info = child.grid_info()
            if info:  # only touch widgets placed with .grid()
                child.grid_configure(sticky="nsew")
        except tk.TclError:
            pass
        # Recurse into frames/containers so nested layouts also stretch
        if child.winfo_children():
            _apply_sticky_recursive(child)


def _apply_weights_recursive(widget):
    info_list = []
    for child in widget.winfo_children():
        info = child.grid_info()
        if info:
            info_list.append(info)

    rows = {int(i["row"]) for i in info_list if "row" in i}
    cols = {int(i["column"]) for i in info_list if "column" in i}

    for r in rows:
        widget.grid_rowconfigure(r, weight=1)
    for c in cols:
        widget.grid_columnconfigure(c, weight=1)

    for child in widget.winfo_children():
        if child.winfo_children():
            _apply_weights_recursive(child)
