import tkinter as tk
from tkinter import ttk

def gui_container(root, label:str, grid_params:dict[str, str]):
    # Container params
    row_frame = tk.LabelFrame(root, text=label, padx=10, pady=10)
    row_frame.grid(**grid_params)
    
    return row_frame
        
def combobox_row(
    root, # root or frame
    label:str, 
    grid_params:dict[str, str],
    combobox_values: list[str] | None = None
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
    root, # root or frame
    label:str, 
    grid_params:dict[str, str],
    initial_value: str | None = None
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
        insert_value.insert(0, initial_value) # 
    
    return gui_label, insert_value

def label_row(
    root, # root or frame
    label_1:str, 
    label_2:str, 
    grid_params:dict[str, str],
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

def graph_plot():
    """TODO."""
    pass

def line_search_box(root):
    "TODO."
    def toggle_widget():
        # If checkbox is checked, show label; otherwise hide it
        if check_var.get():
            label.pack()
        else:
            label.pack_forget()

    # Checkbox variable
    check_var = tk.BooleanVar(value=True)

    # Checkbutton
    check = tk.Checkbutton(root, text="Show Widget", variable=check_var, command=toggle_widget)
    check.pack(pady=10)

    # Widget to toggle
    label = tk.Label(root, text="Hello World!", fg="blue")
    label.pack() # Initially visible

    root.mainloop()