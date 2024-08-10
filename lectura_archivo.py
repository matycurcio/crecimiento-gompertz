import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk


def cargar_datos_excel(callback):
    # Abrir un cuadro de diálogo para seleccionar el archivo Excel
    archivo_excel = filedialog.askopenfilename(title="Seleccionar archivo Excel",
                                               filetypes=[("Excel files", "*.xlsx *.xls")])

    if archivo_excel:
        try:
            df = pd.read_excel(archivo_excel)
            # Suponiendo que las columnas se llaman 'Fechas' y 'Alturas'
            fechas = df['Dias'].values
            alturas = df['Altura'].values

            # Llamar al callback con los datos cargados
            callback(fechas, alturas)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {e}")
    else:
        print("No se seleccionó ningún archivo.")


def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')


def crear_ventana(callback):
    root = tk.Tk()
    root.title("Cargar Datos de Excel")
    root.configure(bg='white')  # Fondo blanco para la ventana

    # Centrar la ventana
    centrar_ventana(root, 400, 200)

    # Crear un texto amigable y colorido
    label = tk.Label(root,
                     text="Ingrese su excel para aproximar la curva.\nRecuerde que las columnas de los días y "
                          "alturas\nse deben llamar 'Dias' y 'Altura'",
                     font=("Montserrat", 12), fg="black", bg="white")
    label.pack(pady=20)

    # Estilo personalizado para el botón redondeado
    style = ttk.Style()
    style.configure('Rounded.TButton', background='green', foreground='black', font=('Arial', 10), borderwidth=1,
                    focusthickness=3, focuscolor='green')
    style.map('Rounded.TButton', background=[('active', 'light green')])

    # Crear un botón redondeado para cargar el archivo Excel
    btn_cargar = ttk.Button(root, text="Cargar Excel", style='Rounded.TButton',
                            command=lambda: cargar_datos_excel(callback))
    btn_cargar.pack(pady=20)

    root.mainloop()
