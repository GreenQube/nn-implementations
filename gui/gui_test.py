import tkinter as tk

# 1. Create the main window
root = tk.Tk()
root.title("My App")
root.geometry("400x300")

label = tk.Label(root, text="Hello World")
label.grid(row=0, column=0) # Places label in the first cell


# # 2. Add widgets (Labels, Buttons, etc.)
# label = tk.Label(root, text="Hello, Tkinter!")
# label.pack()

# 3. Start the application
root.mainloop()
