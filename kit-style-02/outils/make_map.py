"""Construit assets/map.json pour `map_svg()` du moteur : fond Natural Earth (domaine public), zone tracée à la main,
N points semés dans la zone (triés depuis un lieu d'origine), lieux nommés.

    python3 -I make_map.py carte.json assets/map.json

carte.json (exemple : empire perse d'Esther, voir exemple-esther/carte-esther.json) :
{
  "lon": [18, 76], "lat": [8, 46],       fenêtre affichée
  "largeur": 940, "etirement": 1.15,     largeur du SVG et étirement vertical léger
  "zone": [[25.5, 41.8], [29.0, 41.4], ...],   polygone lon/lat (facultatif) — à annoncer « tracé schématique »
  "points": 127, "graine": 127, "ecart": 22,   nombre de points, graine aléatoire, écart minimal en px
  "origine": [48.25, 32.19],             les points apparaissent depuis ce lieu
  "lieux": {"Suse": [48.25, 32.19], "Jérusalem": [35.22, 31.78]}
}
Le fichier Natural Earth ne_50m_land.geojson est téléchargé une fois dans le dossier de ce script.
"""
import json
import os
import random
import sys
import urllib.request

NE = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_land.geojson"
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ne_50m_land.geojson")


def main(cfg_path, out):
    cfg = json.load(open(cfg_path))
    if not os.path.exists(CACHE):
        urllib.request.urlretrieve(NE, CACHE)
    g = json.load(open(CACHE))
    (LON0, LON1), (LAT0, LAT1) = cfg["lon"], cfg["lat"]
    MW = cfg.get("largeur", 940)
    MH = round(MW * (LAT1 - LAT0) / (LON1 - LON0) * cfg.get("etirement", 1.15))

    def P(lon, lat):
        return (lon - LON0) / (LON1 - LON0) * MW, (LAT1 - lat) / (LAT1 - LAT0) * MH

    paths = []
    for f in g["features"]:
        geom = f["geometry"]
        polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
        for poly in polys:
            ring = poly[0]
            if not any(LON0 - 8 < x < LON1 + 8 and LAT0 - 8 < y < LAT1 + 8 for x, y in ring):
                continue
            paths.append("M" + " L".join(f"{P(x, y)[0]:.1f},{P(x, y)[1]:.1f}" for x, y in ring[::2]) + "Z")

    zone, pts = None, []
    if cfg.get("zone"):
        poly = [P(x, y) for x, y in cfg["zone"]]
        zone = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in poly) + "Z"

        def inside(x, y):
            c = False
            for i in range(len(poly)):
                (x1, y1), (x2, y2) = poly[i], poly[i - 1]
                if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
                    c = not c
            return c

        random.seed(cfg.get("graine", 1))
        xs, ys = [p[0] for p in poly], [p[1] for p in poly]
        gap = cfg.get("ecart", 22)
        tries = 0
        while len(pts) < cfg.get("points", 0) and tries < 200000:
            tries += 1
            x, y = random.uniform(min(xs), max(xs)), random.uniform(min(ys), max(ys))
            if inside(x, y) and all((x - a) ** 2 + (y - b) ** 2 > gap ** 2 for a, b in pts):
                pts.append((x, y))
        if len(pts) < cfg.get("points", 0):
            print(f"attention : seulement {len(pts)} points placés, réduire « ecart »")
        if cfg.get("origine"):
            o = P(*cfg["origine"])
            pts.sort(key=lambda p: (p[0] - o[0]) ** 2 + (p[1] - o[1]) ** 2)
    places = {n: P(*ll) for n, ll in cfg.get("lieux", {}).items()}
    json.dump({"w": MW, "h": MH, "land": paths, "empire": zone, "points": pts, "places": places}, open(out, "w"))
    print(f"{out} : {MW} x {MH}, {len(paths)} terres, {len(pts)} points, {len(places)} lieux")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
