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
:root { --background-color: white !important; }

html, body, .stApp { background-color: white !important; color: black !important; }
[data-testid="stAppViewContainer"] { background-color: white !important; }
[data-testid="stHeader"] { background-color: white !important; }
[data-testid="stSidebar"] { background-color: white !important; }
h1, h2, h3, h4, h5, p, span, label, div { color: black !important; }
div[role="radiogroup"] label { color: black !important; }

div.stButton > button {
    background-color: white !important;
    color: black !important;
    border: 2px solid black !important;
    border-radius: 10px;
    font-size: 18px;
    padding: 10px 18px;
}

.plotly, .js-plotly-plot { background: white !important; }
section.main > div { background-color: white !important; }

/* 小徽章感 */
.badge {
    display: inline-block;
    border: 1.5px solid black;
    border-radius: 999px;
    padding: 6px 12px;
    font-weight: 600;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# QUESTIONS
# ===============================
questions = [
    ("Q1. If you lose money, what do you usually do?",
     ["Stop and avoid risk", "Wait and think", "Try again carefully"]),
    ("Q2. How long are you okay leaving money invested?",
     ["Less than 1 year", "2-3 years", "5+ years"]),
    ("Q3. Which feels safest to you?",
     ["Keep cash", "Mix safe + risky", "Mostly growth assets"]),
    ("Q4. When prices move up and down, you feel...",
     ["Nervous", "OK if I understand", "Calm or curious"]),
    ("Q5. You get $10,000...",
     ["Save it", "Save some, invest some", "Invest most"]),
    ("Q6. Which sounds most like you?",
     ["Careful", "Balanced", "Bold"]),
    ("Q7. How often would you check results?",
     ["Every day", "Sometimes", "Not often"]),
    ("Q8. A friend says “hot stock”, you...",
     ["Ignore it", "Research first", "Research & try"]),
    ("Q9. Markets fall suddenly. You feel...",
     ["Scared", "Thoughtful", "Ready to act"]),
    ("Q10. Your main goal is...",
     ["Protect money", "Grow slowly", "Grow a lot"]),
]
score_map = [0, 5, 10]
N = len(questions)

# ===============================
# SESSION STATE INIT
# ===============================
if "stage" not in st.session_state:
    st.session_state.stage = "intro"   # intro | quiz | result
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "answers" not in st.session_state:
    st.session_state.answers = [None] * N  # store chosen option index (0/1/2)

# ===============================
# HEADER
# ===============================
st.title("💡 AI Investor Style Quiz")
st.caption("Educational demo only — not financial advice.")
st.markdown('<div class="badge">🎪 AI Fair Mode</div>', unsafe_allow_html=True)
st.divider()

# ===============================
# HELPERS
# ===============================
def compute_score(answers_idx):
    # answers_idx: list of option indices (0/1/2)
    return sum(score_map[i] for i in answers_idx if i is not None)

def get_result(risk_score):
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
    return investor_type, description, allocation

def reset_all():
    st.session_state.stage = "intro"
    st.session_state.q_index = 0
    st.session_state.answers = [None] * N

# ===============================
# INTRO PAGE
# ===============================
if st.session_state.stage == "intro":
    st.header("👋 Welcome to AI Fair — Investor Style Challenge")

    st.write("""
**Goal:** Turn your behavior into an investor style (Conservative / Balanced / Aggressive).  
**How to play:**  
1) Tap **Start**  
2) Answer **one question per step**  
3) Hit **Next** to keep going (like a mini game)  
4) At the end, you’ll see your **Risk Score + Suggested Portfolio**
""")

    st.info("""
🎪 **AI Fair Note**  
This is a quick demo showing how AI-style logic can translate human choices into financial profiles.
""")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🚀 Start", use_container_width=True):
            st.session_state.stage = "quiz"
            st.session_state.q_index = 0
            st.experimental_rerun()
    with col2:
        if st.button("🧹 Clear (optional)", use_container_width=True):
            reset_all()
            st.experimental_rerun()

# ===============================
# QUIZ PAGE (ONE QUESTION PER STEP)
# ===============================
elif st.session_state.stage == "quiz":
    i = st.session_state.q_index
    q_text, opts = questions[i]

    # Progress UI
    progress = i / N  # 0.0 ~ 0.9
    st.markdown('<div class="badge">🎪 AI Fair Challenge</div>', unsafe_allow_html=True)
    st.write(f"### ✅ Question {i+1} / {N}")
    st.progress(progress)

    # Current answer default
    current = st.session_state.answers[i]
    if current is None:
        current = 1  # default middle option

    choice = st.radio(
        q_text,
        opts,
        index=current,
        key=f"radio_{i}"
    )

    # Save chosen index
    chosen_idx = opts.index(choice)
    st.session_state.answers[i] = chosen_idx

    # Navigation buttons
    c1, c2, c3 = st.columns([1, 1, 1])

    with c1:
        back_disabled = (i == 0)
        if st.button("⬅️ Back", disabled=back_disabled, use_container_width=True):
            st.session_state.q_index = max(0, i - 1)
            st.experimental_rerun()

    with c2:
        # Show current score for fun (optional, adds game feel)
        running_score = compute_score(st.session_state.answers)
        st.metric("Current Score", f"{running_score}")

    with c3:
        # Next or Finish
        if i < N - 1:
            if st.button("Next ➡️", use_container_width=True):
                st.session_state.q_index = i + 1
                st.experimental_rerun()
        else:
            if st.button("🏁 Submit & See Result", use_container_width=True):
                st.session_state.stage = "result"
                st.experimental_rerun()

# ===============================
# RESULT PAGE
# ===============================
else:
    answers_idx = st.session_state.answers

    # Safety: if somehow not all answered, fill missing with middle option
    answers_idx = [a if a is not None else 1 for a in answers_idx]
    risk_score = compute_score(answers_idx)

    investor_type, description, allocation = get_result(risk_score)

    st.markdown('<div class="badge">🎪 AI Fair Result</div>', unsafe_allow_html=True)
    st.header("📊 Your Result")
    st.subheader(f"Investor Type: {investor_type}")
    st.subheader(f"Risk Score: {risk_score}/100")

    st.write("### 🧠 Profile Summary")
    st.write(description)

    # Donut Chart
    fig = go.Figure(
        data=[
            go.Pie(
                labels=list(allocation.keys()),
                values=list(allocation.values()),
                hole=0.6,
                textinfo="percent"
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

    # AI Fair Summary Box
    st.write("### 🎯 AI Fair Quick Explanation")
    st.info(f"""
This user is classified as **{investor_type}**.

• Risk tolerance level is **{risk_score}/100**  
• Decision style: {description}  
• Suggested portfolio focuses on balance between growth and stability  

👉 This demo shows how AI can translate behavior into financial profiles.
""")

    st.divider()
    colA, colB = st.columns([1, 1])
    with colA:
        if st.button("🔄 Reset for next person", use_container_width=True):
            reset_all()
            st.experimental_rerun()
    with colB:
        # optional: allow replay without clearing intro
        if st.button("🎮 Play again", use_container_width=True):
            st.session_state.stage = "quiz"
            st.session_state.q_index = 0
            st.session_state.answers = [None] * N
            st.experimental_rerun()
