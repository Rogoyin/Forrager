   
# Hectopar.
Hectopar = ['Pipeta Hectopar 00-04 kg.', 'Pipeta Hectopar 05-10 kg.', 'Pipeta Hectopar 10-25 kg.',
            'Pipeta Hectopar 25-40 kg.', 'Pipeta Hectopar 40-60 kg.']
Contador = 50 
for i in range (0, len(Hectopar)):    
    df = Filtrar_y_Rellenar(df, 'Descripcion', Hectopar[i], 'Markup %', Contador)
    Contador = Contador + 5
    
    
# Hectopar Gato.
Hectopar_Gato = ['Pipeta Hectopar Gato 00-04 kg.', 'Pipeta Hectopar Gato 05-08 kg.']
Contador = 50 
for i in range (0, len(Hectopar_Gato)):    
    df = Filtrar_y_Rellenar(df, 'Descripcion', Hectopar_Gato[i], 'Markup %', Contador)
    Contador = Contador + 5

# Columna Precio Proveedores.

df['Precio Proveedores'] = df['Costo Proveedores']* (1 + (df['Markup %']/100))


# Llenamos df de 0 si hay NaN.
df = df.fillna(0)

# Columna de Relaciones.

df['Precio Relacion'] = df['Precio Proveedores'] / df['Precio Sistema']
df['Costo Relacion'] = df['Costo Proveedores'] / df['Costo Sistema']


# Columna Costo Final.
df['Costo Final'] = df.apply(lambda row: max(row['Costo Sistema'], row['Costo Proveedores']), axis=1)

# Columna Precio Final.
df['Precio Final'] = df.apply(lambda row: max(row['Precio Sistema'], row['Precio Proveedores']), axis=1)

# Redondeo de Precio Final.
df['Precio Final'] = df['Precio Final'].apply(lambda x: math.ceil(x / 10) * 10)

# Columna Markup Final.
df['Markup Final'] = (df['Precio Final']/df['Costo Final']) - 1

# Columna Markup.
df['Markup %'] = df['Markup %']/100
# Arreglamos precios de ofertas.
for i in range(0, len(df)):
    Producto = df['Descripcion'][i]
    for j in range(0, len(Ofertas)):
        if Producto in Ofertas:
            df.at[i, 'Precio Final'] = Ofertas[Producto]
df[df['Descripcion'] == 'Solo x 15 kg.']

# Ordenar columnas.
Orden = ['Codigo', 'Descripcion', 'Precio Final', 'Costo Final', 'Markup Final',
         'Costo Sistema', 'Costo Proveedores', 'Precio Sistema', 'Precio Proveedores', 
         'Precio Relacion','Costo Relacion', 
         'Markup %', 'Proveedor', 'Categoria']

# Reasigna el DataFrame con el nuevo orden de columnas
df = df[Orden]

# Mostrar dos decimales en la columna Precio Relacion y Costo Relacion.

# Configurar la opción de Pandas para mostrar dos decimales
pd.options.display.float_format = '{:.2f}'.format

# Configurar Pandas para mostrar todas las filas.
pd.set_option('display.max_rows', None)

df 

# Database entero.

# Guardar archivo.
Ruta = 'J:/My Drive/Forraje/Resultados/Resultados.xlsx'

# Guardar
df.to_excel(Ruta, index=False) 

# Cargamos Excel.
Libro = load_workbook(Ruta) 

# Seleccionar hoja activa.
Hoja = Libro.active 

# Anchos.
Hoja.column_dimensions["A"].width = 15 
Hoja.column_dimensions["B"].width = 40
Hoja.column_dimensions["C"].width = 15 
Hoja.column_dimensions["D"].width = 15 
Hoja.column_dimensions["E"].width = 15 
Hoja.column_dimensions["F"].width = 15 
Hoja.column_dimensions["G"].width = 15 
Hoja.column_dimensions["H"].width = 15 
Hoja.column_dimensions["I"].width = 15 
Hoja.column_dimensions["J"].width = 15 
Hoja.column_dimensions["K"].width = 15 
Hoja.column_dimensions["L"].width = 15 
Hoja.column_dimensions["M"].width = 20 
Hoja.column_dimensions["N"].width = 20 

# Inmovilizar paneles
Hoja.freeze_panes = 'C2'
#.-

# Formato $ con dos decimales para columnas de precios y costos.
Estilo = NamedStyle(name="currency")

# Decimales.
Estilo.number_format = '$#,##0'

# Columnas.
Columnas_con_Peso = ["F", "G", "H", "I"]

