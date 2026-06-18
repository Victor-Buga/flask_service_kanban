"""
test_service1.py - Tests unitaires Service 1
  - Niveau 1 : logique (matrices.py), sans serveur
  - Niveau 2 : intégration HTTP (app.py), serveur requis sur localhost:5001
"""
import unittest
import numpy as np
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

from matrices import (f_add_matrices, f_multiply_matrices,
                      f_transpose_matrices, f_determinant_matrices,
                      f_inverse_matrices)

BASE_URL = "http://localhost:5001"

# ── NIVEAU 1 : Logique ────────────────────────────────────────

class TestLogique(unittest.TestCase):

    def test_addition(self):
        A, B = np.array([[1,2],[3,4]], dtype=float), np.array([[5,6],[7,8]], dtype=float)
        self.assertEqual(f_add_matrices(A, B), [[6.0,8.0],[10.0,12.0]])

    def test_addition_nulle(self):
        A = np.array([[1,2],[3,4]], dtype=float)
        self.assertEqual(f_add_matrices(A, np.zeros((2,2))), [[1.0,2.0],[3.0,4.0]])

    def test_multiplication(self):
        A, B = np.array([[1,2],[3,4]], dtype=float), np.array([[5,6],[7,8]], dtype=float)
        self.assertEqual(f_multiply_matrices(A, B), [[19.0,22.0],[43.0,50.0]])

    def test_multiplication_identite(self):
        A = np.array([[3,7],[1,5]], dtype=float)
        self.assertEqual(f_multiply_matrices(A, np.eye(2)), [[3.0,7.0],[1.0,5.0]])

    def test_transposition(self):
        A = np.array([[1,2,3],[4,5,6]], dtype=float)
        self.assertEqual(f_transpose_matrices(A), [[1.0,4.0],[2.0,5.0],[3.0,6.0]])

    def test_determinant(self):
        self.assertAlmostEqual(f_determinant_matrices(np.array([[3,8],[4,6]], dtype=float)), -14.0, places=5)

    def test_determinant_singuliere(self):
        self.assertAlmostEqual(f_determinant_matrices(np.array([[1,2],[2,4]], dtype=float)), 0.0, places=5)

    def test_inverse(self):
        A = np.array([[4,7],[2,6]], dtype=float)
        result = f_inverse_matrices(A)
        expected = np.linalg.inv(A).tolist()
        for i in range(2):
            for j in range(2):
                self.assertAlmostEqual(result[i][j], expected[i][j], places=5)

# ── NIVEAU 2 : Intégration HTTP ───────────────────────────────────

@unittest.skipUnless(REQUESTS_AVAILABLE, "requests non installé")
class TestHTTP(unittest.TestCase):

    def post(self, route, body):
        return requests.post(f"{BASE_URL}{route}", json=body)

    def test_add_ok(self):
        r = self.post("/matrices/add", {"A": [[1,2],[3,4]], "B": [[5,6],[7,8]]})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['resultat'], [[6.0,8.0],[10.0,12.0]])

    def test_add_dimensions_incompatibles(self):
        r = self.post("/matrices/add", {"A": [[1,2]], "B": [[1,2],[3,4]]})
        self.assertEqual(r.status_code, 400)

    def test_multiply_ok(self):
        r = self.post("/matrices/multiply", {"A": [[1,2],[3,4]], "B": [[5,6],[7,8]]})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['resultat'], [[19.0,22.0],[43.0,50.0]])

    def test_multiply_incompatible(self):
        r = self.post("/matrices/multiply", {"A": [[1,2,3]], "B": [[1,2],[3,4]]})
        self.assertEqual(r.status_code, 400)

    def test_transpose_ok(self):
        r = self.post("/matrices/transpose", {"A": [[1,2,3],[4,5,6]]})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['resultat'], [[1.0,4.0],[2.0,5.0],[3.0,6.0]])

    def test_determinant_ok(self):
        r = self.post("/matrices/determinant", {"A": [[3,8],[4,6]]})
        self.assertEqual(r.status_code, 200)
        self.assertAlmostEqual(r.json()['resultat'], -14.0, places=4)

    def test_determinant_non_carree(self):
        r = self.post("/matrices/determinant", {"A": [[1,2,3],[4,5,6]]})
        self.assertEqual(r.status_code, 400)

    def test_inverse_ok(self):
        r = self.post("/matrices/inverse", {"A": [[4,7],[2,6]]})
        self.assertEqual(r.status_code, 200)

    def test_inverse_singuliere(self):
        r = self.post("/matrices/inverse", {"A": [[1,2],[2,4]]})
        self.assertEqual(r.status_code, 400)
        self.assertIn('singuliere', r.json()['erreur'])

    def test_inverse_non_carree(self):
        r = self.post("/matrices/inverse", {"A": [[1,2,3],[4,5,6]]})
        self.assertEqual(r.status_code, 400)


if __name__ == '__main__':
    unittest.main(verbosity=2)
