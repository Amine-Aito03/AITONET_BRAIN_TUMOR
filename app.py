import streamlit as st
from pathlib import Path

from app.styles.theme import apply_theme
from app.components.header import render_header
from app.pages.dashboard import render_dashboard
from app.pages.single_mri import render_single_mri
from app.pages.dataset_analysis import render_dataset_analysis
from app.pages.about import render_about

BASE_DIR = Path(__file__).parent

st.set_page_config(
    page_title="AITONET BRAIN TUMOR",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()

render_header(BASE_DIR)

with st.sidebar:
    st.markdown("## Navigation")
    page = st.radio(
        "Menu principal",
        [
            "Tableau de bord",
            "Analyse IRM unique",
            "Analyse dataset",
            "Rapports",
            "À propos",
        ],
    )

if page == "Tableau de bord":
    render_dashboard()

elif page == "Analyse IRM unique":
    render_single_mri()

elif page == "Analyse dataset":
    render_dataset_analysis()

elif page == "À propos":
    render_about()

else:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Module en construction</div>', unsafe_allow_html=True)
    st.write("Cette section sera développée dans l’étape suivante.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    '<div class="footer">AITONET BRAIN TUMOR — Prototype de recherche développé par Amine Ait Ou Aali</div>',
    unsafe_allow_html=True,
)
