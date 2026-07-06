import streamlit as st

def apply_theme():
    st.markdown(
        """
<style>
:root {
    --fst-blue-dark: #003B73;
    --fst-blue: #005A9C;
    --umi-orange: #F28C28;
    --soft-bg: #F6FAFF;
    --text-main: #172033;
}

.stApp {
    background: linear-gradient(135deg, #F6FAFF 0%, #FFFFFF 55%, #FFF7EF 100%);
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}

.aitonet-header {
    background: white;
    border-radius: 24px;
    padding: 18px 26px;
    box-shadow: 0 12px 35px rgba(0, 59, 115, 0.12);
    border: 1px solid rgba(0, 90, 156, 0.10);
    margin-bottom: 22px;
}

.aitonet-title {
    font-size: 38px;
    font-weight: 900;
    color: var(--fst-blue-dark);
    letter-spacing: 0.5px;
    margin-bottom: 0;
}

.aitonet-subtitle {
    font-size: 16px;
    color: #5f6b7a;
    margin-top: 4px;
}

.hero-card {
    background: linear-gradient(120deg, #003B73, #005A9C);
    color: white;
    padding: 30px;
    border-radius: 26px;
    box-shadow: 0 20px 50px rgba(0, 59, 115, 0.22);
    margin-bottom: 24px;
}

.hero-card h1 {
    font-size: 42px;
    font-weight: 900;
    margin-bottom: 8px;
}

.hero-card p {
    font-size: 17px;
    opacity: 0.94;
}

.card {
    background: white;
    padding: 24px;
    border-radius: 22px;
    box-shadow: 0 12px 30px rgba(0, 59, 115, 0.10);
    border: 1px solid rgba(0, 90, 156, 0.08);
    margin-bottom: 20px;
}

.card-title {
    font-size: 22px;
    font-weight: 850;
    color: var(--fst-blue-dark);
    margin-bottom: 10px;
}

.metric-card {
    background: white;
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    border-top: 5px solid var(--umi-orange);
    box-shadow: 0 10px 28px rgba(0, 59, 115, 0.10);
}

.metric-value {
    font-size: 30px;
    font-weight: 900;
    color: var(--fst-blue-dark);
}

.metric-label {
    color: #657183;
    font-size: 14px;
}

.notice {
    padding: 16px;
    border-radius: 16px;
    background: #EAF3FF;
    border-left: 6px solid var(--fst-blue);
}

.warning {
    padding: 16px;
    border-radius: 16px;
    background: #FFF4E6;
    border-left: 6px solid var(--umi-orange);
}

.footer {
    text-align: center;
    color: #6B7280;
    font-size: 13px;
    margin-top: 40px;
}
</style>
        """,
        unsafe_allow_html=True,
    )
