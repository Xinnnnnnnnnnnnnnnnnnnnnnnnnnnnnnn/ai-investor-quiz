import os
import streamlit as st

import plotly.graph_objects as go

import qrcode
from PIL import Image
from io import BytesIO


# =========================================================
# Page config
# =========================================================
st.set_page_config(
    page_title="AI Investor Style Quiz",
    page_icon="💡",
    layout="centered",
)

# =========================================================
# Global CSS: white background + black text (mobile friendly)
# =========================================================
st.markdown(
    """
    <style>
    /* App background */
    .stApp {
        background-color: #ffffff !important;
        color: #111111 !important;
    }

    /* Ensure common text is visible */
    html, body, [class*="css"]  {
        color: #111111 !important;
    }

    /* Titles */
    h1, h2, h3, h4, h5, h6 {
        color: #111111 !important;
    }

    /* Radio / labels */
    label, .stRadio label, .stRadio div {
        color: #111111 !important;
    }

    /* Buttons */
    .stButton>button {
        background: #111111 !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        padding: 0.55rem 1rem !important;
        border: none !important;
    }

    /* Reduce weird dark blocks on some mobile browsers */
    .block-container {
        padding-top: 1.6rem;
        padding-bottom: 2.2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# Helpers
# =========================================================
def build_qr_image(url: str) -> Image.Image:
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=8,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img.convert("RGB")


def get_public_url() -> str:
    """
    Prefer a stable public URL for QR code:
    1) Streamlit secrets: st.secrets["PUBLIC_URL"]
    2) Environment variable: PUBLIC_URL
    3) Fallback: st.experimental_get_query_params-based is not reliable
       so we fallback to localhost message.
    """
    # 1) Secrets
    try:
        if "PUBLIC_URL" in st.secrets and st.secrets["PUBLIC_URL"]:
            return str(st.secrets["PUBLIC_URL"]).strip()
    except Exception:
        pass

    # 2) Env var
    env_url = os.getenv("PUBLIC_URL", "").strip()
    if env_url:
        return env_url

    # 3) If deployed on streamlit.app, you can hardcode it here too:
    # return "https://your-app-name.streamlit.app"

    return "http://localhost:8501"


def clamp(n, lo, hi):
    return max(lo, min(hi, n))


# =========================================================
# Quiz definition (10 questions)
# Each option has a score contribution: (low / mid / high risk appetite)
# =========================================================
QUESTIONS = [
    {
        "key": "q1",
        "title": "Q1. Your investment drops 20%. What do you do?",
        "options": [
            ("Sell to stop the loss", 0),
            ("Wait and see", 5),
            ("Buy more (long-term)", 10),
        ],
    },
    {
        "key": "q2",
        "title": "Q2. How do you feel about volatility?",
        "options": [
            ("I hate it", 0),
            ("I can accept some", 5),
            ("I’m okay with big swings", 10),
        ],
    },
    {
        "key": "q3",
        "title": "Q3. How long can you keep money invested?",
        "options": [
            ("< 1 year", 0),
            ("1–3 years", 5),
            ("> 3 years", 10),
        ],
    },
    {
        "key": "q4",
        "title": "Q4. Which return do you prefer?",
        "options": [
            ("Stable and smaller", 0),
            ("Balanced", 5),
            ("Higher growth, higher risk", 10),
        ],
    },
    {
        "key": "q5",
        "title": "Q5. You get $1,000. What do you do?",
        "options": [
            ("Save it", 0),
            ("Save some, invest some", 5),
            ("Invest most", 10),
        ],
    },
    {
        "key": "q6",
        "title": "Q6. Which sounds most like you?",
        "options": [
            ("Careful", 0),
            ("Balanced", 5),
            ("Bold", 10),
        ],
    },
    {
        "key": "q7",
        "title": "Q7. How often would you check results?",
        "options": [
            ("Every day", 0),
            ("Sometimes", 5),
            ("Not often", 10),
        ],
    },
    {
        "key": "q8",
        "title": "Q8. A friend says: “This will grow fast!” You…",
        "options": [
            ("Ignore it", 0),
            ("Research first", 5),
            ("Research and try", 10),
        ],
    },
    {
        "key": "q9",
        "title": "Q9. If markets fall suddenly, you feel…",
        "options": [
            ("Scared", 0),
            ("Thoughtful", 5),
            ("Ready to act", 10),
        ],
    },
    {
        "key": "q10",
        "title": "Q10. Your main goal is…",
        "options": [
            ("Protect money", 0),
            ("Grow slowly", 5),
            ("Grow a lot", 10),
        ],
    },
]


def compute_score_and_contrib(answers: dict):
    """
    answers: {q_key: selected_label}
    returns:
      risk_score (0-100)
      question_contrib: {short_label: contribution_0_100}
    """
    raw_total = 0
    raw_max = 0
    contrib_raw = {}

    for q in QUESTIONS:
        raw_max += max(score for _, score in q["options"])
        chosen = answers.get(q["key"])
        chosen_score = 0
        for label, score in q["options"]:
            if label == chosen:
                chosen_score = score
                break

        raw_total += chosen_score
        # Keep each question's "contribution" in same scale (0-10) first
        # We'll scale to 0-100 later.
        short = q["title"].replace("Q", "").split(".")[0].strip()
        # fallback short label:
        if not short:
            short = q["key"].upper()
        contrib_raw[short] = chosen_score

    # Scale to 0-100
    if raw_max == 0:
        risk_score = 0
    else:
        risk_score = int(round((raw_total / raw_max) * 100))

    # per-question contribution as 0-100 (relative within question max 10)
    question_contrib = {}
    for k, v in contrib_raw.items():
        question_contrib[k] = int(round((v / 10) * 100))

    return clamp(risk_score, 0, 100), question_contrib


def investor_type_from_score(score: int):
    if score <= 33:
        return "Conservative", "You prefer stability and lower risk."
    if score <= 66:
        return "Balanced", "You accept some risk for steady growth."
    return "Growth", "You seek higher returns and can tolerate volatility."


def portfolio_from_score(score: int):
    # Simple demo allocation
    if score <= 33:
        return {"Bonds": 55, "Cash": 30, "Stocks (Index)": 15}
    if score <= 66:
        return {"Bonds": 40, "Cash": 20, "Stocks (Index)": 40}
    return {"Bonds": 20, "Cash": 10, "Stocks (Index)": 70}


def money_tip_from_score(score: int):
    if score <= 33:
        return "Tip: Start with a small monthly amount and build a 3–6 month emergency fund first."
    if score <= 66:
        return "Tip: Use index funds + rebalance every 6–12 months to stay consistent."
    return "Tip: Define your risk rules first (max drawdown, time horizon), then invest with discipline."


# =========================================================
# Header
# =========================================================
st.markdown("# 💡 AI Investor Style Quiz")
st.caption("Educational demo only — not financial advice.")
st.markdown("---")

# =========================================================
# QR section (for AI Fair)
# =========================================================
public_url = get_public_url()
st.markdown("## 📱 Scan to Play")
qr_img = build_qr_image(public_url)
st.image(qr_img, width=260)
st.write(public_url)
st.markdown("---")

# =========================================================
# Session state
# =========================================================
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "answers" not in st.session_state:
    st.session_state.answers = {}


# =========================================================
# Quiz form
# =========================================================
st.markdown("## ✅ Take the Quiz")

with st.form("quiz_form", clear_on_submit=False):
    for q in QUESTIONS:
        labels = [opt[0] for opt in q["options"]]
        default = 0

        prev = st.session_state.answers.get(q["key"])
        if prev in labels:
            default = labels.index(prev)

        choice = st.radio(
            q["title"],
            labels,
            index=default,
            key=f"radio_{q['key']}",
        )
        st.session_state.answers[q["key"]] = choice

    submitted = st.form_submit_button("✅ Submit")

if submitted:
    st.session_state.submitted = True


# =========================================================
# Results / Dashboard
# =========================================================
if st.session_state.submitted:
    answers = st.session_state.answers
    risk_score, question_contrib = compute_score_and_contrib(answers)
    investor_type, investor_desc = investor_type_from_score(risk_score)
    portfolio = portfolio_from_score(risk_score)
    tip = money_tip_from_score(risk_score)

    st.markdown("---")
    st.markdown("## 📊 Your Result")

    # Summary card
    st.markdown(
        f"""
        **Risk Score:** {risk_score}/100  
        **Investor Type:** {investor_type}  
        {investor_desc}  
        """
    )
    st.info(tip)

    st.markdown("---")
    st.markdown("## 📊 Your Dashboard")

    # ---------- GAUGE (WHITE THEME) ----------
    fig_gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=risk_score,
            number={"font": {"size": 40, "color": "black"}},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#1f77b4"},
                "steps": [
                    {"range": [0, 33], "color": "#9ad0f5"},
                    {"range": [33, 66], "color": "#5dade2"},
                    {"range": [66, 100], "color": "#e74c3c"},
                ],
            },
        )
    )
    fig_gauge.update_layout(
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="black"),
        margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

    # ---------- PORTFOLIO PIE (WHITE THEME) ----------
    fig_pie = go.Figure(
        data=[
            go.Pie(
                labels=list(portfolio.keys()),
                values=list(portfolio.values()),
                hole=0.6,
            )
        ]
    )
    fig_pie.update_layout(
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="black"),
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(orientation="v"),
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    # ---------- ANSWER IMPACT (WHITE THEME) ----------
    st.markdown("### 📈 Answer Impact (Explainable)")

    impact_labels = list(question_contrib.keys())
    impact_values = list(question_contrib.values())

    fig_bar = go.Figure(
        data=[
            go.Bar(
                x=impact_values,
                y=impact_labels,
                orientation="h",
            )
        ]
    )
    fig_bar.update_layout(
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="black"),
        xaxis=dict(title="Contribution (0–100)"),
        yaxis=dict(title=""),
        margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reset for next person"):
            st.session_state.submitted = False
            st.session_state.answers = {}
            st.rerun()

    with col2:
        st.caption("AI Fair mode: Reset after each user ✅")


# =========================================================
# Footer
# =========================================================
st.caption("© Demo project for AI Fair — Casey")
