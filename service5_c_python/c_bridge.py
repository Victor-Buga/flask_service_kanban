# Ce module charge la bibliotheque compilee lib/stats.so (ou .dll / .dylib selon le systeme), declare la signature de chaque fonction C, puis expose
# des fonctions Python propres qui cachent toute la complexite de ctypes.

import ctypes
import os
import platform

# ─── Chargement de la bibliotheque ──────────────────────────────────────
# Determiner l'extension du fichier compile selon le systeme d'exploitation.
_ext = '.so'
if platform.system() == 'Darwin':        # macOS
    _ext = '.dylib'
elif platform.system() == 'Windows':     # Windows
    _ext = '.dll'

_lib_path = os.path.join(os.path.dirname(__file__), 'lib', f'stats{_ext}')

if not os.path.exists(_lib_path):
    raise FileNotFoundError(
        f'Bibliotheque C introuvable : {_lib_path}\n'
        'Executez ./compile.sh pour compiler src/stats.c'
    )

_lib = ctypes.CDLL(_lib_path)

# ─── Declaration des signatures (types) ─────────────────────────────────
# Type "pointeur vers double", utilise pour passer un tableau a une fonction C.
_DoublePtr = ctypes.POINTER(ctypes.c_double)

# calcul_moyenne(double *tableau, int n) -> double
_lib.calcul_moyenne.argtypes = [_DoublePtr, ctypes.c_int]
_lib.calcul_moyenne.restype = ctypes.c_double

# calcul_variance(double *tableau, int n) -> double
_lib.calcul_variance.argtypes = [_DoublePtr, ctypes.c_int]
_lib.calcul_variance.restype = ctypes.c_double

# calcul_ecart_type(double *tableau, int n) -> double
_lib.calcul_ecart_type.argtypes = [_DoublePtr, ctypes.c_int]
_lib.calcul_ecart_type.restype = ctypes.c_double

# calcul_mediane(double *tableau, int n) -> double
_lib.calcul_mediane.argtypes = [_DoublePtr, ctypes.c_int]
_lib.calcul_mediane.restype = ctypes.c_double

# calcul_min(double *tableau, int n) -> double
_lib.calcul_min.argtypes = [_DoublePtr, ctypes.c_int]
_lib.calcul_min.restype = ctypes.c_double

# calcul_max(double *tableau, int n) -> double
_lib.calcul_max.argtypes = [_DoublePtr, ctypes.c_int]
_lib.calcul_max.restype = ctypes.c_double

# produit_scalaire(double *v1, double *v2, int n) -> double
_lib.produit_scalaire.argtypes = [_DoublePtr, _DoublePtr, ctypes.c_int]
_lib.produit_scalaire.restype = ctypes.c_double


# ─── Fonctions Python propres (wrappers) ────────────────────────────────
def _to_c_array(python_list):
    """Convertit une liste Python en tableau C de doubles.

    Retourne le tableau C alloue et sa longueur. C'est cette etape qui
    permet de passer une liste Python a une fonction C attendant un
    double* : on cree un tableau ctypes contigu en memoire.
    """
    arr = (ctypes.c_double * len(python_list))(*python_list)
    return arr, len(python_list)


def moyenne(valeurs: list[float]) -> float:
    arr, n = _to_c_array(valeurs)
    return round(_lib.calcul_moyenne(arr, n), 6)


def variance(valeurs: list[float]) -> float:
    arr, n = _to_c_array(valeurs)
    return round(_lib.calcul_variance(arr, n), 6)


def ecart_type(valeurs: list[float]) -> float:
    arr, n = _to_c_array(valeurs)
    return round(_lib.calcul_ecart_type(arr, n), 6)


def mediane(valeurs: list[float]) -> float:
    arr, n = _to_c_array(valeurs)
    return round(_lib.calcul_mediane(arr, n), 6)


def minimum(valeurs: list[float]) -> float:
    arr, n = _to_c_array(valeurs)
    return round(_lib.calcul_min(arr, n), 6)


def maximum(valeurs: list[float]) -> float:
    arr, n = _to_c_array(valeurs)
    return round(_lib.calcul_max(arr, n), 6)


def dot_product(v1: list[float], v2: list[float]) -> float:
    if len(v1) != len(v2):
        raise ValueError('Les deux vecteurs doivent avoir la meme longueur')
    a1, n = _to_c_array(v1)
    a2, _ = _to_c_array(v2)
    return round(_lib.produit_scalaire(a1, a2, n), 6)
