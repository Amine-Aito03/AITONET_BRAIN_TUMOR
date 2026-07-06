from pathlib import Path
from datetime import datetime
import tempfile

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle


BLUE_DARK = colors.HexColor("#003B73")
BLUE = colors.HexColor("#005A9C")
ORANGE = colors.HexColor("#F28C28")
LIGHT_BLUE = colors.HexColor("#EAF3FF")
LIGHT_ORANGE = colors.HexColor("#FFF4E6")
GRAY = colors.HexColor("#5F6B7A")


def _save_numpy_image(array, path, cmap="gray"):
    plt.figure(figsize=(4, 4))
    plt.imshow(array, cmap=cmap)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(path, dpi=180, bbox_inches="tight", pad_inches=0)
    plt.close()


def _save_rgb_image(image, path):
    image.save(path)


def _draw_header(c, width, height, assets_dir):
    fst_logo = assets_dir / "logo_fst.jpg"
    aito_logo = assets_dir / "AITOLOGO.png"

    c.setFillColor(BLUE_DARK)
    c.roundRect(1.2 * cm, height - 3.1 * cm, width - 2.4 * cm, 2.1 * cm, 14, fill=1, stroke=0)

    # logos avec fond blanc propre
    c.setFillColor(colors.white)
    c.roundRect(1.45 * cm, height - 2.85 * cm, 3.2 * cm, 1.55 * cm, 8, fill=1, stroke=0)
    c.roundRect(width - 4.6 * cm, height - 2.85 * cm, 3.2 * cm, 1.55 * cm, 8, fill=1, stroke=0)

    if fst_logo.exists():
        c.drawImage(str(fst_logo), 1.6 * cm, height - 2.68 * cm, width=2.9 * cm, height=1.2 * cm, preserveAspectRatio=True, mask="auto")

    if aito_logo.exists():
        c.drawImage(str(aito_logo), width - 4.35 * cm, height - 2.72 * cm, width=2.7 * cm, height=1.25 * cm, preserveAspectRatio=True, mask="auto")

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, height - 1.75 * cm, "AITONET BRAIN TUMOR")

    c.setFont("Helvetica", 9)
    c.drawCentredString(width / 2, height - 2.3 * cm, "Rapport automatique d'analyse IRM cérébrale")


def _draw_footer(c, width):
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 8)
    c.drawCentredString(
        width / 2,
        0.9 * cm,
        "AITONET BRAIN TUMOR — Prototype de recherche | Développé par Amine Ait Ou Aali"
    )