for Columna in Columnas_con_Peso:
    for Celda in Hoja[Columna]:
        Celda.style = Estilo
#.-

# Formato general con dos decimales para columnas de relación.
General = NamedStyle(name="general")

# Decimales.
General.number_format = '0.00'

# Columnas.
for Columna in ["J", "K"]:
    for Celda in Hoja[Columna]:
        Celda.style = General
#.-

# Formato general con porcentaje y sin decimales para columna de markup.
General.number_format = '0%'

# Columnas.
for Columna in ["E", "L"]:
    for Celda in Hoja[Columna]:
        Celda.style = General
#.-

# Formato general con cero decimales para columnas de precio final y costo final.
for Columna in ["C", "D"]:
    for Celda in Hoja[Columna]:
        Celda.number_format = '0'

# Centrar.
Centrar = Alignment(horizontal='center', vertical='center')

# Iteración sobre cada celda de la fila.

for i in Hoja.columns:
    for Celda in i:
        Celda.alignment = Centrar

# Duplica la hoja 2 veces.
Hoja2_Nombre = "Hoja2"
Hoja2 = Libro.copy_worksheet(Hoja)
Hoja2.title = Hoja2_Nombre

Hoja3_Nombre = "Hoja3"
Hoja3 = Libro.copy_worksheet(Hoja)
Hoja3.title = Hoja3_Nombre 

# Formato condicional de color rojo en Costo Final para comparación Costo Final - Costo Sistema anterior.
for Fila in Hoja.iter_rows(min_row=2, min_col=4, max_row=Hoja.max_row, max_col=6):  
    for Celda1, Celda2 in zip(Fila, Fila[2:]):
        if abs(Celda1.value - Celda2.value) < 5:
            None
        else:
            Celda1.fill = PatternFill(start_color="FF6666", end_color="FF6666", fill_type="solid") 

# Formato condicional de color verde en Precio Final para comparación Precio Final - Precio Sistema.
for Fila in Hoja.iter_rows(min_row=2, min_col=3, max_row=Hoja.max_row, max_col=8):  
    for Celda1, Celda2 in zip(Fila, Fila[5:]):
        if abs(Celda1.value - Celda2.value) < 21:
            None
        else:
            Celda1.fill = PatternFill(start_color="89ac76", end_color="89ac76", fill_type="solid")
            Celda1.font = Font(bold=True) 

# Formato condicional de color azul en Costo Proveedores para comparación Costo Final - Costo Proveedores (cuando este sea bajo).
for Fila in Hoja2.iter_rows(min_row=2, min_col=4, max_row=Hoja2.max_row-1, max_col=7):  
    for Celda1, Celda2 in zip(Fila, Fila[3:]):
        if abs(Celda1.value - Celda2.value) > 21:
            if Celda2.value == 0:
                None
            else:
                Celda2.fill = PatternFill(start_color="B0E0E6", end_color="B0E0E6", fill_type="solid")
                Celda2.font = Font(bold=True) 

# Formato condicional de color naranja en Costo Final para comparación Costo Final - Costo Proveedores (cuando este sea alto).
for Fila in Hoja3.iter_rows(min_row=2, min_col=4, max_row=Hoja3.max_row-1, max_col=7):  
    for Celda1, Celda2 in zip(Fila, Fila[3:]):
        if Celda1.value - Celda2.value < 0:
            if Celda2.value == 0:
                None
            else:
                Celda1.fill = PatternFill(start_color="FFA500", end_color="FFA500", fill_type="solid")
                Celda1.font = Font(bold=True) 

# Formato de filtro a la primera fila de la Hoja 1.
Hoja.auto_filter.ref = Hoja.dimensions

# Obtener las filas que tienen formato condicional aplicado.
Filas_Negrita = set()
for Fila in Hoja.iter_rows(min_row=2, max_row=Hoja.max_row, min_col=3, max_col=3):  
    for Celda in Fila:
        if Celda.font == Font(bold=True): 
            Filas_Negrita.add(Fila[0].row)

# Ocultar todas las filas.
for i in range(2, Hoja.max_row + 1):  # Empezar desde la fila 2 ya que la fila 1 contiene los encabezados
    Hoja.row_dimensions[i].hidden = True

# Mostrar solo las filas con formato condicional aplicado.
for Fila in Filas_Negrita:
    Hoja.row_dimensions[Fila].hidden = False
 

# Contar el número de celdas con negrita.
Negrita = len(Filas_Negrita)

