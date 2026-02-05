st.markdown("""
<style>

/* ===== FORCE LIGHT MODE ===== */

:root {
    --background-color: white !important;
}

html, body, .stApp {
    background-color: white !important;
    color: black !important;
}

/* 主內容區 */
[data-testid="stAppViewContainer"] {
    background-color: white !important;
}

/* Header */
[data-testid="stHeader"] {
    background-color: white !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: white !important;
}

/* 所有文字 */
h1, h2, h3, h4, h5, p, span, label, div {
    color: black !important;
}

/* Radio / checkbox */
div[role="radiogroup"] label {
    color: black !important;
}

/* Button */
div.stButton > button {
    background-color: white !important;
    color: black !important;
    border: 2px solid black !important;
    border-radius: 8px;
    font-size: 18px;
}

/* Plotly 白底 */
.plotly, .js-plotly-plot {
    background: white !important;
}

/* 移除暗色 layer */
section.main > div {
    background-color: white !important;
}

</style>
""", unsafe_allow_html=True)
