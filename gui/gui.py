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

def check_box(root, checkbox_gui_params, gui_config, grid_elements):
    def toggle_widget():
        # .get() returns 1 if checked, 0 if unchecked
        if check_var.get() == 1:
            my_label.grid(row=1, column=0, pady=10) # Show
        else:
            for grid_element in grid_elements:
                grid_element.grid_forget() # Hide

    # 1. Checkbox and its variable
    check_var = tk.IntVar()
    checkbox = tk.Checkbutton(
        root, 
        text="Show Params", 
        variable=check_var, 
        command=toggle_widget
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

