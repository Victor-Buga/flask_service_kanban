"""
    -! matrices.py - Fonctions de calcul matriciel.
    -? Utilisé par app.py
    -> L'objectif est d'expliciter ce que fait le code par le nom des fonctions.
"""
import numpy as np


def f_add_matrices(A: np.ndarray, B: np.ndarray) -> list:
    """Additionne deux matrices NumPy et retourne une liste Python."""
    return (A + B).tolist()


def f_multiply_matrices(A: np.ndarray, B: np.ndarray) -> list:
    """Multiplie deux matrices NumPy (produit matriciel) et retourne une liste Python."""
    return np.dot(A, B).tolist()


def f_transpose_matrices(A: np.ndarray) -> list:
    """Transpose une matrice NumPy et retourne une liste Python."""
    return A.T.tolist()


def f_determinant_matrices(A: np.ndarray) -> float:
    """Calcule le déterminant d'une matrice carrée NumPy."""
    return float(np.linalg.det(A))


def f_inverse_matrices(A: np.ndarray) -> list:
    """Calcule l'inverse d'une matrice carrée NumPy et retourne une liste Python."""
    return np.linalg.inv(A).tolist()
