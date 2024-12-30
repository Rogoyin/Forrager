import pandas as pd
import numpy as np
import re as re
from tkinter import Tk, Label, Entry, Button, Frame, Scrollbar, Canvas, StringVar, Toplevel, filedialog, PhotoImage
from tkinter.ttk import Combobox
from fpdf import FPDF
from datetime import datetime
from pathlib import Path

# Obtener el directorio del script actual.
Script_Directory = Path(__file__).parent

# Convertir a string.
Script_Directory = str(Script_Directory)

# Database con los precios.
Proveedores = f'{Script_Directory}/Proveedores.xlsx'
df_Proveedores = pd.read_excel(Proveedores, sheet_name='Centro')

# Database con los precios más baratos.
Baratos = f'{Script_Directory}/Baratos.xlsx'
df_Baratos = pd.read_excel(Baratos)

# Main function to create the window and handle the order.
def Create_Order_Interface(Baratos_DataFrame: pd.DataFrame, Proveedores_DataFrame):

    """
    Creates a graphical interface to select a provider, place an order, and generate a PDF.

    Parameters:
    - Baratos_DataFrame: DataFrame with product and provider data.
    - Proveedores_DataFrame: DataFrame with provider data.

    """

    # Convert 'Precio 1' column to numeric type.
    Baratos_DataFrame['Precio 1'] = pd.to_numeric(Baratos_DataFrame['Precio 1'], errors='coerce')

    # Filter unique providers.
    Providers = [Provider for Provider in Baratos_DataFrame['Proveedor 1'].unique() if Provider not in ["NA", "-"]]

    # Function to create the popup window with the order.
    def Open_Order_Window(Provider: str):

        # Create order DataFrame for the selected provider.
        Order_DataFrame = Baratos_DataFrame[Baratos_DataFrame['Proveedor 1'] == Provider][['Descripcion', 'Precio 1']].reset_index(drop=True)
        Order_DataFrame['Precio 1'] = pd.to_numeric(Order_DataFrame['Precio 1'], errors='coerce')

        # Create popup window.
        Order_Window = Toplevel(Root, padx=20, pady=10)
        Order_Window.title("Armar pedido")
        Order_Window.geometry("800x400")
        Order_Window.iconbitmap(f"{Script_Directory}/Icon.ico")
        Order_Window.update_idletasks()
        Width = Order_Window.winfo_width()
        Height = Order_Window.winfo_height()
        x = (Order_Window.winfo_screenwidth() // 2) - (Width // 2)
        y = (Order_Window.winfo_screenheight() // 2) - (Height // 2)
        Order_Window.geometry('{}x{}+{}+{}'.format(Width, Height, x, y))

        # Configure the main frame with scroll.
        Canvas_Frame = Canvas(Order_Window)
        Vertical_Scrollbar = Scrollbar(Order_Window, orient="vertical", command=Canvas_Frame.yview)
        Scrollable_Frame = Frame(Canvas_Frame)

        Scrollable_Frame.bind(
            "<Configure>",
            lambda e: Canvas_Frame.configure(scrollregion=Canvas_Frame.bbox("all"))
        )

        Canvas_Frame.create_window((0, 0), window=Scrollable_Frame, anchor="nw")
        Canvas_Frame.configure(yscrollcommand=Vertical_Scrollbar.set)

        Canvas_Frame.pack(side="left", fill="both", expand=True)
        Vertical_Scrollbar.pack(side="right", fill="y")

        # Add column headers.
        Headers = ["Producto", "Precio", "Pedido", "Total"]
        for Column_Index, Header in enumerate(Headers):
            Label(Scrollable_Frame, text=Header, font=("Arial", 10, "bold")).grid(row=0, column=Column_Index, padx=5, pady=5)

        # Variables and inputs for the "Order" column.
        Order_Variables = []
        Total_Labels = []

        def Update_Totals():

            """
            Updates the Total column based on the entered orders.
            
            """
            for Index, Variable in enumerate(Order_Variables):
                try:
                    Quantity = int(Variable.get())
                except ValueError:
                    Quantity = 0
                Price = Order_DataFrame.loc[Index, 'Precio 1']
                Total = Quantity * Price
                Total_Labels[Index]["text"] = f"${Total:,.0f}".replace(",", ".")

        # Populate rows with order data.
        for Index, Row in Order_DataFrame.iterrows():
            Label(Scrollable_Frame, text=Row['Descripcion'], anchor="w").grid(row=Index + 1, column=0, padx=5, pady=5, sticky="w")
            Label(Scrollable_Frame, text=f"${Row['Precio 1']:,.0f}".replace(",", ".")).grid(row=Index + 1, column=1, padx=5, pady=5)

            Order_Variable = StringVar(value="0")
            Order_Variables.append(Order_Variable)
            Order_Entry = Entry(Scrollable_Frame, textvariable=Order_Variable, width=5)
            Order_Entry.grid(row=Index + 1, column=2, padx=5, pady=5)
            Order_Entry.bind("<KeyRelease>", lambda e: Update_Totals())

            Total_Label = Label(Scrollable_Frame, text="$0")
            Total_Label.grid(row=Index + 1, column=3, padx=5, pady=5)
            Total_Labels.append(Total_Label)

        # Button to generate the PDF.
        def Generate_PDF():

            """
            Generates a PDF with the order and saves it to the specified location.
            
            """

            PDF = FPDF()
            PDF.add_page()
            PDF.set_font("Arial", size=12)

            PDF.cell(200, 10, f"Pedido - {Provider}", ln=True, align="C")
            PDF.ln(10)

            PDF.set_font("Arial", size=10)
            PDF.cell(100, 10, txt="Producto", border=1)
            PDF.cell(40, 10, txt="Precio", border=1)
            PDF.cell(20, 10, txt="Pedido", border=1)
            PDF.cell(30, 10, txt="Total", border=1)
            PDF.ln()

            for Index, Row in Order_DataFrame.iterrows():
                Quantity = int(Order_Variables[Index].get() or 0)
                if Quantity > 0:
                    Description = Row['Descripcion']
                    Price = Row['Precio 1']
                    Total = Quantity * Price

                    PDF.cell(100, 10, txt=Description, border=1)
                    PDF.cell(40, 10, txt=f"${Price:,.0f}".replace(",", "."), border=1)
                    PDF.cell(20, 10, txt=str(Quantity), border=1)
                    PDF.cell(30, 10, txt=f"${Total:,.0f}".replace(",", "."), border=1)
                    PDF.ln()

            Save_Path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], initialfile=f"Pedido a {Provider} - {datetime.now().strftime('%Y-%m-%d')}.pdf")
            if Save_Path:
                PDF.output(Save_Path)
            
            Root.destroy()

        Button(Order_Window, text="Armar pedido", command=Generate_PDF).pack(pady=10, padx=20)

        # Label to display the total sum.
        Total_Sum_Label = Label(Order_Window, text="Monto: $0", font=("Arial", 10, "bold"))
        Total_Sum_Label.pack(pady=5, padx=20)

        # Update the sum of totals.
        def Update_Total_Sum():
            Total_Sum = sum(int(Variable.get() or 0) * Order_DataFrame.loc[Index, 'Precio 1'] for Index, Variable in enumerate(Order_Variables))
            Total_Sum_Label.config(text=f"Monto: ${Total_Sum:,}".replace(",", "."))

        # Update totals function also updates the sum.
        def Update_Totals():

            for Index, Variable in enumerate(Order_Variables):
                try:
                    Quantity = int(Variable.get())
                except ValueError:
                    Quantity = 0
                Price = Order_DataFrame.loc[Index, 'Precio 1']
                Total = Quantity * Price
                Total_Labels[Index]["text"] = f"${Total:,}".replace(",", ".")
            Update_Total_Sum()

                # Function to open a new window to add a product.
        
        def Add_Product():

            """
            Opens a window to search for a product and add it to the order list.
            
            """

            Add_Window = Toplevel(Order_Window)
            Add_Window.title("Agregar producto")
            Add_Window.iconbitmap(f"{Script_Directory}/Icon.ico")
            Add_Window.geometry("400x300")
            Add_Window.transient(Order_Window)

            Label(Add_Window, text="Buscar producto:", font=("Arial", 12)).pack(pady=10)
            Product_Search_Variable = StringVar()
            Product_Search_Entry = Entry(Add_Window, textvariable=Product_Search_Variable, width=30)
            Product_Search_Entry.pack(pady=5)

            Search_Results_Frame = Frame(Add_Window)
            Search_Results_Frame.pack(fill="both", expand=True, pady=10)

            def Search_Products():

                # Clear previous results.
                for Widget in Search_Results_Frame.winfo_children():
                    Widget.destroy()

                # Filter products based on search term.
                Search_Term = Product_Search_Variable.get().lower()
                Filtered_Products = Proveedores_DataFrame[Proveedores_DataFrame['Descripcion'].str.contains(Search_Term, case=False, na=False)]

                # Display results.
                for Index, Row in Filtered_Products.iterrows():
                    Product_Button = Button(
                        Search_Results_Frame,
                        text=f"{Row['Descripcion']} - ${Row[Provider]:,.0f}".replace(",", "."),
                        anchor="w",
                        command=lambda R=Row: Add_Selected_Product(R)
                    )
                    Product_Button.pack(fill="x", padx=5, pady=2)

            def Add_Selected_Product(Product_Row):

                # Add the selected product to the order DataFrame and update the interface.

                New_Row = {'Descripcion': Product_Row['Descripcion'], 'Precio 1': Product_Row[Provider]}
                Order_DataFrame.loc[len(Order_DataFrame)] = New_Row
                Order_Variable = StringVar(value="0")
                Order_Variables.append(Order_Variable)

                # Add new product to the table.
                Row_Index = len(Order_DataFrame)
                Label(Scrollable_Frame, text=New_Row['Descripcion'], anchor="w").grid(row=Row_Index, column=0, padx=5, pady=5, sticky="w")
                Label(Scrollable_Frame, text=f"${New_Row['Precio 1']:,.0f}".replace(",", ".")).grid(row=Row_Index, column=1, padx=5, pady=5)
                Order_Entry = Entry(Scrollable_Frame, textvariable=Order_Variable, width=5)
                Order_Entry.grid(row=Row_Index, column=2, padx=5, pady=5)
                Order_Entry.bind("<KeyRelease>", lambda e: Update_Totals())
                Total_Label = Label(Scrollable_Frame, text="$0")
                Total_Label.grid(row=Row_Index, column=3, padx=5, pady=5)
                Total_Labels.append(Total_Label)
                Add_Window.destroy()

            Button(Add_Window, text="Buscar", command=Search_Products).pack(pady=5)

        # Add "Agregar producto" button.
        Button(Order_Window, text="Agregar producto", command=Add_Product).pack(pady=10, padx=20)

    # Create the main window.
    Root = Tk()
    Root.title("")
    Root.geometry("500x200")
    Root.eval('tk::PlaceWindow . center')

    # Establecer el ícono de la ventana
    Root.iconbitmap(f"{Script_Directory}/Icon.ico")

    Label(Root, text="Selecccionar proveedor:", font=("Arial", 12)).pack(pady=10)

    # Combobox to select provider.
    Provider_Variable = StringVar()
    Provider_Combobox = Combobox(Root, textvariable=Provider_Variable, values=Providers, state="readonly")
    Provider_Combobox.pack(pady=10)

    # Button to open the popup window.
    Button(Root, text="Aceptar", command=lambda: Open_Order_Window(Provider_Variable.get())).pack(pady=10)

    Root.mainloop()

Create_Order_Interface(df_Baratos, df_Proveedores)