import streamlit as st
import qrcode
from io import BytesIO
import pandas as pd
import altair as alt

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="AI Investor Style Quiz",
    page_icon="💡",
    layout="centered",
)

# -----------------------------
# Force WHITE background (even in themes)
# -----------------------------
st.markdown(
    """
    <style>
      .stApp { background-color: #ffffff; }
      [data-testid="stAppViewContainer"] { background-color: #ffffff; }
      [data-testid="stHeader"] { background: rgba(255,255,255,0); }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Helper: QR code generator
# -----------------------------
@st.cache_data
def make_qr_image(data: str, box_size: int = 10, border: int = 2) -> BytesIO:
    qr = qrcode.QRCode(box_size=box_size, border=border)
    qr.add_data(data)
    qr.make(fit=True)
    

    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

# -----------------------------
# Quiz content
# Each option: (label, score)
# -----------------------------
@st.cache_data
def load_quiz_standard():
    return [
        {"id": "q1", "question": "Q1. Your investment drops 20%. What do you do?",
         "options": [("Sell to stop the loss", 0), ("Wait and see", 2), ("Buy more (if fundamentals still good)", 4)]},

        {"id": "q2", "question": "Q2. Your goal timeline is…",
         "options": [("0–2 years", 0), ("3–5 years", 2), ("5+ years", 4)]},

        {"id": "q3", "question": "Q3. Which portfolio feels most comfortable?",
         "options": [("Mostly cash / savings", 0), ("Mix of bonds + index funds", 2), ("Mostly stocks / index funds", 4)]},

        {"id": "q4", "question": "Q4. When you hear “volatile market”…",
         "options": [("I feel anxious", 0), ("I can tolerate it with a plan", 2), ("I see opportunity", 4)]},

        {"id": "q5", "question": "Q5. If you had extra money, you prefer…",
         "options": [("Keep it in a safe place", 0), ("Invest a part, keep a part", 2), ("Invest most of it", 4)]},

        {"id": "q6", "question": "Q6. Your investing style is closer to…",
         "options": [("Capital preservation", 0), ("Balanced growth", 2), ("Growth-focused", 4)]},

        {"id": "q7", "question": "Q7. How often do you check your investments?",
         "options": [("Every day", 0), ("A few times a month", 2), ("Monthly / quarterly", 4)]},

        {"id": "q8", "question": "Q8. If your friend says “this stock will 10x”, you…",
         "options": [("Avoid it", 0), ("Research first, small position", 2), ("Research and consider bigger position", 4)]},

        {"id": "q9", "question": "Q9. If the market drops, you feel…",
         "options": [("I want to exit quickly", 0), ("I stay calm if I have a plan", 2), ("I feel excited to buy at lower prices", 4)]},

        {"id": "q10", "question": "Q10. Your main investing goal is…",
         "options": [("Safety and stability", 0), ("Steady long-term growth", 2), ("Max growth and big outcomes", 4)]},
    ]

@st.cache_data
def load_quiz_beginner():
    # Simpler wording for international students with little finance knowledge
    return [
        {"id": "q1", "question": "Q1. If you lose money, what do you do?",
         "options": [("Stop and avoid risk", 0), ("Wait and think", 2), ("Try again carefully", 4)]},

        {"id": "q2", "question": "Q2. How long are you okay leaving money invested?",
         "options": [("Less than 1 year", 0), ("2–3 years", 2), ("5+ years", 4)]},

        {"id": "q3", "question": "Q3. Which feels safest to you?",
         "options": [("Keep cash", 0), ("Mix safe + growth", 2), ("Mostly growth assets", 4)]},

        {"id": "q4", "question": "Q4. When prices go up and down, you feel…",
         "options": [("Nervous", 0), ("OK if I understand", 2), ("Calm or curious", 4)]},

        {"id": "q5", "question": "Q5. You get $1,000. What do you do?",
         "options": [("Save it", 0), ("Save some, invest some", 2), ("Invest most", 4)]},

        {"id": "q6", "question": "Q6. Which sounds most like you?",
         "options": [("Careful", 0), ("Balanced", 2), ("Bold", 4)]},

        {"id": "q7", "question": "Q7. How often would you check results?",
         "options": [("Every day", 0), ("Sometimes", 2), ("Not often", 4)]},

        {"id": "q8", "question": "Q8. A friend says: “This will grow fast!” You…",
         "options": [("Ignore it", 0), ("Research first", 2), ("Research and try", 4)]},

        {"id": "q9", "question": "Q9. If markets fall suddenly, you feel…",
         "options": [("Scared", 0), ("Thoughtful", 2), ("Ready to act", 4)]},

        {"id": "q10", "question": "Q10. Your main goal is…",
         "options": [("Protect money", 0), ("Grow slowly", 2), ("Grow a lot", 4)]},
    ]

# -----------------------------
# Result logic
# -----------------------------
def score_to_result(total_score: int, max_score: int) -> dict:
    risk_score = round((total_score / max_score) * 100)

    if risk_score <= 25:
        investor_type = "Steady Saver (Conservative)"
        portfolio = {"Cash": 40, "Bonds": 40, "Stocks (Index)": 20}
        tip = "Build an emergency fund first, then invest small & consistently."
        watchout = "Inflation may reduce purchasing power over time."
        strength = "Stable mindset. Less likely to panic-sell."
    elif risk_score <= 55:
        investor_type = "Balanced Builder"
        portfolio = {"Cash": 20, "Bonds": 30, "Stocks (Index)": 50}
        tip = "Set a monthly auto-invest plan and avoid checking prices daily."
        watchout = "Switching strategies too often can hurt consistency."
        strength = "Good balance between safety and growth."
    elif risk_score <= 80:
        investor_type = "Growth Planner"
        portfolio = {"Cash": 10, "Bonds": 20, "Stocks (Index)": 70}
        tip = "Diversify and rebalance quarterly."
        watchout = "FOMO can lead to chasing hype."
        strength = "Long-term focus. Can handle normal volatility."
    else:
        investor_type = "Bold Explorer (Aggressive)"
        portfolio = {"Cash": 5, "Bonds": 10, "Stocks (Index)": 70, "Satellite (Themes)": 15}
        tip = "Define rules: position size + stop-loss + review schedule."
        watchout = "Too much concentration can cause big drawdowns."
        strength = "High risk tolerance. Strong conviction-driven action."

    return {
        "risk_score": risk_score,
        "investor_type": investor_type,
        "portfolio": portfolio,
        "tip": tip,
        "strength": strength,
        "watchout": watchout,
    }

# -----------------------------
# Pretty Charts (Altair)
# -----------------------------
def risk_gauge(score: int, title: str = "Risk Score (0–100)"):
    score = max(0, min(100, int(score)))

    base = pd.DataFrame({
        "start": [0, 25, 50, 75],
        "end":   [25, 50, 75, 100],
        "label": ["Conservative", "Balanced", "Growth", "Aggressive"]
    })

    bands = alt.Chart(base).mark_arc(innerRadius=70, outerRadius=100).encode(
        theta=alt.Theta("start:Q", stack=None),
        theta2="end:Q",
        color=alt.Color("label:N", legend=None)
    )

    pointer_df = pd.DataFrame({"start": [max(score - 1, 0)], "end": [score]})
    pointer = alt.Chart(pointer_df).mark_arc(innerRadius=65, outerRadius=112).encode(
        theta=alt.Theta("start:Q", stack=None),
        theta2="end:Q",
        color=alt.value("black")
    )

    text = alt.Chart(pd.DataFrame({"text": [f"{score}/100"]})).mark_text(
        size=34, fontWeight="bold"
    ).encode(text="text:N")

    return (bands + pointer + text).properties(width=320, height=220, title=title)

def portfolio_donut(portfolio: dict, title: str = "Sample Portfolio"):
    if not portfolio or sum(portfolio.values()) <= 0:
        portfolio = {"Cash": 100}

    df = pd.DataFrame({"Asset": list(portfolio.keys()), "Weight": list(portfolio.values())})
    return alt.Chart(df).mark_arc(innerRadius=70, outerRadius=120).encode(
        theta=alt.Theta("Weight:Q"),
        color=alt.Color("Asset:N", legend=alt.Legend(title=None)),
        tooltip=["Asset:N", "Weight:Q"]
    ).properties(width=320, height=260, title=title)

def contribution_bar(contrib: dict, title: str = "Why you got this result"):
    if not contrib:
        contrib = {"No data": 0}

    df = pd.DataFrame({"Question": list(contrib.keys()), "Impact": list(contrib.values())})
    df = df.sort_values("Impact", ascending=False).head(8)

    return alt.Chart(df).mark_bar().encode(
        x=alt.X("Impact:Q", title="Impact (higher = more risk-taking)"),
        y=alt.Y("Question:N", sort="-x", title=None),
        tooltip=["Question:N", "Impact:Q"]
    ).properties(width=520, height=260, title=title)

# -----------------------------
# Sidebar: Demo Controls
# -----------------------------
st.sidebar.title("⚙️ Demo Controls")
DEMO_MODE = st.sidebar.toggle("Demo Mode (AI Fair)", value=True)

MODE = st.sidebar.radio(
    "Quiz Version",
    ["Beginner Mode (Simpler English)", "Standard Mode"],
    index=0
)

if st.sidebar.button("🔄 Reset Quiz (救命鍵)"):
    st.session_state.clear()
    st.rerun()

st.sidebar.caption("Demo Mode ON = more stable for live demos.")

# -----------------------------
# App URL for QR (Cloud Secrets recommended)
# -----------------------------
APP_URL = st.secrets.get("APP_URL", "http://localhost:8501")

# Hide Streamlit chrome in demo mode (cleaner)
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
1) Scan QR code (or open the link)  
2) Answer 10 quick questions  
3) Tap **Submit**  
4) See your **Risk Score**, **Investor Type**, and **Charts** instantly  
"""
    )

