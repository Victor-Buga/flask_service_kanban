import unittest
import warnings
from unittest.mock import patch
 
from app import app
 
class BaseTestCase(unittest.TestCase):
    """Classe de base : prépare un client de test Flask pour chaque test."""
 
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
 
#/db/stats/describe
 
class TestDescribe(BaseTestCase):
 
    def test_parametre_manquant(self):
        """Sans paramètre 'serie', on doit avoir une erreur 400."""
        response = self.client.get('/db/stats/describe')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('erreur', data)
 
    @patch('app.fetch_series')
    def test_serie_valide(self, mock_fetch):
        """Cas normal : la série existe et contient des valeurs."""
        mock_fetch.return_value = [10, 20, 30, 40, 50]
 
        response = self.client.get('/db/stats/describe?serie=temperature')
 
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['source'], 'mysql')
        resultat = data['resultat']
 
        self.assertEqual(resultat['serie'], 'temperature')
        self.assertEqual(resultat['n'], 5)
        self.assertEqual(resultat['moyenne'], 30.0)
        self.assertEqual(resultat['mediane'], 30.0)
        self.assertEqual(resultat['minimum'], 10.0)
        self.assertEqual(resultat['maximum'], 50.0)
        # écart-type (ddof=1) de [10,20,30,40,50] = 15.8114 (arrondi à 4 décimales)
        self.assertAlmostEqual(resultat['ecart_type'], 15.8114, places=3)
 
        mock_fetch.assert_called_once_with('temperature')
 
    @patch('app.fetch_series')
    def test_serie_inexistante(self, mock_fetch):
        """fetch_series lève ValueError -> 404."""
        mock_fetch.side_effect = ValueError("Aucune donnée trouvée pour la série 'inconnue'")
 
        response = self.client.get('/db/stats/describe?serie=inconnue')
 
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn('erreur', data)
        self.assertIn('inconnue', data['erreur'])
 
    @patch('app.fetch_series')
    def test_erreur_base_de_donnees(self, mock_fetch):
        """Une exception générique (ex: erreur MySQL) -> 500."""
        mock_fetch.side_effect = Exception("Connexion refusée")
 
        response = self.client.get('/db/stats/describe?serie=temperature')
 
        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertEqual(data['erreur'], 'Erreur base de données')
        self.assertIn('Connexion refusée', data['detail'])
 
    @patch('app.fetch_series')
    def test_une_seule_valeur(self, mock_fetch):
        """Avec une seule valeur, std (ddof=1) vaut NaN -> comportement à vérifier.
 
        jsonify échoue normalement sur NaN, donc on s'attend à 200 ou 500
        selon la version de Flask/numpy. Ce test documente le comportement
        actuel plutôt que de l'imposer.
        """
        mock_fetch.return_value = [42.0]
 
        with warnings.catch_warnings():
            # np.std avec ddof=1 sur une seule valeur calcule 0/0 -> NaN,
            # numpy émet un RuntimeWarning attendu, on le masque ici.
            warnings.simplefilter('ignore', category=RuntimeWarning)
            response = self.client.get('/db/stats/describe?serie=unique')
 
        self.assertIn(response.status_code, (200, 500))
  
#/db/stats/correlation
 
class TestCorrelation(BaseTestCase):
 
    def test_parametres_manquants(self):
        """Sans serie_x ni serie_y -> 400."""
        response = self.client.get('/db/stats/correlation')
        self.assertEqual(response.status_code, 400)
 
        response = self.client.get('/db/stats/correlation?serie_x=a')
        self.assertEqual(response.status_code, 400)
 
        response = self.client.get('/db/stats/correlation?serie_y=b')
        self.assertEqual(response.status_code, 400)
 
    @patch('app.fetch_series')
    def test_correlation_parfaite_positive(self, mock_fetch):
        """Deux séries parfaitement corrélées -> r = 1."""
        mock_fetch.side_effect = [
            [1, 2, 3, 4, 5],   # serie_x
            [2, 4, 6, 8, 10],  # serie_y
        ]
 
        response = self.client.get('/db/stats/correlation?serie_x=x&serie_y=y')
 
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        resultat = data['resultat']
 
        self.assertAlmostEqual(resultat['r'], 1.0, places=4)
        self.assertTrue(resultat['significatif'])
        self.assertEqual(data['series']['n_points'], 5)
 
    @patch('app.fetch_series')
    def test_correlation_longueurs_differentes(self, mock_fetch):
        """Si les séries n'ont pas la même longueur, on tronque à la plus courte."""
        mock_fetch.side_effect = [
            [1, 2, 3, 4, 5, 6],  # serie_x (6 valeurs)
            [10, 20, 30],        # serie_y (3 valeurs)
        ]
 
        response = self.client.get('/db/stats/correlation?serie_x=x&serie_y=y')
 
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['series']['n_points'], 3)
 
    @patch('app.fetch_series')
    def test_serie_x_inexistante(self, mock_fetch):
        """fetch_series lève ValueError pour serie_x -> 404."""
        mock_fetch.side_effect = ValueError("Aucune donnée trouvée pour la série 'x'")
 
        response = self.client.get('/db/stats/correlation?serie_x=x&serie_y=y')
 
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn('erreur', data)
 
    @patch('app.fetch_series')
    def test_erreur_base_de_donnees(self, mock_fetch):
        """Exception générique -> 500."""
        mock_fetch.side_effect = Exception("Timeout MySQL")
 
        response = self.client.get('/db/stats/correlation?serie_x=x&serie_y=y')
 
        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertEqual(data['erreur'], 'Erreur base de données')
        self.assertIn('Timeout MySQL', data['detail'])
 
 

class TestAccueil(BaseTestCase):
 
    def test_page_accueil(self):
        """La route '/' doit répondre 200 (nécessite templates/test.html)."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
 
 
if __name__ == '__main__':
    unittest.main()
 