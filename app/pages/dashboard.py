import streamlit as st

def render_dashboard():
    st.markdown(
        """
        <div class="hero-card">
            <h1>Analyse intelligente des IRM cérébrales</h1>
            <p>
            AITONET BRAIN TUMOR est une plateforme de recherche combinant
            classification des tumeurs cérébrales, visualisation AITO-3,
            calibration de confiance, prédiction sélective et analyse OOD.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown('<div class="metric-card"><div class="metric-value">98.69%</div><div class="metric-label">Accuracy finale</div></div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="metric-card"><div class="metric-value">0.005</div><div class="metric-label">ECE après TS</div></div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="metric-card"><div class="metric-value">0.95</div><div class="metric-label">AUROC OOD</div></div>', unsafe_allow_html=True)

    with c4:
        st.markdown('<div class="metric-card"><div class="metric-value">4</div><div class="metric-label">Classes</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Classes étudiées</div>', unsafe_allow_html=True)
    st.write("glioma · meningioma · notumor · pituitary")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Valeur ajoutée de la plateforme</div>', unsafe_allow_html=True)
    st.write("• Visualisation AITO-3 : Perona-Malik, basse fréquence, énergie directionnelle.")
    st.write("• Confiance calibrée avec Temperature Scaling.")
    st.write("• Prédiction sélective pour identifier les cas incertains.")
    st.write("• Détection OOD pour signaler les images hors domaine.")
    st.write("• Génération future de rapports PDF professionnels.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="warning">
        <b>Avertissement :</b> cette plateforme est un prototype de recherche.
        Elle ne remplace pas un diagnostic médical.
        </div>
        """,
        unsafe_allow_html=True,
    )