# QR Section
st.subheader("📱 Scan to Play")
st.image(make_qr_image(APP_URL), width=240)
st.markdown(f"**Share link:** {APP_URL}")

if "localhost" in APP_URL or "127.0.0.1" in APP_URL:
    st.info(
        "Your QR is pointing to localhost (only your computer can open it).\n\n"
        "✅ For AI Fair: set APP_URL in Streamlit Cloud Secrets to your public https link."
    )

st.markdown("---")

# Choose quiz set
quiz = load_quiz_beginner() if MODE.startswith("Beginner") else load_quiz_standard()
max_score = sum(max(opt[1] for opt in q["options"]) for q in quiz)

# Demo: one-click result
if DEMO_MODE:
    cols = st.columns([1, 2, 3])
    with cols[0]:
        if st.button("⚡ Instant Demo Result"):
            st.session_state.demo_answers = {q["id"]: q["options"][-1][0] for q in quiz}
            st.session_state.force_submit = True
            st.rerun()

default_answers = st.session_state.get("demo_answers", {})

# -----------------------------
# Quiz Form (submit-based)
# -----------------------------
with st.form("quiz_form"):
    st.subheader("✅ Take the Quiz")
    answers = {}

    for q in quiz:
        labels = [x[0] for x in q["options"]]
        index = labels.index(default_answers[q["id"]]) if q["id"] in default_answers else 0
        answers[q["id"]] = st.radio(q["question"], labels, index=index, key=f"radio_{q['id']}")

    submitted = st.form_submit_button("✅ Submit")

