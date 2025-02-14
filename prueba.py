# -f programa algo en numpy para multiplicar dos matrices 
import numpy as np

# Definir las matrices
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# Multiplicar las matrices
resultado = np.dot(A, B)

print(resultado)

# -p ahora haz una función para calcular determinantes 
def calcular_determinante(matriz):
    """Calcula el determinante de una matriz cuadrada."""
    return np.linalg.det(matriz)
