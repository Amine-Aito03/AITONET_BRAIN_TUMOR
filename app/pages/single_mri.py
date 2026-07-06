import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt

from app.utils.aito3 import build_aito3, red_contour_overlay
from app.utils.pdf_report import generate_aitonet_pdf


def render_single_mri():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Informations avant analyse</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        nom = st.text_input("Nom")
        prenom = st.text_input("Prénom")
        age = st.number_input("Âge", min_value=0, max_value=120, value=25)

    with c2:
        sexe = st.selectbox("Sexe", ["Non spécifié", "Homme", "Femme"])
        profil = st.selectbox("Profil", ["Médecin", "Radiologue", "Chercheur", "Étudiant", "Patient", "Autre"])
        institution = st.text_input("Institution")

    with c3:
        pays = st.text_input("Pays")
        objectif = st.selectbox("Objectif", ["Recherche", "Enseignement", "Aide à la décision", "Validation"])
        seuil = st.slider("Seuil de confiance", 0.50, 0.99, 0.95, 0.01)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Photo utilisateur / patient</div>', unsafe_allow_html=True)

    photo_mode = st.radio(
        "Méthode d'ajout de photo",
        ["Importer une photo", "Ouvrir la caméra"],
        horizontal=True,
    )

    if photo_mode == "Importer une photo":
        user_photo = st.file_uploader(
            "Importer une photo utilisateur / patient",
            type=["png", "jpg", "jpeg"],
            key="user_photo_upload",
        )
    else:
        user_photo = st.camera_input(
            "Prendre une photo avec la caméra",
            key="user_photo_camera",
        )

    st.markdown("</div>", unsafe_allow_html=True)

    required_missing = []
    if not nom.strip():
        required_missing.append("Nom")
    if not prenom.strip():
        required_missing.append("Prénom")
    if age <= 0:
        required_missing.append("Âge")
    if sexe == "Non spécifié":
        required_missing.append("Sexe")
    if not institution.strip():
        required_missing.append("Institution")
    if not pays.strip():
        required_missing.append("Pays")

    if required_missing:
        st.markdown(
            f"""
            <div class="warning">
            <b>Informations obligatoires manquantes :</b> {", ".join(required_missing)}.<br>
            Vous devez compléter ces informations avant de continuer l'analyse.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.stop()

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Importer une IRM cérébrale</div>', unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Choisir une image IRM",
        type=["png", "jpg", "jpeg", "bmp"],
    )

    st.markdown("</div>", unsafe_allow_html=True)

    if uploaded is None:
        st.markdown(
            """
            <div class="notice">
            Importez une image IRM pour visualiser les canaux AITO-3.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    image = Image.open(uploaded).convert("RGB")
    channels = build_aito3(image)
    overlay = red_contour_overlay(
        channels["original"],
        channels["directional_energy"],
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Visualisation AITO-3</div>', unsafe_allow_html=True)

    v1, v2, v3, v4, v5 = st.columns(5)

    with v1:
        st.image(image, caption="IRM originale", width="stretch")

    with v2:
        st.image(channels["perona_malik"], caption="Perona-Malik", clamp=True, width="stretch")

    with v3:
        st.image(channels["low_frequency"], caption="Basse fréquence", clamp=True, width="stretch")

    with v4:
        st.image(channels["directional_energy"], caption="Énergie directionnelle", clamp=True, width="stretch")

    with v5:
        st.image(overlay, caption="Contours saillants indicatifs", width="stretch")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="warning">
        <b>Note importante :</b> les contours rouges sont des régions saillantes indicatives
        issues du traitement AITO-3. Ils ne constituent pas une segmentation médicale certifiée.
        La connexion complète au moteur AITO-Net sera ajoutée après récupération des backbones sources.
        </div>
        """,
        unsafe_allow_html=True,
    )

    user_info = {
        "nom": nom,
        "prenom": prenom,
        "age": age,
        "sexe": sexe,
        "profil": profil,
        "institution": institution,
        "pays": pays,
        "objectif": objectif,
        "photo_path": user_photo,
    }

    result_info = {
        "Mode": "Visualisation AITO-3",
        "Classification": "Non activée dans cette version stable",
        "Confiance": "Non applicable",
        "Décision": "Prototype de recherche",
    }

    if st.button("Générer le rapport PDF"):
        pdf_path = generate_aitonet_pdf(
            base_dir=__import__("pathlib").Path(__file__).resolve().parents[2],
            user_info=user_info,
            original_image=image,
            channels=channels,
            overlay_image=overlay,
            result_info=result_info,
        )

        with open(pdf_path, "rb") as f:
            st.download_button(
                "Télécharger le rapport PDF",
                data=f,
                file_name="rapport_aitonet_brain_tumor.pdf",
                mime="application/pdf",
            )
