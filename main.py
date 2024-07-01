import numpy as np
import scipy.optimize as opt
import sympy as sp
import matplotlib.pyplot as plt

# Datos de ejemplo
fechas = np.array([20, 30, 86, 90, 93, 104, 107, 112, 114, 120, 125, 128, 132, 135, 139, 142, 147, 154, 156, 163])
alturas = np.array([5, 7, 32, 37, 39, 64, 71, 78, 79, 80, 86, 88, 88, 92, 92, 92, 92, 92, 92, 92])


# Función de Gompertz
def gompertz(t, a, b, c):
    return a * np.exp(-b * np.exp(-c * t))

# Ajuste de la curva
popt, _ = opt.curve_fit(gompertz, fechas, alturas, p0=(alturas.max(), 1, 0.1))

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
fechas_continuas = np.linspace(fechas.min(), fechas.max(), 100)
segunda_derivada_valores = segunda_derivada_func(fechas_continuas)

# Graficar los resultados
alturas_ajustadas = gompertz(fechas_continuas, *popt)

plt.figure(figsize=(10, 5))

# Gráfico de la función ajustada
plt.subplot(1, 2, 1)
plt.scatter(fechas, alturas, label='Datos')
plt.plot(fechas_continuas, alturas_ajustadas, label='Ajuste Gompertz')
plt.xlabel('Fechas (días)')
plt.ylabel('Alturas (cm)')
plt.legend()
plt.title('Ajuste de la Curva de Gompertz')

# Gráfico de la segunda derivada
plt.subplot(1, 2, 2)
plt.plot(fechas_continuas, segunda_derivada_valores, label='Segunda Derivada', color='r')
plt.xlabel('Fechas (días)')
plt.ylabel('Segunda Derivada')
plt.legend()
plt.title('Segunda Derivada de la Curva de Gompertz')

plt.tight_layout()
plt.show()
