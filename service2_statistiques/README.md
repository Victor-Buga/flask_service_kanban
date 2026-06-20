### Route 1 — POST /stats/describe
Statistiques descriptives d'une série.
```bash
curl -X POST http://localhost:5002/stats/describe \
  -H 'Content-Type: application/json' \
  -d '{"data": [12.5, 15.3, 8.7, 21.0, 13.2, 9.8, 17.6, 11.4]}'
```

### Route 2 — POST /stats/correlation
Corrélation de Pearson entre deux séries.
```bash
curl -X POST http://localhost:5002/stats/correlation \
  -H 'Content-Type: application/json' \
  -d '{"x": [1,2,3,4,5], "y": [2.1,3.9,6.2,7.8,10.1]}'
```

### Route 3 — POST /stats/test_normalite
Test de normalité (Shapiro-Wilk).
```bash
curl -X POST http://localhost:5002/stats/test_normalite \
  -H 'Content-Type: application/json' \
  -d '{"data": [2.1, 2.3, 1.9, 2.0, 2.2, 2.05, 1.95, 2.15]}'
```

### Route supplémentaire — POST /stats/test_student
Test t de Student entre deux groupes.
```bash
curl -X POST http://localhost:5002/stats/test_student \
  -H 'Content-Type: application/json' \
  -d '{"groupe1": [12,14,13,15,11], "groupe2": [18,20,19,21,17]}'
```