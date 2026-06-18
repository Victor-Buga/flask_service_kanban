import requests
import time

while True:
    r1 = requests.get(
        "http://127.0.0.1:5003/db/stats/describe",
        params={"serie": "serie_A"}
    )

    r2 = requests.get(
        "http://127.0.0.1:5003/db/stats/correlation",
        params={"serie_x":"serie_A","serie_y":"serie_B"}
    )

    print(r1.json())
    print(r2.json())

    time.sleep(2)