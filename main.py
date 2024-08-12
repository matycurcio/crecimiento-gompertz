import numpy as np
import scipy.optimize as opt
import sympy as sp
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from lectura_archivo import crear_ventana


def procesar_datos(dias, alturas):
    # Normalizar fechas y alturas
    fechas_norm = dias / dias.max()
    alturas_norm = alturas / alturas.max()

    # Función de Gompertz con normalización
    def gompertz_norm(t, a, b, c):
        return a * np.exp(-b * np.exp(-c * t))

    # Ajuste de la curva utilizando los datos normalizados
    popt, pcov = opt.curve_fit(gompertz_norm, fechas_norm, alturas_norm, p0=(1, 1, 0.1))

    # Parámetros ajustados
    a, b, c = popt
    print("Parámetros ajustados:")
    print(f"a = {a}, b = {b}, c = {c}")

    # Cálculo de la segunda derivada usando sympy

    # Definir la variable simbólica
    t = sp.symbols('t')

    # Definir la función de Gompertz simbólicamente
    gompertz_sym = a * sp.exp(-b * sp.exp(-c * t))

    # Calcular la segunda derivada
    segunda_derivada_sym = sp.diff(gompertz_sym, t, 2)

    # Convertir la segunda derivada en una función evaluable
    segunda_derivada_func = sp.lambdify(t, segunda_derivada_sym, 'numpy')

    # Evaluar la segunda derivada en un rango de fechas
    fechas_continuas_norm = np.linspace(fechas_norm.min(), fechas_norm.max(), 100)
    segunda_derivada_valores_norm = segunda_derivada_func(fechas_continuas_norm)

    # Desnormalizar las fechas para graficar
    fechas_continuas = fechas_continuas_norm * dias.max()
    segunda_derivada_valores = segunda_derivada_valores_norm * alturas.max()

    # Encontrar el punto mínimo de la segunda derivada
    min_index = np.argmin(segunda_derivada_valores)
    min_fecha = fechas_continuas[min_index]
    min_valor = segunda_derivada_valores[min_index]

    # Graficar los resultados
    alturas_ajustadas_norm = gompertz_norm(fechas_continuas_norm, *popt)
    alturas_ajustadas = alturas_ajustadas_norm * alturas.max()  # Desnormalizar alturas ajustadas

    plt.figure(figsize=(14, 6))

    # Gráfico de la función ajustada
    plt.subplot(1, 2, 1)
    plt.scatter(dias, alturas, label='Datos')
    plt.plot(fechas_continuas, alturas_ajustadas, label='Ajuste Gompertz')
    plt.xlabel('Fechas (días)')
    plt.ylabel('Alturas (cm)')
    plt.legend()
    plt.title('Ajuste de la Curva de Gompertz')

    # Gráfico de la segunda derivada
    plt.subplot(1, 2, 2)
    plt.plot(fechas_continuas, segunda_derivada_valores, label='Segunda Derivada', color='r')
    plt.scatter(min_fecha, min_valor, color='blue', zorder=5)  # Punto mínimo
    plt.annotate(f'Mín:({min_fecha:.2f}, {min_valor:.4f})',
                 xy=(min_fecha, min_valor),
                 xytext=(min_fecha + 20, min_valor + 0.02),
                 arrowprops=dict(arrowstyle='->'),
                 bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white"))
    plt.xlabel('Fechas (días)')
    plt.ylabel('Segunda Derivada')
    plt.legend()
    plt.title('Segunda Derivada de la Curva de Gompertz')

    # Ajustar manualmente los márgenes
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.25)
    plt.show()


# Iniciar la interfaz gráfica y cargar los datos
crear_ventana(procesar_datos)
