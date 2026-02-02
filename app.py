import streamlit as st
import qrcode
from io import BytesIO

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="AI Investor Style Quiz",
    page_icon="💡",
    layout="centered",
)

# -----------------------------
# Helper: QR code generator
# -----------------------------
@st.cache_data
def make_qr_image(data: str, box_size: int = 10, border: int = 2) -> BytesIO:
    qr = qrcode.QRCode(box_size=box_size, border=border)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

# -----------------------------
# Quiz content (edit-friendly)
# Each option: (label, score)
# -----------------------------
@st.cache_data
def load_quiz():
    return [
        {
            "id": "q1",
            "question": "Q1. Your investment drops 20%. What do you do?",
            "options": [
                ("Sell to stop the loss", 0),
                ("Wait and see", 2),
                ("Buy more (if fundamentals still good)", 4),
            ],
        },
        {
            "id": "q2",
            "question": "Q2. Your goal timeline is…",
            "options": [
                ("0–2 years", 0),
                ("3–5 years", 2),
                ("5+ years", 4),
            ],
        },
        {
            "id": "q3",
            "question": "Q3. Which portfolio feels most comfortable?",
            "options": [
                ("Mostly cash / savings", 0),
                ("Mix of bonds + index funds", 2),
                ("Mostly stocks / index funds", 4),
            ],
        },
        {
            "id": "q4",
            "question": "Q4. When you hear “volatile market”…",
            "options": [
                ("I feel anxious", 0),
                ("I can tolerate it with a plan", 2),
                ("I see opportunity", 4),
            ],
        },
        {
            "id": "q5",
            "question": "Q5. If you had extra money, you prefer…",
            "options": [
                ("Keep it in a safe place", 0),
                ("Invest a part, keep a part", 2),
                ("Invest most of it", 4),
            ],
        },
        {
            "id": "q6",
            "question": "Q6. Your investing style is closer to…",
            "options": [
                ("Capital preservation", 0),
                ("Balanced growth", 2),
                ("Growth-focused", 4),
            ],
        },
        {
            "id": "q7",
            "question": "Q7. How often do you check your investments?",
            "options": [
                ("Every day", 0),
                ("A few times a month", 2),
                ("Monthly / quarterly", 4),
            ],
        },
        {
            "id": "q8",
            "question": "Q8. If your friend says “this stock will 10x”, you…",
            "options": [
                ("Avoid it", 0),
                ("Research first, small position", 2),
                ("Research and consider bigger position", 4),
            ],
        },
    ]

def score_to_result(total_score: int, max_score: int) -> dict:
    # Risk score scaled to 0–100
    risk_score = round((total_score / max_score) * 100)

    if risk_score <= 25:
        investor_type = "Steady Saver (Conservative)"
        portfolio = {"Cash": 40, "Bonds": 40, "Stocks (Index)": 20}
        tip = "Build an emergency fund first, then invest small & consistently."
        watchout = "Low growth risk: inflation may slowly reduce purchasing power."
        strength = "Stable mindset. Less likely to panic-sell."
    elif risk_score <= 55:
        investor_type = "Balanced Builder"
        portfolio = {"Cash": 20, "Bonds": 30, "Stocks (Index)": 50}
        tip = "Set a monthly auto-invest plan and avoid checking prices daily."
        watchout = "Overthinking risk: switching strategy too often."
        strength = "Good balance between safety and growth."
    elif risk_score <= 80:
        investor_type = "Growth Planner"
        portfolio = {"Cash": 10, "Bonds": 20, "Stocks (Index)": 70}
        tip = "Use diversification and a simple rule: rebalance quarterly."
        watchout = "FOMO risk: chasing hype during bull markets."
        strength = "Long-term focus. Can handle normal volatility."
    else:
        investor_type = "Bold Explorer (Aggressive)"
        portfolio = {"Cash": 5, "Bonds": 10, "Stocks (Index)": 70, "Satellite (Themes)": 15}
        tip = "Define clear rules: position size + stop-loss + review schedule."
        watchout = "Overconfidence risk: big drawdowns if concentration is too high."
        strength = "High risk tolerance. Strong conviction-driven action."

    return {
        "risk_score": risk_score,
        "investor_type": investor_type,
        "portfolio": portfolio,
        "tip": tip,
        "strength": strength,
        "watchout": watchout,
    }

