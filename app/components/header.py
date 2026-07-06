import streamlit as st
from pathlib import Path
from PIL import Image

def render_header(base_dir: Path):
    assets_dir = base_dir / "assets"

    fst_logo = assets_dir / "logo_fst.jpg"
    aito_logo = assets_dir / "AITOLOGO.png"

    st.markdown('<div class="aitonet-header">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.2, 3.6, 1.2])

    with col1:
        if fst_logo.exists():
            st.image(Image.open(fst_logo), width="stretch")

    with col2:
        st.markdown(
            """
            <div style="text-align:center;">
                <div class="aitonet-title">AITONET BRAIN TUMOR</div>
                <div class="aitonet-subtitle">
                    Plateforme intelligente d’analyse des IRM cérébrales
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        if aito_logo.exists():
            st.image(Image.open(aito_logo), width="stretch")

    st.markdown('</div>', unsafe_allow_html=True)