# -----------------------------
# Results (safe render)
# -----------------------------
try:
    do_submit = submitted or st.session_state.get("force_submit", False)

    if do_submit:
        total = 0
        question_contrib = {}

        for q in quiz:
            chosen_label = answers[q["id"]]
            score_map = dict(q["options"])
            s = score_map[chosen_label]   # 0/2/4
            total += s

            short_q = q["question"].split(". ", 1)[-1]
            question_contrib[short_q] = s

        result = score_to_result(total, max_score)
        risk_score = result["risk_score"]

        st.markdown("---")
        st.header("🎯 Your Result")

        c1, c2 = st.columns([1, 1])
        with c1:
            st.metric("Risk Score", f"{risk_score}/100")
        with c2:
            st.write(f"**Investor Type:** {result['investor_type']}")

        st.write("")
        st.write(f"✅ **Strength:** {result['strength']}")
        st.write(f"⚠️ **Watch out:** {result['watchout']}")
        st.write(f"💡 **One action tip:** {result['tip']}")

        st.markdown("## 📊 Your Dashboard")
        cc1, cc2 = st.columns([1, 1])
        with cc1:
            st.altair_chart(risk_gauge(risk_score, title="Risk Score"), use_container_width=True)
        with cc2:
            st.altair_chart(portfolio_donut(result["portfolio"], title="Sample Portfolio"), use_container_width=True)

        st.altair_chart(contribution_bar(question_contrib, title="Answer Impact (Explainable)"), use_container_width=True)

        st.markdown("---")
        st.caption("Made for AI Fair demo. Educational use only.")

        # clear one-time flags
        st.session_state.force_submit = False
        st.session_state.demo_answers = {}

except Exception:
    st.error("Oops! Something went wrong. Please tap **Reset Quiz** and try again 🙏")
    st.stop()
