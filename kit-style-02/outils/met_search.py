"""Recherche de photos d'objets en domaine public (CC0) dans l'API Open Access du Metropolitan Museum of Art.

Chercher (affiche les candidats et les enregistre dans candidats.json) :
    python3 -I met_search.py chercher "Achaemenid gold" "Persepolis relief" --max 6
Télécharger des objets choisis (image pleine résolution + brouillon de crédits) :
    python3 -I met_search.py telecharger 324433 324025 --dossier sources/

L'ancienne route /v1/search est retirée (HTTP 410) : on utilise /v1.1/search, puis /v1/objects/{id}.
La licence est revérifiée objet par objet (isPublicDomain) avant tout téléchargement.
"""
import argparse
import json
import os
import urllib.error
import urllib.parse
import urllib.request

API = "https://collectionapi.metmuseum.org/public/collection"


def get(url, raw=False):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.read() if raw else json.load(r)
    except urllib.error.HTTPError:
        return None


def chercher(queries, maxi):
    seen, keep = set(), {}
    for q in queries:
        res = get(f"{API}/v1.1/search?q={urllib.parse.quote(q)}&hasImages=true&isPublicDomain=true&limit=25") or {}
        print(f"== {q} : {res.get('total')} résultats")
        n = 0
        for i in res.get("objectIDs") or []:
            if i in seen:
                continue
            seen.add(i)
            o = get(f"{API}/v1/objects/{i}")
            if o and o.get("isPublicDomain") and o.get("primaryImage"):
                keep[i] = {k: o.get(k) for k in ("title", "culture", "objectDate", "medium", "primaryImage", "primaryImageSmall",
                                                 "objectURL", "creditLine")}
                print(f"   {i} | {o.get('title', '')[:60]} | {o.get('culture', '')[:22]} | {o.get('objectDate', '')[:24]}")
                print(f"        aperçu : {o.get('primaryImageSmall')}")
                n += 1
            if n >= maxi:
                break
    json.dump(keep, open("candidats.json", "w"), ensure_ascii=False, indent=1)
    print(f"{len(keep)} candidats enregistrés dans candidats.json")


def telecharger(ids, dossier):
    os.makedirs(dossier, exist_ok=True)
    lignes = []
    for i in ids:
        o = get(f"{API}/v1/objects/{i}")
        if not o or not o.get("isPublicDomain") or not o.get("primaryImage"):
            print(f"{i} : refusé (pas en domaine public ou pas d'image)")
            continue
        data = get(o["primaryImage"], raw=True)
        path = os.path.join(dossier, f"met-{i}.jpg")
        open(path, "wb").write(data)
        print(f"{i} : {path} ({len(data) // 1024} Ko)")
        lignes.append(f"- `met-{i}` — « {o.get('title')} », {o.get('culture') or o.get('artistDisplayName') or ''}, {o.get('objectDate')} — "
                      f"{o.get('objectURL')} — {o.get('creditLine')} — Public Domain (CC0, Met Open Access)")
    with open(os.path.join(dossier, "credits-brouillon.md"), "a") as f:
        f.write("\n".join(lignes) + "\n")
    print("crédits ajoutés à", os.path.join(dossier, "credits-brouillon.md"))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("chercher")
    a.add_argument("requetes", nargs="+")
    a.add_argument("--max", type=int, default=6)
    b = sub.add_parser("telecharger")
    b.add_argument("ids", nargs="+", type=int)
    b.add_argument("--dossier", default="sources")
    args = ap.parse_args()
    if args.cmd == "chercher":
        chercher(args.requetes, args.max)
    else:
        telecharger(args.ids, args.dossier)
