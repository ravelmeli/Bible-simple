"""Transforme une image détourée (PNG transparent) ou une photo sur fond uni en « autocollant » du style 02 :
recadrage, redimensionnement, trous bouchés, liseré blanc régulier. L'ombre est ajoutée par le CSS du gabarit.

PNG déjà détouré (par ex. `npx hyperframes remove-background photo.jpg -o cut.png`) :
    python3 -I make_sticker.py cut.png assets/stickers/objet.png --taille 900 --liseré 12
Photo sur fond studio uni (gris, blanc, noir) : détourage par distance à la couleur du bord :
    python3 -I make_sticker.py photo.jpg assets/stickers/objet.png --fond-uni 24
Planche de contrôle de tout un dossier :
    python3 -I make_sticker.py --planche assets/stickers controle.png

Repères : liseré 12 px pour une photo, 16 px pour un personnage, 14 px pour un petit objet affiché petit
(dans ce cas, --taille proche de la taille à l'écran, 420 à 520, pour que le liseré reste visible).
"""
import argparse
import os
from collections import deque

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


def fill_holes(mask):
    m = Image.fromarray(np.pad(mask.astype(np.uint8) * 255, 1)).copy()
    ImageDraw.floodfill(m, (0, 0), 128)
    return np.array(m)[1:-1, 1:-1] != 128


def largest(mask):
    """Plus grande composante connexe (4-voisinage)."""
    H, W = mask.shape
    lab = np.zeros((H, W), np.int32)
    best, best_n, n = 0, 0, 0
    for y, x in zip(*np.nonzero(mask)):
        if lab[y, x]:
            continue
        n += 1
        lab[y, x] = n
        q, c = deque([(y, x)]), 0
        while q:
            cy, cx = q.popleft()
            c += 1
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ny, nx = cy + dy, cx + dx
                if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and not lab[ny, nx]:
                    lab[ny, nx] = n
                    q.append((ny, nx))
        if c > best:
            best, best_n = c, n
    return lab == best_n


def by_color(src, tol):
    """Détourage d'une photo sur fond uni : écart à la couleur médiane du bord > tol."""
    im = Image.open(src).convert("RGB")
    im.thumbnail((1200, 1200))
    a = np.array(im).astype(np.int32)
    border = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
    bg = np.median(border, axis=0)
    mask = np.sqrt(((a - bg) ** 2).sum(axis=2)) > tol
    mask = np.array(Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3))) > 0
    mask = fill_holes(largest(mask))
    out = im.convert("RGBA")
    out.putalpha(Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8)))
    return out


def sticker(im, size=900, outline=12):
    a = np.array(im)[..., 3]
    ys, xs = np.nonzero(a > 40)
    im = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    im.thumbnail((size, size), Image.LANCZOS)
    pad = outline + 6
    c = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    c.paste(im, (pad, pad), im)
    m = fill_holes(np.array(c.split()[3]) > 90)
    # Liseré rond et régulier : dilatation (filtre max) puis bord légèrement adouci.
    grow = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(2 * outline + 1)).filter(ImageFilter.GaussianBlur(1.2))
    white = Image.new("RGBA", c.size, (255, 255, 255, 255))
    white.putalpha(grow)
    return Image.alpha_composite(white, c)


def planche(dossier, out, cell=320, cols=5):
    names = sorted(f for f in os.listdir(dossier) if f.endswith(".png"))
    rows = (len(names) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell, rows * cell), (233, 237, 241))
    for k, n in enumerate(names):
        s = Image.open(os.path.join(dossier, n))
        s.thumbnail((cell - 20, cell - 20))
        sheet.paste(s, ((k % cols) * cell + (cell - s.width) // 2, (k // cols) * cell + (cell - s.height) // 2), s)
    sheet.save(out)
    print(out, len(names), "autocollants")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("entree")
    ap.add_argument("sortie")
    ap.add_argument("--taille", type=int, default=900)
    ap.add_argument("--liseré", "--lisere", dest="outline", type=int, default=12)
    ap.add_argument("--fond-uni", dest="tol", type=float, default=None, help="tolérance (22 à 28) pour une photo sur fond uni")
    ap.add_argument("--planche", action="store_true", help="entree = dossier d'autocollants, sortie = planche de contrôle")
    a = ap.parse_args()
    if a.planche:
        planche(a.entree, a.sortie)
    else:
        src = by_color(a.entree, a.tol) if a.tol is not None else Image.open(a.entree).convert("RGBA")
        out = sticker(src, a.taille, a.outline)
        os.makedirs(os.path.dirname(os.path.abspath(a.sortie)), exist_ok=True)
        out.save(a.sortie)
        print(a.sortie, out.size)
