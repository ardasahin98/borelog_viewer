"""Draw a boring log with the Boring Log Viewer render API.

Needs Python 3 and the requests package (pip install requests).
Run:  python api_example.py
Writes B-1.png and B-1.svg next to this script.
"""
import requests

API = "https://uclageo.com/boring-log-viewer/api/render"

log = {
    "schema_version": "1.0",
    "units": {"length": "ft", "unit_weight": "pcf"},
    "metadata": {"project": "Example Street Bridge", "boring_name": "B-1", "elevation": 112.5},
    "groundwater": [{"depth": 7.5, "note": "encountered during drilling"}],
    "layers": [
        {"top": 0, "bottom": 4, "description": "Brown, loose, moist, silty SAND (fill)", "uscs": "SM"},
        {"top": 4, "bottom": 12, "description": "Gray, medium dense, wet, poorly graded SAND with silt", "uscs": "SP-SM"},
        {"top": 12, "bottom": 20, "description": "Gray, soft, wet, lean CLAY", "uscs": "CL"},
    ],
    "samples": [
        {"top": 2.5, "bottom": 4, "name": "S-1", "type": "SPT", "blows": [3, 4, 4], "blow_count": 8,
         "specimens": [{"name": "S-1a", "top": 2.5, "bottom": 4, "water_content": 14.2, "fines_content": 31}]},
        {"top": 12.5, "bottom": 14.5, "name": "T-3", "type": "Shelby", "recovery": 1.8,
         "specimens": [{"name": "T-3a", "top": 12.6, "bottom": 13.1, "water_content": 36.5,
                        "liquid_limit": 44, "plastic_limit": 21}]},
    ],
}

for fmt in ("png", "svg"):
    r = requests.post(API, params={"format": fmt}, json=log, timeout=60)
    if not r.ok:
        # On a bad log the API answers 422 with a list of what's wrong, e.g.
        # {"error": "Invalid boring log", "errors": [{"path": "/layers/0/uscs", "message": ...}]}
        print(f"{fmt}: failed ({r.status_code})", r.text)
        continue
    with open(f"B-1.{fmt}", "wb") as f:
        f.write(r.content)
    print(f"wrote B-1.{fmt}")
