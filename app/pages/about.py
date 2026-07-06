import streamlit as st
from pathlib import Path
from PIL import Image

def render_about():
    base_dir = Path(__file__).resolve().parents[2]
    photo_path = base_dir / "assets" / "amine_photo.png"

    st.markdown('<div class="card">', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2.2])

    with col1:
        if photo_path.exists():
            st.image(Image.open(photo_path), width="stretch")
        else:
            st.info("Ajoute ta photo dans assets/amine_photo.png")

    with col2:
        st.markdown('<div class="card-title">À propos du créateur</div>', unsafe_allow_html=True)
        st.markdown("## Amine Ait Ou Aali")
        st.write("**Master 2 — Mathématiques Appliquées et Épidémiologie**")
        st.write("Faculté des Sciences et Techniques — Université Moulay Ismaïl")
        st.write("Créateur de la plateforme **AITONET BRAIN TUMOR**")

        st.markdown("### Profil scientifique")
        st.write(
            "Passionné par les mathématiques appliquées, l’intelligence artificielle, "
            "le calcul scientifique et l’imagerie médicale. Le projet AITONET BRAIN TUMOR "
            "s’inscrit dans le cadre du développement d’un système fiable d’analyse des IRM cérébrales."
        )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Projet de Fin d’Études</div>', unsafe_allow_html=True)
    st.write(
        "**Développement d’un cadre mathématique et algorithmique pour l’analyse fiable "
        "d’images IRM cérébrales.**"
    )
    st.write(
        "Le projet combine Perona–Malik, représentations multi-échelles, Deep Learning, "
        "fusion de modèles, calibration, prédiction sélective et détection OOD."
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Compétences principales</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("**Mathématiques**")
        st.write("EDP, analyse fonctionnelle, modélisation, calcul scientifique.")

    with c2:
        st.markdown("**IA / Deep Learning**")
        st.write("CNN, Transfer Learning, DenseNet, MobileNetV2, calibration, OOD.")

    with c3:
        st.markdown("**Imagerie médicale**")
        st.write("IRM cérébrales, Perona–Malik, DWT, SWT, NSCT, classification.")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Contacts</div>', unsafe_allow_html=True)
    st.write("**Email :** a.aitouaali@edu.umi.ac.ma")
    st.write("**Téléphone :** +212 6 27 10 28 54")
    st.write("**LinkedIn :** à compléter")
    st.write("**ORCID :** à compléter")
    st.write("**ResearchGate :** à compléter")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="warning">
        <b>Avertissement :</b> AITONET BRAIN TUMOR est un prototype de recherche.
        Il ne remplace pas l’avis d’un médecin spécialiste.
        </div>
        """,
        unsafe_allow_html=True,
    )
