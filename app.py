import streamlit as st
import plotly.graph_objects as go

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="AI Investor Style Quiz",
    layout="wide"
)

# ===============================
# GLOBAL WHITE THEME
# ===============================
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

# ===============================
# TITLE
# ===============================
st.title("💡 AI Investor Style Quiz")
st.caption("Educational demo only — not financial advice.")

st.divider()

# ===============================
# QUESTIONS
# ===============================

questions = [
    ("Q1. Market drops 20%. You...", ["Sell immediately", "Hold", "Buy more"]),
    ("Q2. Investment goal?", ["Preserve capital", "Balanced growth", "Max growth"]),
    ("Q3. Risk makes you feel...", ["Nervous", "Neutral", "Excited"]),
    ("Q4. Portfolio style?", ["Stable", "Mixed", "Aggressive"]),
    ("Q5. You get $1,000...", ["Save it", "Split", "Invest most"]),
    ("Q6. Which sounds most like you?", ["Careful", "Balanced", "Bold"]),
    ("Q7. Check results?", ["Daily", "Sometimes", "Rarely"]),
    ("Q8. Friend says hot stock...", ["Ignore", "Research", "Try"]),
    ("Q9. Market crash?", ["Scared", "Thoughtful", "Ready"]),
    ("Q10. Main goal?", ["Protect", "Grow slowly", "Grow a lot"]),
]

answers = []
score_map = [0, 5, 10]

for i, (q, opts) in enumerate(questions):
    choice = st.radio(q, opts, index=1, key=q)
    answers.append(score_map[opts.index(choice)])

# ===============================
# SUBMIT
# ===============================
submitted = st.button("✅ Submit")

# ===============================
# RESULT LOGIC
# ===============================
if submitted:

    risk_score = sum(answers)

    if risk_score < 35:
        investor_type = "Conservative"
        description = "Prefers stability and capital protection."
        allocation = {"Bonds": 50, "Stocks (Index)": 30, "Cash": 20}

    elif risk_score < 70:
        investor_type = "Balanced"
        description = "Seeks growth with controlled volatility."
        allocation = {"Bonds": 30, "Stocks (Index)": 50, "Cash": 20}

    else:
        investor_type = "Aggressive"
        description = "Targets long-term growth and accepts volatility."
        allocation = {"Bonds": 15, "Stocks (Index)": 70, "Cash": 15}

    st.divider()
    st.header("📊 Your Result")

    st.subheader(f"Investor Type: {investor_type}")
    st.subheader(f"Risk Score: {risk_score}/100")

    st.write("### 🧠 Profile Summary")
    st.write(description)

    # ===============================
    # DONUT CHART
    # ===============================
    fig = go.Figure(
        data=[
            go.Pie(
                labels=list(allocation.keys()),
                values=list(allocation.values()),
                hole=0.6,
                textinfo="percent",
            )
        ]
    )

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="black", size=16),
        legend=dict(font=dict(color="black")),
    )

    st.plotly_chart(fig, use_container_width=True)

    # ===============================
    # AI FAIR SUMMARY BOX
    # ===============================
    st.write("### 🎯 AI Fair Quick Explanation")

    st.info(f"""
This user is classified as **{investor_type}**.

• Risk tolerance level is **{risk_score}/100**  
• Decision style: {description}  
• Suggested portfolio focuses on balance between growth and stability  

👉 This demo shows how AI can translate behavior into financial profiles.
""")

    # ===============================
    # RESET BUTTON
    # ===============================
    st.divider()
    if st.button("🔄 Reset for next person"):
        st.session_state.clear()
        st.experimental_rerun()