def render_portfolio(portfolio: dict):
    st.write("**Sample Portfolio (for demo)**")
    cols = st.columns(len(portfolio))
    for i, (k, v) in enumerate(portfolio.items()):
        with cols[i]:
            st.metric(k, f"{v}%")

# -----------------------------
# Sidebar: Demo Controls
# -----------------------------
st.sidebar.title("⚙️ Demo Controls")
DEMO_MODE = st.sidebar.toggle("Demo Mode (AI Fair)", value=True)

if st.sidebar.button("🔄 Reset Quiz (救命鍵)"):
    st.session_state.clear()
    st.rerun()

st.sidebar.caption("Tip: Demo Mode ON = 更穩、更不容易當機。")

# -----------------------------
# App URL (QR code uses this)
# - Cloud: set APP_URL in Streamlit Secrets
# - Local: fallback to localhost
# -----------------------------
APP_URL = st.secrets.get("APP_URL", "http://localhost:8501")

# Optional: hide Streamlit UI for cleaner demo
if DEMO_MODE:
    st.markdown(
        """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------
# Main UI
# -----------------------------
st.title("💡 AI Investor Style Quiz")
st.caption("Educational demo only — not financial advice.")

with st.expander("📌 How to Play (1 min)"):
    st.write(
        """
1) Answer 8 quick questions  
2) Tap **Submit**  
3) Get your **Risk Score**, **Investor Type**, and a **sample portfolio** + **one action tip**  
"""
    )

# --- QR Section
st.subheader("📱 Scan to Play")

qr_buf = make_qr_image(APP_URL)
st.image(qr_buf, width=240)
st.markdown(f"[Open link]({APP_URL})")

# If app is running locally, help user show a LAN URL hint
if "localhost" in APP_URL or "127.0.0.1" in APP_URL:
    st.info(
        "你現在的 QR 連到 localhost（只有你電腦自己看得到）。\n\n"
        "✅ 要讓手機掃得到：你需要 **雲端網址**（Streamlit Cloud）或同一個 Wi-Fi 下的 **Network URL**。\n"
        "（AI Fair 建議：直接用 Streamlit Cloud 最穩）"
    )

st.markdown("---")

# -----------------------------
# Quiz Form (submit-based)
# -----------------------------
quiz = load_quiz()
max_score = sum(max(opt[1] for opt in q["options"]) for q in quiz)

# Demo: instant result button
if DEMO_MODE:
    cols = st.columns([1, 1, 2])
    with cols[0]:
        if st.button("⚡ Instant Demo Result"):
            # pick middle-high answers to show a nice result
            st.session_state.demo_answers = {q["id"]: q["options"][-1][0] for q in quiz}
            st.session_state.submitted = True
            st.rerun()
    with cols[1]:
        st.write("")  # spacer

# Collect answers
default_answers = st.session_state.get("demo_answers", {})

with st.form("quiz_form"):
    st.subheader("✅ Take the Quiz")

    answers = {}
    for q in quiz:
        labels = [x[0] for x in q["options"]]
        # default selection if demo_answers exists
        if q["id"] in default_answers:
            index = labels.index(default_answers[q["id"]])
        else:
            index = 0

        answers[q["id"]] = st.radio(q["question"], labels, index=index, key=f"radio_{q['id']}")

    submitted = st.form_submit_button("✅ Submit")

# -----------------------------
# Result Rendering (safe)
# -----------------------------
try:
    submitted_flag = submitted or st.session_state.get("submitted", False)
    if submitted_flag:
        # map label -> score
        total = 0
        for q in quiz:
            chosen_label = answers[q["id"]]
            score_map = dict(q["options"])
            total += score_map[chosen_label]

        result = score_to_result(total, max_score)

        st.markdown("---")
        st.header("🎯 Your Result")

        c1, c2 = st.columns([1, 1])
        with c1:
            st.metric("Risk Score", result["risk_score"])
        with c2:
            st.write(f"**Investor Type:** {result['investor_type']}")

        st.write("")
        st.write(f"✅ **Strength:** {result['strength']}")
        st.write(f"⚠️ **Watch out:** {result['watchout']}")
        st.write(f"💡 **One action tip:** {result['tip']}")

        st.write("")
        render_portfolio(result["portfolio"])

        st.markdown("---")
        st.caption("Made for AI Fair demo. Educational use only.")

        # clear one-time flags
        st.session_state.submitted = False

except Exception:
    st.error("Oops! Something went wrong. Please tap **Reset Quiz** and try again 🙏")
    st.stop()
