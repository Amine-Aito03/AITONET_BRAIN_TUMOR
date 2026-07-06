import numpy as np
from PIL import Image, ImageFilter


def normalize(x):
    x = x.astype(np.float32)
    return (x - x.min()) / (x.max() - x.min() + 1e-8)


def to_gray(image: Image.Image):
    return np.asarray(
        image.convert("L").resize((224, 224))
    ).astype(np.float32) / 255.0


def perona_malik(img, n_iter=12, kappa=0.12, gamma=0.18):
    u = img.copy().astype(np.float32)

    for _ in range(n_iter):
        north = np.roll(u, -1, axis=0) - u
        south = np.roll(u, 1, axis=0) - u
        east = np.roll(u, -1, axis=1) - u
        west = np.roll(u, 1, axis=1) - u

        cN = np.exp(-(north / kappa) ** 2)
        cS = np.exp(-(south / kappa) ** 2)
        cE = np.exp(-(east / kappa) ** 2)
        cW = np.exp(-(west / kappa) ** 2)

        u = u + gamma * (cN * north + cS * south + cE * east + cW * west)

    return normalize(u)


def build_aito3(image: Image.Image):
    gray = to_gray(image)
    pm = perona_malik(gray)

    low = Image.fromarray((gray * 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(radius=4)
    )
    low = np.asarray(low).astype(np.float32) / 255.0

    gy, gx = np.gradient(pm)
    energy = normalize(np.sqrt(gx**2 + gy**2))

    return {
        "original": gray,
        "perona_malik": pm,
        "low_frequency": normalize(low),
        "directional_energy": energy,
    }


def red_contour_overlay(gray, energy, quantile=0.93):
    base = np.stack([gray, gray, gray], axis=-1)
    overlay = base.copy()

    threshold = np.quantile(energy, quantile)
    mask = energy >= threshold

    overlay[mask, 0] = 1.0
    overlay[mask, 1] = 0.03
    overlay[mask, 2] = 0.02

    return overlay
