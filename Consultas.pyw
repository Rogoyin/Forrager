import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import locale

def Search_In_DataFrame():

    """
    Searches for matches in the "Descripcion" column of the DataFrame based on the user's input
    and displays the matches along with their "Precio 1" values.

    """
    
    Search_Term = Search_Entry.get()

    if not Search_Term:
        messagebox.showwarning("Error", "Lo escribiste como el orto, escribilo bien.")
        return

    # Filter the DataFrame based on the search term.
    Matches = df[df["Descripcion"].str.contains(Search_Term, case=False, na=False)]

    # Clear the Treeview.
    for Row in Result_Tree.get_children():
        Result_Tree.delete(Row)

    # Add results to the Treeview.
    for _, Row in Matches.iterrows():

        # Format the price with "$" and thousand separators.
        try:
            # Convertir el valor a float antes de formatearlo
            Price = float(Row["Precio 1"])
            Formatted_Price = locale.currency(Price, grouping=True, international=False).split(',')[0]
        except ValueError:
            Formatted_Price = "-"

        Result_Tree.insert("", "end", values=(Row["Descripcion"], Formatted_Price))

# Set the locale for currency formatting
locale.setlocale(locale.LC_ALL, 'es_AR.UTF-8')  # Set to Argentina locale for correct formatting.

# Load the Excel file into a DataFrame.
try:
    df = pd.read_excel("J:/My Drive/Forraje/Baratos.xlsx")  

except Exception as e:
    print("Error cargando Excel:", e)
    exit()

# Create the main application window.
Root = tk.Tk()
Root.title("Buscador de productos")
Root.iconbitmap("Pedidos/Icon.ico")
Root.geometry("600x400")

# Create a label and entry for the search term.
Search_Label = tk.Label(Root, text="Buscar producto:")
Search_Label.pack(pady=5)

Search_Entry = tk.Entry(Root, width=50)
Search_Entry.pack(pady=5)

# Create a search button.
Search_Button = tk.Button(Root, text="Buscar", command=Search_In_DataFrame)
Search_Button.pack(pady=10)

# Create a Treeview to display results.
Columns = ("Descripcion", "Precio 1")
Result_Tree = ttk.Treeview(Root, columns=Columns, show="headings")
Result_Tree.heading("Descripcion", text="Descripcion")
Result_Tree.heading("Precio 1", text="Precio")
Result_Tree.column("Descripcion", anchor="center", width=250)  # Center the "Descripcion" column
Result_Tree.column("Precio 1", anchor="center", width=150)  # Center the "Precio" column
Result_Tree.pack(fill="both", expand=True, pady=10)

# Add a vertical scrollbar to the Treeview.
Scrollbar = tk.Scrollbar(Root, orient="vertical", command=Result_Tree.yview)
Scrollbar.pack(side="right", fill="y")
Result_Tree.configure(yscrollcommand=Scrollbar.set)

# Start the Tkinter event loop.
Root.mainloop()
