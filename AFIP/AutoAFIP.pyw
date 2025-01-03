import tkinter as tk
from tkinter import messagebox
import subprocess
import datetime

def Run_AFIPy_Script():

    """
    Executes the AFIPy.py script using the Python interpreter.
    If today is not Wednesday or Sunday, asks the user for confirmation.

    """

    # Get the current day of the week (0 = Monday, 6 = Sunday)
    Current_Day = datetime.datetime.now().weekday()

    # Check if today is Wednesday (2) or Sunday (6)
    if Current_Day in [2, 6]:
        Run_Script = True
    else:
        # Ask the user if they want to run the script
        Run_Script = messagebox.askyesno("", "Hoy no es miércoles ni domingo. ¿Querés continuar?")

    if not Run_Script:
        messagebox.showinfo("", "El script no va a correr.")
        Root_Window.destroy()
        return

    try:
        # Hide the main window before running the script.
        Root_Window.withdraw()

        # Run the Python script using subprocess.
        subprocess.run(
            ["python", "C:/Users/tomas/Documents/Programación/Github/Patricionog/Forrager/AFIP/AFIPy.pyw"],
            check=True
        )
        messagebox.showinfo("", "BotAFIP ejecutado correctamente")
    except Exception as Error:
        messagebox.showerror("Error", f"Ocurrió un error:\n{Error}")

# Create the main Tkinter window.
Root_Window = tk.Tk()
Root_Window.title("")
Root_Window.geometry("300x150")

# Center the window on the screen.
Screen_Width = Root_Window.winfo_screenwidth()  # Get screen width.
Screen_Height = Root_Window.winfo_screenheight()  # Get screen height.
Window_Width = 500  
Window_Height = 150  
Position_Top = int(Screen_Height / 2 - Window_Height / 2)  # Calculate position Y.
Position_Left = int(Screen_Width / 2 - Window_Width / 2)  # Calculate position X.
Root_Window.geometry(f'{Window_Width}x{Window_Height}+{Position_Left}+{Position_Top}')  # Set position.

# Add an icon to the window.
Root_Window.iconbitmap('C:/Users/tomas/Documents/Programación/Github/Patricionog/Forrager/AFIP/Icon.ico') 

# Add a label to remind the user.
Reminder_Label = tk.Label(Root_Window, text="Momento de facturar en AFIP", font=("Calibri", 14))
Reminder_Label.pack(pady=20)

# Add a button to initiate the script.
Start_Button = tk.Button(
    Root_Window, text="Iniciar", font=("Calibri", 10), command=Run_AFIPy_Script
)
Start_Button.pack(pady=10)

# Run the Tkinter main loop.
Root_Window.mainloop()

