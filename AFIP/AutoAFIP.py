import tkinter as tk
from tkinter import messagebox
import subprocess

def Run_AFIPy_Notebook():

    """
    Executes the AFIPy.ipynb Jupyter notebook using the nbconvert command.

    """

    try:
        # Run the notebook using nbconvert with execution.
        subprocess.run(
            ["jupyter", "nbconvert", "--to", "notebook", "--execute", "AFIPy.ipynb"],
            check=True
        )
        messagebox.showinfo("Success", "AFIPy.ipynb executed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

# Create the main Tkinter window.
Root = tk.Tk()
Root.title("AFIP Reminder")
Root.geometry("300x150")

# Add a label to remind the user.
Label = tk.Label(Root, text="Tenés que hacer lo de AFIP", font=("Arial", 14))
Label.pack(pady=20)

# Add a button to initiate the notebook.
Button = tk.Button(
    Root, text="Iniciar", font=("Arial", 12), command = Run_AFIPy_Notebook
)
Button.pack(pady=10)

# Run the Tkinter main loop.
Root.mainloop()
