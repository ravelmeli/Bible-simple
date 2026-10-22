"""Découpe une planche Nano Banana (éléments isolés sur fond blanc uni) en PNG transparents, un par élément.

    python3 -I decouper_planche.py planche-personnages.png elements/ --noms esther-pied,esther-portrait,mardochee,roi,haman,peuple

Les éléments sont détectés comme composantes connexes de pixels « non blancs » (sur une version réduite pour la
vitesse), triés en lignes puis de gauche à droite, et nommés dans cet ordre. Une planche de contrôle
(<dossier>/_controle.png) permet de vérifier la découpe à l'œil avant de passer à make_sticker.py.
"""
import argparse
import os
from collections import deque

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


def components(mask, min_area):
    H, W = mask.shape
    lab = np.zeros((H, W), np.int32)
    boxes, n = [], 0
    for y, x in zip(*np.nonzero(mask)):
        if lab[y, x]:
            continue
        n += 1
        lab[y, x] = n
        q, area = deque([(y, x)]), 0
        x0, y0, x1, y1 = x, y, x, y
        while q:
            cy, cx = q.popleft()
            area += 1
            x0, y0, x1, y1 = min(x0, cx), min(y0, cy), max(x1, cx), max(y1, cy)
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and not lab[ny, nx]:
                        lab[ny, nx] = n
                        q.append((ny, nx))
        if area >= min_area:
            boxes.append((x0, y0, x1 + 1, y1 + 1))
    return boxes


def fill_holes(mask):
    m = Image.fromarray(np.pad(mask.astype(np.uint8) * 255, 1)).copy()
    ImageDraw.floodfill(m, (0, 0), 128)
    return np.array(m)[1:-1, 1:-1] != 128


def main(src, out_dir, names, tol=28, scale=4):
    os.makedirs(out_dir, exist_ok=True)
    im = Image.open(src).convert("RGB")
    a = np.array(im).astype(np.int32)
    dist = np.sqrt(((255 - a) ** 2).sum(axis=2))          # écart au blanc
    small = Image.fromarray(((dist > tol) * 255).astype(np.uint8)).resize((im.width // scale, im.height // scale), Image.BOX)
    small = small.filter(ImageFilter.MaxFilter(5))            # relie les traits fins d'un même élément
    boxes = components(np.array(small) > 40, min_area=400 // scale)
    # Tri en lignes (centres verticaux proches), puis de gauche à droite.
    boxes.sort(key=lambda b: (b[1] + b[3]) / 2)
    rows, cur = [], []
    for b in boxes:
        if cur and (b[1] + b[3]) / 2 - (cur[-1][1] + cur[-1][3]) / 2 > (b[3] - b[1]) * 0.5:
            rows.append(cur)
            cur = []
        cur.append(b)
    if cur:
        rows.append(cur)
    boxes = [b for r in rows for b in sorted(r)]
    ctrl = im.copy()
    d = ImageDraw.Draw(ctrl)
    for k, (x0, y0, x1, y1) in enumerate(boxes):
        X0, Y0 = max(0, x0 * scale - 8), max(0, y0 * scale - 8)
        X1, Y1 = min(im.width, x1 * scale + 8), min(im.height, y1 * scale + 8)
        crop = a[Y0:Y1, X0:X1]
        m = fill_holes(np.sqrt(((255 - crop) ** 2).sum(axis=2)) > tol)
        alpha = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.7))
        el = Image.fromarray(crop.astype(np.uint8)).convert("RGBA")
        el.putalpha(alpha)
        name = names[k] if k < len(names) else f"element-{k + 1:02d}"
        el.save(os.path.join(out_dir, name + ".png"))
        d.rectangle((X0, Y0, X1, Y1), outline=(248, 88, 48), width=6)
        d.text((X0 + 10, Y0 + 10), f"{k + 1} {name}", fill=(248, 88, 48))
        print(f"{k + 1:2d} {name}: {X1 - X0} x {Y1 - Y0}")
    ctrl.thumbnail((1600, 1600))
    ctrl.save(os.path.join(out_dir, "_controle.png"))
    print(len(boxes), "éléments ; contrôle :", os.path.join(out_dir, "_controle.png"))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("planche")
    ap.add_argument("dossier")
    ap.add_argument("--noms", default="", help="noms dans l'ordre de lecture, séparés par des virgules")
    ap.add_argument("--tolerance", type=float, default=28)
    a = ap.parse_args()
    main(a.planche, a.dossier, [n for n in a.noms.split(",") if n], a.tolerance)
