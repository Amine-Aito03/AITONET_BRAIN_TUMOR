import streamlit as st
import pandas as pd
from PIL import Image

from app.utils.aito3 import build_aito3


def render_dataset_analysis():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Analyse d’un dataset IRM</div>', unsafe_allow_html=True)

    dataset_name = st.text_input("Nom du dataset")
    responsable = st.text_input("Responsable / utilisateur")
    contexte = st.selectbox(
        "Contexte",
        ["Recherche", "Validation externe", "Enseignement", "Démonstration"],
    )

    files = st.file_uploader(
        "Importer plusieurs images IRM",
        type=["png", "jpg", "jpeg", "bmp"],
        accept_multiple_files=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

    if not files:
        st.markdown(
            """
            <div class="notice">
            Importez plusieurs images pour générer un résumé dataset.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    rows = []

    for f in files:
        try:
            image = Image.open(f).convert("RGB")
            _ = build_aito3(image)

            rows.append({
                "dataset": dataset_name,
                "image": f.name,
                "status": "AITO-3 ready",
                "module": "Visualisation / prototype",
                "responsable": responsable,
                "contexte": contexte,
            })

        except Exception as e:
            rows.append({
                "dataset": dataset_name,
                "image": f.name,
                "status": f"Erreur: {e}",
                "module": "Non traité",
                "responsable": responsable,
                "contexte": contexte,
            })

    df = pd.DataFrame(rows)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Résumé global</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Images importées", len(df))

    with c2:
        st.metric("Images préparées AITO-3", int((df["status"] == "AITO-3 ready").sum()))

    with c3:
        st.metric("Erreurs", int((df["status"] != "AITO-3 ready").sum()))

    st.dataframe(df, width="stretch")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Télécharger le résumé CSV",
        data=csv,
        file_name="aitonet_dataset_summary.csv",
        mime="text/csv",
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="warning">
        Dans cette version, l’analyse dataset vérifie la préparation AITO-3.
        La classification automatique complète sera activée après connexion du moteur AITO-Net complet.
        </div>
        """,
        unsafe_allow_html=True,
    )
