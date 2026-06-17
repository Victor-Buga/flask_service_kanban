from flask import Flask, request, jsonify
import numpy as np
from matrices import (f_add_matrices, f_multiply_matrices,
                      f_transpose_matrices, f_determinant_matrices,
                      f_inverse_matrices)

# Création de l'application Flask
app = Flask(__name__)


def parse_matrix(data, key):
    """
    Extrait et convertit une matrice depuis le JSON reçu.
    - data : dictionnaire JSON de la requête
    - key  : clé à lire ('A' ou 'B')
    Retourne un tableau NumPy de flottants, ou lève ValueError si invalide.
    """
    try:
        return np.array(data[key], dtype=float)
    except (KeyError, ValueError) as e:
        raise ValueError(f"Matrice '{key}' invalide : {e}")


# ── Route 1 : Addition ────────────────────────────────────────────────────────
# Attend un JSON { "A": [...], "B": [...] } avec deux matrices de mêmes dimensions
@app.route('/matrices/add', methods=['POST'])
def add_matrices():
    data = request.get_json()           # Lecture du corps JSON
    try:
        A = parse_matrix(data, 'A')
        B = parse_matrix(data, 'B')
        if A.shape != B.shape:          # Vérification : dimensions identiques
            return jsonify({'erreur': 'Dimensions incompatibles'}), 400
        result = f_add_matrices(A, B)
        return jsonify({'operation': 'addition', 'resultat': result})
    except (ValueError, TypeError) as e:
        return jsonify({'erreur': str(e)}), 400


# ── Route 2 : Multiplication ──────────────────────────────────────────────────
# Règle : nb colonnes de A doit égaler nb lignes de B
@app.route('/matrices/multiply', methods=['POST'])
def multiply_matrices():
    data = request.get_json()
    try:
        A = parse_matrix(data, 'A')
        B = parse_matrix(data, 'B')
        if A.shape[1] != B.shape[0]:    # Vérification de compatibilité
            return jsonify({'erreur': 'Colonnes(A) doit egaler Lignes(B)'}), 400
        result = f_multiply_matrices(A, B)
        return jsonify({'operation': 'multiplication', 'resultat': result})
    except (ValueError, TypeError) as e:
        return jsonify({'erreur': str(e)}), 400


# ── Route 3 : Transposition ───────────────────────────────────────────────────
# Retourne la matrice avec lignes et colonnes échangées (pas de contrainte de forme)
@app.route('/matrices/transpose', methods=['POST'])
def transpose_matrix():
    data = request.get_json()
    try:
        A = parse_matrix(data, 'A')
        result = f_transpose_matrices(A)
        return jsonify({'operation': 'transposee', 'resultat': result})
    except (ValueError, TypeError) as e:
        return jsonify({'erreur': str(e)}), 400


# ── Route 4 : Déterminant ─────────────────────────────────────────────────────
# Le déterminant n'existe que pour les matrices carrées (n×n)
@app.route('/matrices/determinant', methods=['POST'])
def determinant_matrix():
    data = request.get_json()
    try:
        A = parse_matrix(data, 'A')
        if A.shape[0] != A.shape[1]:    # Vérification : matrice carrée
            return jsonify({'erreur': 'La matrice doit etre carree'}), 400
        det = f_determinant_matrices(A)
        return jsonify({'operation': 'determinant', 'resultat': round(det, 6)})
    except (ValueError, TypeError) as e:
        return jsonify({'erreur': str(e)}), 400


# ── Route 5 : Inverse ─────────────────────────────────────────────────────────
# Une matrice est inversible si elle est carrée ET son déterminant est non nul
@app.route('/matrices/inverse', methods=['POST'])
def inverse_matrix():
    data = request.get_json()
    try:
        A = parse_matrix(data, 'A')
        if A.shape[0] != A.shape[1]:    # Vérification : matrice carrée
            return jsonify({'erreur': 'La matrice doit etre carree'}), 400
        det = np.linalg.det(A)
        if abs(det) < 1e-10:            # Déterminant +- 0 => matrice singulière
            return jsonify({'erreur': 'Matrice singuliere, non inversible'}), 400
        result = f_inverse_matrices(A)
        return jsonify({'operation': 'inverse', 'resultat': result})
    except (ValueError, TypeError) as e:
        return jsonify({'erreur': str(e)}), 400


# Lancement du serveur en mode debug sur le port 5001
if __name__ == '__main__':
    app.run(debug=True, port=5001)
