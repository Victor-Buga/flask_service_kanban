"""
Test unitaire client du Service 2
"""

import unittest
import requests

BASE_URL = "http://localhost:5002"


def post(route, payload):
    """Envoie une requête POST JSON au service et renvoie la réponse."""
    return requests.post(f"{BASE_URL}{route}", json=payload)


class TestDescribe(unittest.TestCase):
    def test_valeurs_connues(self):
        # Sur [1,2,3,4,5] : moyenne = 3, ecart_type (ddof=1) = 1.5811
        reponse = post("/stats/describe", {"data": [1, 2, 3, 4, 5]})
        self.assertEqual(reponse.status_code, 200)
        res = reponse.json()["resultat"]
        self.assertEqual(res["n"], 5)
        self.assertAlmostEqual(res["moyenne"], 3.0)
        self.assertAlmostEqual(res["ecart_type"], 1.5811, places=4)

    def test_cle_manquante(self):
        reponse = post("/stats/describe", {"valeurs": [1, 2, 3]})
        self.assertEqual(reponse.status_code, 400)


class TestCorrelation(unittest.TestCase):
    def test_correlation_forte(self):
        reponse = post("/stats/correlation", {"x": [1, 2, 3, 4, 5], "y": [2, 4, 6, 8, 10]})
        self.assertEqual(reponse.status_code, 200)
        res = reponse.json()["resultat"]
        self.assertAlmostEqual(res["r"], 1.0, places=4)
        self.assertEqual(res["interpretation"], "forte")

    def test_longueurs_differentes(self):
        reponse = post("/stats/correlation", {"x": [1, 2, 3], "y": [1, 2]})
        self.assertEqual(reponse.status_code, 400)


class TestNormalite(unittest.TestCase):
    def test_structure(self):
        reponse = post("/stats/test_normalite", {"data": [2.1, 2.3, 1.9, 2.0, 2.2, 2.05, 1.95, 2.15]})
        self.assertEqual(reponse.status_code, 200)
        res = reponse.json()["resultat"]
        self.assertIn("p_value", res)
        self.assertIsInstance(res["est_normale"], bool)


class TestStudent(unittest.TestCase):
    def test_difference_significative(self):
        reponse = post("/stats/test_student", {"groupe1": [1, 2, 3, 4, 5], "groupe2": [6, 7, 8, 9, 10]})
        self.assertEqual(reponse.status_code, 200)
        res = reponse.json()["resultat"]
        self.assertTrue(res["difference_significative"])


if __name__ == "__main__":
    unittest.main()