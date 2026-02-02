import streamlit as st
import matplotlib.pyplot as plt
import qrcode
from io import BytesIO

# -----------------------------
# BASIC SETTINGS
# -----------------------------
st.set_page_config(page_title="AI Investor Style Quiz", layout="centered")

# Fair 當天要換成你的區網 IP
APP_URL = "http://localhost:8501"

# -----------------------------
# QUIZ QUESTIONS (10)
# A=0 low risk, B=1 medium, C=2 high risk
# -----------------------------
QUESTIONS = [
    ("Your investment drops 20%. What do you do?",
     ["Sell to stop the loss", "Wait and see", "Buy more"]),
    ("How long can you leave this money invested?",
     ["Less than 1 year", "3–5 years", "10+ years"]),
    ("Which sounds most comfortable?",
     ["Small steady growth", "Medium ups and downs", "Big ups and downs"]),
    ("You get $1,000 to invest. What do you do?",
     ["Keep it in cash", "Split between safe and growth", "Put most in growth"]),
    ("What matters most?",
     ["Protect my money", "Grow steadily", "Maximize long-term returns"]),
    ("How often would you check investments?",
     ["Every day", "Monthly", "A few times a year"]),
    ("If the market is scary, you…",
     ["Stay out", "Invest slowly over time", "Buy more because prices are lower"]),
    ("Which portfolio feels safest?",
     ["Mostly savings/bonds", "Balanced mix", "Mostly stocks"]),
    ("Why are you investing?",
     ["Short-term needs", "Future stability", "Big long-term goals"]),
    ("Which fits you best?",
     ["I dislike losses", "I want balance", "I can wait for growth"]),
]

def calc_risk_score(answer_indices):
    """answer_indices: list of 10 numbers (0/1/2). Return 0-100 score."""
    raw = sum(answer_indices)  # 0..20
    score = int(round((raw / 20) * 100))
    return score

def investor_type(score):
    if score <= 33:
        return "🛡 Careful Saver"
    elif score <= 66:
        return "⚖ Balanced Planner"
    return "🚀 Growth Seeker"

def portfolio_for(t):
    if "Careful" in t:
        return {"Stocks": 30, "Bonds": 50, "Cash": 20}
    if "Balanced" in t:
        return {"Stocks": 55, "Bonds": 30, "Cash": 15}
    return {"Stocks": 80, "Bonds": 15, "Cash": 5}

def tip_for(t):
    if "Careful" in t:
        return "Tip: Build an emergency fund first."
    if "Balanced" in t:
        return "Tip: Diversify and invest consistently."
    return "Tip: Focus on long-term goals. Avoid panic selling."

def draw_risk_bar(score):
    fig, ax = plt.subplots()
    ax.barh(["Risk"], [score])
    ax.set_xlim(0, 100)
    ax.set_xlabel("0 = Low, 100 = High")
    ax.set_title("Risk Level")
    st.pyplot(fig)

def draw_portfolio_pie(portfolio):
    fig, ax = plt.subplots()
    ax.pie(portfolio.values(), labels=portfolio.keys(), autopct="%1.0f%%", startangle=90)
    ax.set_title("Sample Portfolio Mix")
    st.pyplot(fig)

# -----------------------------
# UI
# -----------------------------
st.title("💡 AI Investor Style Quiz")
st.caption("Educational demo only — not financial advice.")

# QR (先用 localhost 測試)
st.subheader("📱 Scan to Play")
qr = qrcode.make(APP_URL)
buf = BytesIO()
qr.save(buf, format="PNG")
st.image(buf.getvalue(), width=220)
st.caption(APP_URL)

st.markdown("---")
st.subheader("✅ Take the Quiz")

answers = []
for i, (q, options) in enumerate(QUESTIONS):
    choice = st.radio(f"Q{i+1}. {q}", ["Choose one..."] + options, index=0, key=f"q{i}")
    if choice == "Choose one...":
        answers.append(None)
    else:
        answers.append(options.index(choice))  # 0/1/2

st.markdown("---")

if st.button("🎯 Calculate My Style"):
    if any(a is None for a in answers):
        st.warning("Please answer all questions!")
    else:
        score = calc_risk_score(answers)
        t = investor_type(score)
        portfolio = portfolio_for(t)
        tip = tip_for(t)

        st.success("Here are your results 👇")
        st.subheader("Investor Type")
        st.write(t)

        st.subheader("Risk Bar")
        st.write(f"Risk Score: **{score}/100**")
        draw_risk_bar(score)

        st.subheader("Portfolio Pie Chart")
        draw_portfolio_pie(portfolio)

        st.subheader("One Tip")
        st.info(tip)