# Escribir el número de celdas con negrita en la fila siguiente a la última fila del documento
Fila_Ultima = Hoja.max_row + 1
Celda_Texto = Hoja.cell(row=Fila_Ultima, column=3)
Celda_Texto.value = "Productos:"
Celda_Texto.alignment = Alignment(horizontal="center")
Celda_Resultado = Hoja.cell(row=Fila_Ultima, column=4)
Celda_Resultado.value = Negrita
Celda_Resultado.alignment = Alignment(horizontal="center") 

# Formato de filtro a la primera fila de la Hoja 2 y 3.
Hoja2.auto_filter.ref = Hoja2.dimensions
Hoja3.auto_filter.ref = Hoja3.dimensions

# Obtener las filas que tienen formato condicional aplicado en Hoja 2 y 3.
Filas_Negrita_2 = set()
for Fila in Hoja2.iter_rows(min_row=2, max_row=Hoja2.max_row, min_col=7, max_col=7):  
    for Celda in Fila:
        if Celda.font == Font(bold=True): 
            Filas_Negrita_2.add(Fila[0].row)

# Ocultar todas las filas en Hoja 2.
for i in range(2, Hoja2.max_row + 1):  # Empezar desde la fila 2 ya que la fila 1 contiene los encabezados
    Hoja2.row_dimensions[i].hidden = True

# Mostrar solo las filas con formato condicional aplicado en Hoja 2.
for Fila in Filas_Negrita_2:
    Hoja2.row_dimensions[Fila].hidden = False

# Lo mismo para la Hoja 3. 
    
Filas_Negrita_3 = set()
for Fila in Hoja3.iter_rows(min_row=2, max_row=Hoja3.max_row, min_col=7, max_col=7):  
    for Celda in Fila:
        if Celda.font == Font(bold=True): 
            Filas_Negrita_3.add(Fila[0].row)
            
for i in range(2, Hoja3.max_row + 1):  # Empezar desde la fila 2 ya que la fila 1 contiene los encabezados
    Hoja3.row_dimensions[i].hidden = True           
            
for Fila in Filas_Negrita_3:
    Hoja3.row_dimensions[Fila].hidden = False

# Inmovilizar paneles en Hoja2 y 3.
Hoja2.freeze_panes = 'C2'
Hoja3.freeze_panes = 'C2'

# Calcula el número de filas en la Hoja2.
Filas = Hoja2.max_row

# Itera sobre todas las filas y mueve los valores de la columna
for i in range(1, Filas):
    # Obtiene el valor de la celda en la columna de origen
    Valor_Celda_Origen = Hoja2.cell(row=i, column=7).value
    
    # Inserta el valor en la nueva posición
    Hoja2.cell(row=i, column=5).value = Valor_Celda_Origen

# Elimina la columna original
Hoja2.delete_cols(7)

# Calcula el número de filas en la Hoja3.
Filas = Hoja3.max_row

# Itera sobre todas las filas y mueve los valores de la columna
for i in range(1, Filas):
    # Obtiene el valor de la celda en la columna de origen
    Valor_Celda_Origen = Hoja3.cell(row=i, column=7).value
    
    # Inserta el valor en la nueva posición
    Hoja3.cell(row=i, column=5).value = Valor_Celda_Origen

# Elimina la columna original
Hoja3.delete_cols(7)
#.-

# Formato para las columnas de interés en Hoja2.

# Decimales.
General.number_format = '0'

# Columnas.
for Columna in ["D","E"]:
    for Celda in Hoja2[Columna]:
        Celda.style = General
        Celda.alignment = Centrar
        Celda.fill = PatternFill(start_color="808080", end_color="808080", fill_type="solid")
        
for Celda in Hoja2["E"]:
    Celda.fill = PatternFill(start_color="87CEEB", end_color="87CEEB", fill_type="solid")
#.-

# Formato para las columnas de interés en Hoja3.

# Decimales.
General.number_format = '0'

# Columnas.
for Columna in ["D","E"]:
    for Celda in Hoja3[Columna]:
        Celda.style = General
        Celda.alignment = Centrar
        Celda.fill = PatternFill(start_color="808080", end_color="808080", fill_type="solid")
        
for Celda in Hoja3["E"]:
    Celda.fill = PatternFill(start_color="FFA500", end_color="FFA500", fill_type="solid")
#.-

# Cambiar nombres de hojas.
Hoja.title = 'Precio Calculado Alto'
Hoja2.title = 'Costo Calculado Bajo'
Hoja3.title = 'Costo Calculado Alto' 

# Guardar el archivo
Libro.save(Ruta)