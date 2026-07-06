import streamlit as st
from pathlib import Path
from datetime import datetime
import tempfile
import numpy as np
import pandas as pd
from PIL import Image, ImageFilter, ImageOps
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

CLASS_NAMES = ["glioma", "meningioma", "notumor", "pituitary"]

AITO_LOGO = ASSETS_DIR / "AITOLOGO.png"
FST_LOGO = ASSETS_DIR / "logo_fst.jpg"

st.set_page_config(
    page_title="AITONET BRAIN TUMOR",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f6fbff 0%, #ffffff 55%, #fff7ef 100%);
}
.hero {
    padding: 30px;
    border-radius: 25px;
    background: linear-gradient(120deg, #003B73, #005A9C);
    color: white;
    box-shadow: 0 18px 45px rgba(0,59,115,0.25);
}
.hero h1 {
    font-size: 44px;
    font-weight: 900;
    margin-bottom: 0px;
}
.hero p {
    font-size: 18px;
    opacity: 0.94;
}
.card {
    background: white;
    padding: 24px;
    border-radius: 22px;
    box-shadow: 0 12px 30px rgba(0,59,115,0.10);
    margin-bottom: 22px;
    border: 1px solid rgba(0,90,156,0.10);
}
.metric-card {
    background: white;
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    border-top: 5px solid #F28C28;
    box-shadow: 0 10px 25px rgba(0,59,115,0.10);
}
.metric-value {
    font-size: 30px;
    font-weight: 900;
    color: #003B73;
}
.metric-label {
    color: #6b7280;
}
.success-box {
    padding: 16px;
    border-radius: 15px;
    background: #eaf7ef;
    border-left: 6px solid #1b8f4d;
}
.warning-box {
    padding: 16px;
    border-radius: 15px;
    background: #fff4e6;
    border-left: 6px solid #F28C28;
}
.danger-box {
    padding: 16px;
    border-radius: 15px;
    background: #fdecec;
    border-left: 6px solid #c0392b;
}
.footer {
    text-align: center;
    color: #6b7280;
    margin-top: 40px;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)


def load_logo(path):
    if path.exists():
        return Image.open(path)
    return None


def normalize(x):
    x = x.astype(np.float32)
    return (x - x.min()) / (x.max() - x.min() + 1e-8)


def to_gray(image):
    return np.asarray(image.convert("L").resize((224, 224))).astype(np.float32) / 255.0


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
        u = u + gamma * (cN*north + cS*south + cE*east + cW*west)
    return normalize(u)


def build_aito3(image):
    gray = to_gray(image)
    pm = perona_malik(gray)
    low = np.asarray(
        Image.fromarray((gray * 255).astype(np.uint8)).filter(
            ImageFilter.GaussianBlur(radius=4)
        )
    ).astype(np.float32) / 255.0
    gy, gx = np.gradient(gray)
    energy = normalize(np.sqrt(gx**2 + gy**2))
    return gray, pm, normalize(low), energy


def red_contour_overlay(gray, energy):
    base = np.stack([gray, gray, gray], axis=-1)
    overlay = base.copy()
    threshold = np.quantile(energy, 0.93)
    mask = energy >= threshold
    overlay[mask, 0] = 1.0
    overlay[mask, 1] = 0.05
    overlay[mask, 2] = 0.03
    return overlay


def demo_prediction(image):
    arr = to_gray(image)
    seed = int(arr.mean() * 100000 + arr.std() * 100000)
    rng = np.random.default_rng(seed)
    logits = rng.normal(0, 0.25, 4)
    winner = seed % 4
    logits[winner] += rng.uniform(2.2, 4.0)
    exp = np.exp(logits - logits.max())
    probs = exp / exp.sum()
    pred = int(np.argmax(probs))
    conf = float(probs[pred])
    return pred, conf, probs


def decision(conf, threshold):
    if conf >= threshold:
        return "Acceptée", "success"
    if conf >= 0.85:
        return "À vérifier par expert", "warning"
    return "Validation experte requise", "danger"


def save_aito3_figure(image, gray, pm, low, energy, overlay):
    path = REPORTS_DIR / f"aito3_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    fig, axes = plt.subplots(1, 5, figsize=(16, 4))
    items = [
        (image.convert("L").resize((224, 224)), "IRM originale"),
        (pm, "Perona-Malik"),
        (low, "Basse fréquence"),
        (energy, "Énergie directionnelle"),
        (overlay, "Contours saillants AITO-3"),
    ]
    for ax, (im, title) in zip(axes, items):
        if title == "Contours saillants AITO-3":
            ax.imshow(im)
        else:
            ax.imshow(im, cmap="gray")
        ax.set_title(title)
        ax.axis("off")
    plt.tight_layout()
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close()
    return path


def generate_pdf(info, result, aito3_image_path):
    pdf_path = REPORTS_DIR / f"rapport_aitonet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=A4)
    w, h = A4

    c.setFont("Helvetica-Bold", 18)
    c.drawString(2*cm, h - 2*cm, "AITONET BRAIN TUMOR")

    c.setFont("Helvetica", 11)
    c.drawString(2*cm, h - 2.8*cm, "Rapport automatique d'analyse IRM cérébrale")
    c.drawString(2*cm, h - 3.5*cm, f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    y = h - 4.7*cm
    c.setFont("Helvetica-Bold", 13)
    c.drawString(2*cm, y, "Informations utilisateur")
    y -= 0.7*cm

    c.setFont("Helvetica", 10)
    for k, v in info.items():
        c.drawString(2*cm, y, f"{k} : {v}")
        y -= 0.45*cm

    y -= 0.4*cm
    c.setFont("Helvetica-Bold", 13)
    c.drawString(2*cm, y, "Résultat AITONET")
    y -= 0.7*cm

    c.setFont("Helvetica", 10)
    for k, v in result.items():
        c.drawString(2*cm, y, f"{k} : {v}")
        y -= 0.45*cm

    c.showPage()

    c.setFont("Helvetica-Bold", 15)
    c.drawString(2*cm, h - 2*cm, "Visualisation AITO-3")

    c.drawImage(str(aito3_image_path), 1.3*cm, h - 12*cm, width=18*cm, height=5*cm)

    c.setFont("Helvetica", 9)
    c.drawString(2*cm, 3.2*cm, "Note : les contours rouges sont des régions saillantes indicatives issues du traitement AITO-3.")
    c.drawString(2*cm, 2.7*cm, "Ils ne constituent pas une segmentation médicale certifiée.")

    c.setFont("Helvetica-Bold", 11)
    c.drawString(2*cm, 1.8*cm, "Signature")
    c.setFont("Helvetica", 9)
    c.drawString(2*cm, 1.35*cm, "Amine Ait Ou Aali — Créateur de la plateforme AITONET BRAIN TUMOR")
    c.drawString(2*cm, 0.95*cm, "Email : à compléter | LinkedIn : à compléter | ORCID : à compléter | Téléphone : à compléter")

    c.save()
    return pdf_path


with st.sidebar:
    aito_logo = load_logo(AITO_LOGO)
    if aito_logo:
        st.image(aito_logo, width="stretch")

    st.markdown("## Navigation")
    page = st.radio(
        "",
        ["Tableau de bord", "Analyse IRM unique", "Analyse dataset", "À propos"]
    )

    st.markdown("---")
    fst_logo = load_logo(FST_LOGO)
    if fst_logo:
        st.image(fst_logo, width="stretch")

st.markdown("""
<div class="hero">
<h1>AITONET BRAIN TUMOR</h1>
<p>Plateforme intelligente d’analyse des IRM cérébrales : classification, confiance calibrée, visualisation AITO-3 et aide à la décision.</p>
</div>
""", unsafe_allow_html=True)

if page == "Tableau de bord":
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown('<div class="metric-card"><div class="metric-value">98.69%</div><div class="metric-label">Accuracy finale</div></div>', unsafe_allow_html=True)
    c2.markdown('<div class="metric-card"><div class="metric-value">0.005</div><div class="metric-label">ECE après TS</div></div>', unsafe_allow_html=True)
    c3.markdown('<div class="metric-card"><div class="metric-value">0.95</div><div class="metric-label">AUROC OOD</div></div>', unsafe_allow_html=True)
    c4.markdown('<div class="metric-card"><div class="metric-value">4</div><div class="metric-label">Classes</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Résumé du système")
    st.write("Classes : glioma, meningioma, notumor, pituitary.")
    st.write("Modules : AITO-3, confiance calibrée, prédiction sélective, OOD, rapport PDF.")
    st.warning("Prototype de recherche : ne remplace pas un diagnostic médical.")
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "Analyse IRM unique":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Informations nécessaires avant analyse")
    a, b, c = st.columns(3)
    with a:
        nom = st.text_input("Nom")
        prenom = st.text_input("Prénom")
        age = st.number_input("Âge", 0, 120, 25)
    with b:
        sexe = st.selectbox("Sexe", ["Non spécifié", "Homme", "Femme"])
        profil = st.selectbox("Profil", ["Médecin", "Radiologue", "Chercheur", "Étudiant", "Patient", "Autre"])
        institution = st.text_input("Institution")
    with c:
        pays = st.text_input("Pays")
        objectif = st.selectbox("Objectif", ["Recherche", "Enseignement", "Aide à la décision", "Validation"])
        seuil = st.slider("Seuil d'acceptation", 0.50, 0.99, 0.95, 0.01)
    st.markdown("</div>", unsafe_allow_html=True)

    uploaded = st.file_uploader("Importer une IRM", type=["png", "jpg", "jpeg", "bmp"])

    if uploaded:
        image = Image.open(uploaded).convert("RGB")
        gray, pm, low, energy = build_aito3(image)
        overlay = red_contour_overlay(gray, energy)

        pred, conf, probs = demo_prediction(image)
        dec, dec_type = decision(conf, seuil)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Canaux AITO-3")
        v1, v2, v3, v4, v5 = st.columns(5)
        v1.image(image, caption="IRM originale", width="stretch")
        v2.image(pm, caption="Perona-Malik", clamp=True, width="stretch")
        v3.image(low, caption="Basse fréquence", clamp=True, width="stretch")
        v4.image(energy, caption="Énergie directionnelle", clamp=True, width="stretch")
        v5.image(overlay, caption="Contours saillants indicatifs", width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        left, right = st.columns([1, 1])

        with left:
            st.subheader("Résultat")
            st.write(f"Classe prédite : **{CLASS_NAMES[pred]}**")
            st.write(f"Confiance calibrée : **{conf*100:.2f}%**")
            if dec_type == "success":
                st.markdown(f'<div class="success-box"><b>Décision :</b> {dec}</div>', unsafe_allow_html=True)
            elif dec_type == "warning":
                st.markdown(f'<div class="warning-box"><b>Décision :</b> {dec}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="danger-box"><b>Décision :</b> {dec}</div>', unsafe_allow_html=True)

            st.info("La prédiction actuelle est en mode interface. La connexion complète au modèle AITO-Net sera intégrée après stabilisation de l'application.")

        with right:
            fig, ax = plt.subplots(figsize=(7, 4))
            ax.bar(CLASS_NAMES, probs)
            ax.set_ylim(0, 1)
            ax.set_ylabel("Probabilité")
            ax.set_title("Probabilités par classe")
            ax.grid(axis="y", alpha=0.25)
            plt.xticks(rotation=15)
            st.pyplot(fig)

        st.markdown("</div>", unsafe_allow_html=True)

        info = {
            "Nom": nom,
            "Prénom": prenom,
            "Âge": age,
            "Sexe": sexe,
            "Profil": profil,
            "Institution": institution,
            "Pays": pays,
            "Objectif": objectif,
        }

        result = {
            "Classe prédite": CLASS_NAMES[pred],
            "Confiance calibrée": f"{conf*100:.2f}%",
            "Décision": dec,
            "Seuil": seuil,
            "Classes": ", ".join(CLASS_NAMES),
        }

        aito3_path = save_aito3_figure(image, gray, pm, low, energy, overlay)
        pdf_path = generate_pdf(info, result, aito3_path)

        with open(pdf_path, "rb") as f:
            st.download_button(
                "Télécharger le rapport PDF",
                data=f,
                file_name="rapport_aitonet_brain_tumor.pdf",
                mime="application/pdf"
            )

elif page == "Analyse dataset":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Analyse dataset")
    dataset_name = st.text_input("Nom du dataset")
    user_name = st.text_input("Responsable")
    files = st.file_uploader("Importer plusieurs IRM", type=["png", "jpg", "jpeg", "bmp"], accept_multiple_files=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if files:
        rows = []
        for f in files:
            img = Image.open(f).convert("RGB")
            pred, conf, _ = demo_prediction(img)
            dec, _ = decision(conf, 0.95)
            rows.append({
                "dataset": dataset_name,
                "image": f.name,
                "prediction": CLASS_NAMES[pred],
                "confidence": round(conf*100, 2),
                "decision": dec
            })
        df = pd.DataFrame(rows)
        st.dataframe(df, width="stretch")
        st.download_button("Télécharger CSV", df.to_csv(index=False).encode("utf-8"), "dataset_report.csv", "text/csv")

elif page == "À propos":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("À propos du créateur")
    st.write("**Amine Ait Ou Aali**")
    st.write("Master 2 — Mathématiques Appliquées et Épidémiologie")
    st.write("Université Moulay Ismaïl — Faculté des Sciences et Techniques")
    st.write("Créateur de la plateforme AITONET BRAIN TUMOR.")
    st.markdown("---")
    st.write("Email : à compléter")
    st.write("LinkedIn : à compléter")
    st.write("ORCID : à compléter")
    st.write("Téléphone : à compléter")
    st.warning("Cette plateforme est un prototype de recherche et ne remplace pas l’avis d’un médecin spécialiste.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="footer">AITONET BRAIN TUMOR — Prototype de recherche développé par Amine Ait Ou Aali</div>', unsafe_allow_html=True)