def generate_aitonet_pdf(
    base_dir: Path,
    user_info: dict,
    original_image: Image.Image,
    channels: dict,
    overlay_image,
    result_info: dict | None = None,
):
    reports_dir = base_dir / "reports"
    assets_dir = base_dir / "assets"
    reports_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = reports_dir / f"rapport_aitonet_brain_tumor_{timestamp}.pdf"

    temp_dir = Path(tempfile.mkdtemp())

    original_path = temp_dir / "original.png"
    pm_path = temp_dir / "perona_malik.png"
    low_path = temp_dir / "low_frequency.png"
    energy_path = temp_dir / "directional_energy.png"
    overlay_path = temp_dir / "overlay.png"
    user_photo_path = temp_dir / "user_photo.png"

    if user_info.get("photo_path") is not None:
        try:
            user_photo_img = Image.open(user_info.get("photo_path")).convert("RGB")
            user_photo_img.save(user_photo_path)
        except Exception:
            user_photo_path = None
    else:
        user_photo_path = None

    _save_rgb_image(original_image.resize((420, 420)), original_path)
    _save_numpy_image(channels["perona_malik"], pm_path)
    _save_numpy_image(channels["low_frequency"], low_path)
    _save_numpy_image(channels["directional_energy"], energy_path)
    _save_numpy_image(overlay_image, overlay_path, cmap=None)

    c = canvas.Canvas(str(pdf_path), pagesize=A4)
    width, height = A4

    # ================= PAGE 1 =================
    _draw_header(c, width, height, assets_dir)

    # Bande titre
    c.setFillColor(BLUE_DARK)
    c.roundRect(1.3*cm, height-4.5*cm, width-2.6*cm, 0.9*cm, 8, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(1.8*cm, height-4.2*cm, "1. Fiche d’analyse IRM")

    # Bloc informations
    c.setFillColor(LIGHT_BLUE)
    c.roundRect(1.3*cm, height-13.1*cm, 11.2*cm, 7.9*cm, 16, fill=1, stroke=0)

    c.setFillColor(BLUE_DARK)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1.9*cm, height-6.0*cm, "Informations utilisateur")

    info_lines = [
        ("Nom", user_info.get("nom", "")),
        ("Prénom", user_info.get("prenom", "")),
        ("Âge", str(user_info.get("age", ""))),
        ("Sexe", user_info.get("sexe", "")),
        ("Profil", user_info.get("profil", "")),
        ("Institution", user_info.get("institution", "")),
        ("Pays", user_info.get("pays", "")),
        ("Objectif", user_info.get("objectif", "")),
    ]

    y = height - 7.0*cm
    for key, value in info_lines:
        c.setFillColor(BLUE_DARK)
        c.setFont("Helvetica-Bold", 9.5)
        c.drawString(1.9*cm, y, f"{key}")
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 9.5)
        c.drawString(5.0*cm, y, str(value))
        c.setStrokeColor(colors.HexColor("#D6E4F0"))
        c.line(1.9*cm, y-0.17*cm, 11.7*cm, y-0.17*cm)
        y -= 0.65*cm

    # Bloc photo
    c.setFillColor(colors.white)
    c.roundRect(13.0*cm, height-13.1*cm, 5.3*cm, 7.9*cm, 16, fill=1, stroke=0)

    c.setFillColor(BLUE_DARK)
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(15.65*cm, height-6.0*cm, "Photo utilisateur")

    if user_photo_path is not None:
        c.setStrokeColor(ORANGE)
        c.setLineWidth(2)
        c.roundRect(13.7*cm, height-12.2*cm, 3.9*cm, 5.2*cm, 10, fill=0, stroke=1)
        c.drawImage(
            str(user_photo_path),
            13.85*cm,
            height-12.0*cm,
            width=3.6*cm,
            height=4.8*cm,
            preserveAspectRatio=True,
            mask="auto"
        )
    else:
        c.setFillColor(GRAY)
        c.setFont("Helvetica", 9)
        c.drawCentredString(15.65*cm, height-9.2*cm, "Aucune photo fournie")

    # Résumé analyse
    c.setFillColor(BLUE_DARK)
    c.roundRect(1.3*cm, height-18.2*cm, width-2.6*cm, 4.3*cm, 16, fill=1, stroke=0)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1.9*cm, height-14.8*cm, "2. Résumé de l’analyse")

    if result_info is None:
        result_info = {
            "Mode": "Visualisation AITO-3",
            "Classification": "Non activée dans cette version",
            "Confiance": "Non applicable",
            "Décision": "Prototype de recherche",
        }

    y = height - 15.7*cm
    for key, value in result_info.items():
        c.setFillColor(ORANGE)
        c.setFont("Helvetica-Bold", 9.5)
        c.drawString(1.9*cm, y, f"{key} :")
        c.setFillColor(colors.white)
        c.setFont("Helvetica", 9.5)
        c.drawString(5.6*cm, y, str(value))
        y -= 0.58*cm

    # Bloc IRM analysée
    c.setFillColor(colors.white)
    c.roundRect(1.3*cm, 2.4*cm, width-2.6*cm, 6.0*cm, 16, fill=1, stroke=0)

    c.setFillColor(BLUE_DARK)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1.9*cm, 7.7*cm, "3. Image IRM analysée")

    c.drawImage(
        str(original_path),
        1.9*cm,
        3.0*cm,
        width=5.8*cm,
        height=4.3*cm,
        preserveAspectRatio=True,
        mask="auto"
    )

    c.setFillColor(GRAY)
    c.setFont("Helvetica", 9)
    c.drawString(8.4*cm, 6.7*cm, "Cette image IRM est utilisée pour construire les canaux AITO-3.")
    c.drawString(8.4*cm, 6.2*cm, "Les résultats présentés sont destinés à un usage de recherche.")
    c.drawString(8.4*cm, 5.7*cm, "La classification complète AITO-Net sera activée après connexion du moteur final.")

    c.setFillColor(ORANGE)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(8.4*cm, 4.8*cm, "Avertissement")
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 8.5)
    c.drawString(8.4*cm, 4.35*cm, "Ce rapport ne remplace pas l’avis d’un médecin spécialiste.")

    _draw_footer(c, width)
    c.showPage()

    # ================= PAGE 2 =================
    _draw_header(c, width, height, assets_dir)

    c.setFillColor(BLUE_DARK)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(1.6 * cm, height - 4.0 * cm, "3. Visualisation AITO-3")

    c.setFont("Helvetica", 9)
    c.setFillColor(GRAY)
    c.drawString(
        1.6 * cm,
        height - 4.6 * cm,
        "AITO-3 met en évidence différentes représentations de l’IRM : diffusion, basse fréquence et énergie directionnelle."
    )

    # Layout images
    img_w = 5.2 * cm
    img_h = 5.2 * cm

    positions = [
        (1.6 * cm, height - 10.4 * cm, original_path, "IRM originale"),
        (7.4 * cm, height - 10.4 * cm, pm_path, "Perona-Malik"),
        (13.2 * cm, height - 10.4 * cm, low_path, "Basse fréquence"),
        (4.5 * cm, height - 17.2 * cm, energy_path, "Énergie directionnelle"),
        (10.4 * cm, height - 17.2 * cm, overlay_path, "Contours saillants indicatifs"),
    ]

    for x, y, img_path, title in positions:
        c.setFillColor(colors.white)
        c.roundRect(x - 0.1 * cm, y - 0.4 * cm, img_w + 0.2 * cm, img_h + 0.9 * cm, 10, fill=1, stroke=0)
        c.drawImage(str(img_path), x, y, width=img_w, height=img_h, preserveAspectRatio=True, mask="auto")
        c.setFillColor(BLUE_DARK)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(x + img_w / 2, y - 0.25 * cm, title)

    c.setFillColor(GRAY)
    c.setFont("Helvetica", 8)
    c.drawString(
        1.6 * cm,
        2.5 * cm,
        "Les contours rouges sont des régions saillantes indicatives issues de l’énergie directionnelle."
    )
    c.drawString(
        1.6 * cm,
        2.1 * cm,
        "Ils ne constituent pas une segmentation tumorale certifiée."
    )

    _draw_footer(c, width)
    c.showPage()

    # ================= PAGE 3 =================
    _draw_header(c, width, height, assets_dir)

    c.setFillColor(BLUE_DARK)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(1.6 * cm, height - 4.0 * cm, "4. Signature et traçabilité")

    c.setFillColor(colors.white)
    c.roundRect(1.6 * cm, height - 12.5 * cm, width - 3.2 * cm, 7.4 * cm, 18, fill=1, stroke=0)

    c.setFillColor(BLUE_DARK)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(2.2 * cm, height - 6.0 * cm, "Rapport généré par")

    c.setFont("Helvetica-Bold", 16)
    c.drawString(2.2 * cm, height - 7.0 * cm, "Amine Ait Ou Aali")

    c.setFillColor(GRAY)
    c.setFont("Helvetica", 10)
    c.drawString(2.2 * cm, height - 7.8 * cm, "Master 2 — Mathématiques Appliquées et Épidémiologie")
    c.drawString(2.2 * cm, height - 8.4 * cm, "Faculté des Sciences et Techniques — Université Moulay Ismaïl")
    c.drawString(2.2 * cm, height - 9.3 * cm, "Email : a.aitouaali@edu.umi.ac.ma")
    c.drawString(2.2 * cm, height - 9.9 * cm, "Téléphone : +212 6 27 10 28 54")
    c.drawString(2.2 * cm, height - 10.5 * cm, "LinkedIn : à compléter | ORCID : à compléter | ResearchGate : à compléter")

    c.setFillColor(ORANGE)
    c.setFont("Helvetica-BoldOblique", 17)
    c.drawString(2.2 * cm, height - 11.6 * cm, "Signature : Amine Ait Ou Aali")

    c.setFillColor(GRAY)
    c.setFont("Helvetica", 8)
    c.drawString(
        1.6 * cm,
        2.2 * cm,
        "Ce document est produit automatiquement par la plateforme AITONET BRAIN TUMOR dans un contexte de recherche."
    )

    _draw_footer(c, width)
    c.save()

    return pdf_path
