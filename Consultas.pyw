import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import locale

def Search_In_DataFrame():

    """
    Searches for matches in the "Descripcion" column of the DataFrame based on the user's input
    and displays the matches along with their "Precio", "Proveedor" and "Costo 1" values.

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

    # Add results to the Treeview and create buttons
    for _, Row in Matches.iterrows():

        # Format the price with "$" and thousand separators.
        try:
            Price_1 = float(Row["Costo 1"])
            Formatted_Price_1 = locale.currency(Price_1, grouping=True, international=False).split(',')[0]
        except ValueError:
            Formatted_Price_1 = "-"

        # Get "Precio" and "Proveedor" from the DataFrame
        try:
            Price = float(Row["Precio"])
            Formatted_Price = locale.currency(Price, grouping=True, international=False).split(',')[0]
        except ValueError:
            Formatted_Price = "-"

        Proveedor = Row.get("Proveedor 1", "-")

        # Add the row to the Treeview
        Result_Tree.insert("", "end", values=(Row["Descripcion"], Formatted_Price_1, Formatted_Price, Proveedor), iid=Row["Descripcion"])

    # Create the "+" buttons separately to scroll along with the Treeview
    Create_Buttons(Matches)

def Create_Buttons(Matches):
    for _, Row in Matches.iterrows():
        # Create the "+" button for the row and bind it to the function to open the detailed view
        Button = tk.Button(Button_Frame, text="+", command=lambda row=Row: Open_Detailed_Window(row), width=5, height=1)
        Button.pack(side="top", pady=5)  # Buttons stacked vertically with slight padding

def Open_Detailed_Window(Row):

    """
    Opens a new window that shows detailed information about the selected row.
    Displays the columns as rows and adds additional rows: Proveedor 2, Costo 2, Proveedor 3, Costo 3.

    """

    # Create a new window
    Detail_Window = tk.Toplevel(Root)
    Detail_Window.title(f"Detalles del producto")
    Detail_Window.iconbitmap("C:/Users/tomas/Documents/Programación/Github/Patricionog/Forrager/Pedidos/Icon.ico")
    Detail_Window.geometry("400x400")

    # Create a Treeview in the new window with rows for each detail
    Detail_Columns = ("Detalle", "Valor")
    Detail_Tree = ttk.Treeview(Detail_Window, columns=Detail_Columns, show="headings")
    Detail_Tree.heading("Detalle", text="Detalle")
    Detail_Tree.heading("Valor", text="Valor")
    Detail_Tree.column("Detalle", anchor="center", width=150)
    Detail_Tree.column("Valor", anchor="center", width=150)
    Detail_Tree.pack(fill="both", expand=True)

    # Insert the details of the product
    Detail_Tree.insert("", "end", values=("Descripcion", Row["Descripcion"]))
    Detail_Tree.insert("", "end", values=("Precio", locale.currency(float(Row["Precio"]), grouping=True, international=False).split(',')[0]))
    Detail_Tree.insert("", "end", values=("Proveedor 1", Row["Proveedor 1"]))
    Detail_Tree.insert("", "end", values=("Costo 1", locale.currency(float(Row["Costo 1"]), grouping=True, international=False).split(',')[0]))

    # Add new rows for Proveedor 2, Costo 2, Proveedor 3, Costo 3
    Detail_Tree.insert("", "end", values=("Proveedor 2", Row.get("Proveedor 2", "-")))
    Detail_Tree.insert("", "end", values=("Costo 2", locale.currency(float(Row["Costo 2"]), grouping=True, international=False).split(',')[0] if "Costo 2" in Row else "-"))
    Detail_Tree.insert("", "end", values=("Proveedor 3", Row.get("Proveedor 3", "-")))
    Detail_Tree.insert("", "end", values=("Costo 3", locale.currency(float(Row["Costo 3"]), grouping=True, international=False).split(',')[0] if "Costo 3" in Row else "-"))

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
Root.iconbitmap("C:/Users/tomas/Documents/Programación/Github/Patricionog/Forrager/Pedidos/Icon.ico")
Root.geometry("820x400")

# Create a frame for the search components (label and entry)
Search_Frame = tk.Frame(Root)
Search_Frame.pack(pady=20, padx=10, anchor="n", fill="x")  # Fill horizontally, anchor north (top)

# Create a label and entry for the search term inside the frame
Search_Label = tk.Label(Search_Frame, text="Buscar producto:")
Search_Label.pack(pady=5)

Search_Entry = tk.Entry(Search_Frame, width=50)
Search_Entry.pack(pady=5)

# Create a search button inside the frame
Search_Button = tk.Button(Search_Frame, text="Buscar", command=Search_In_DataFrame)
Search_Button.pack(pady=10)

# Create a Canvas to hold the Treeview and the Button_Frame.
Canvas = tk.Canvas(Root)
Canvas.pack(fill="both", expand=True, side="left")

# Create a vertical scrollbar for the Canvas.
Scrollbar = tk.Scrollbar(Root, orient="vertical", command=Canvas.yview)
Scrollbar.pack(side="right", fill="y")

# Create a frame inside the Canvas for the Treeview and buttons.
Scroll_Frame = tk.Frame(Canvas)
Canvas.create_window((0, 0), window=Scroll_Frame, anchor="nw")
Canvas.configure(yscrollcommand=Scrollbar.set)

# Crear un estilo para el Treeview con una mayor altura de fila
Style = ttk.Style()
Style.configure("Treeview", rowheight=36)  

# Create a Treeview to display results inside the frame
Columns = ("Descripcion", "Costo 1", "Precio", "Proveedor")
Result_Tree = ttk.Treeview(Scroll_Frame, columns=Columns, show="headings", style="Treeview")
Result_Tree.heading("Descripcion", text="Descripcion")
Result_Tree.heading("Costo 1", text="Costo")
Result_Tree.heading("Precio", text="Precio")
Result_Tree.heading("Proveedor", text="Proveedor")
Result_Tree.column("Descripcion", anchor="center", width=250)  # Center the "Descripcion" column.
Result_Tree.column("Costo 1", anchor="center", width=150)  # Center the "Costo 1" column.
Result_Tree.column("Precio", anchor="center", width=150)  # Center the "Precio" column.
Result_Tree.column("Proveedor", anchor="center", width=150)  # Center the "Proveedor" column.
Result_Tree.pack(fill="both", expand=True, pady=20, side="left", padx=10)  # Keep the Treeview on the left.

# Create a frame to hold the "+" buttons inside the Scroll_Frame
Button_Frame = tk.Frame(Scroll_Frame)
Button_Frame.pack(side="right", padx=10, anchor="n", fill="y", pady=44)

# Update the Canvas scroll region whenever the frame size changes
Scroll_Frame.bind("<Configure>", lambda e: Canvas.config(scrollregion=Canvas.bbox("all")))

# Start the Tkinter event loop.
Root.mainloop()
