# Imports nécessaires :
# flask
from flask import Flask, request, jsonify
# numpy
import numpy as np
# assets (matrices)
from matrices import (add_matrices, multiply_matrices,
                      transpose_matrix, determinant_matrix,
                      inverse_matrix)
                      
# =======================================================================
# Tester les matrices
Copier coller les instructions suivantes, en un coup, et les faire exécuter sous powershell pour confirmer que le code fonctionne.
# | ------------------------------------------------------------------- |
# add
Invoke-WebRequest -Uri "http://127.0.0.1:5001/matrices/add" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"A": [[1,2],[3,4]], "B": [[5,6],[7,8]]}'
# -----------------------------------------------------------------------
# multiply
Invoke-RestMethod -Uri "http://127.0.0.1:5001/matrices/multiply" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"A": [[1,2],[3,4]], "B": [[5,6],[7,8]]}'
# -----------------------------------------------------------------------
# transpose
Invoke-RestMethod -Uri "http://127.0.0.1:5001/matrices/transpose" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"A": [[1,2],[3,4]]}'
# -----------------------------------------------------------------------
# determinant
Invoke-RestMethod -Uri "http://127.0.0.1:5001/matrices/determinant" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"A": [[1,2],[3,4]]}'
# -----------------------------------------------------------------------
# inverse
Invoke-RestMethod -Uri "http://127.0.0.1:5001/matrices/inverse" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"A": [[1,2],[3,4]]}'
# =======================================================================
# Exemple de requête curl pour tester la multiplication de deux matrices 3×3.
Invoke-RestMethod -Uri "http://127.0.0.1:5001/matrices/multiply" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"A": [[1,2,3],[4,5,6],[7,8,9]], "B": [[9,8,7],[6,5,4],[3,2,1]]'
