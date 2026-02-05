import streamlit as st
import plotly.graph_objects as go

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="AI Investor Style Quiz",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# GLOBAL CSS — FORCE WHITE BACKGROUND + BLACK TEXT
# --------------------------------------------------
st.markdown(
    """
    <style>
    /* App background */
    html, body, [class*="stApp"] {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    /* Text */
    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: #000000 !important;
    }

    /* Make sure Streamlit markdown text is visible */
    .stMarkdown, .stMarkdown p, .stMarkdown span {
        color: #000000 !important;
    }

    /* Radio group label text */
    div[role="radiogroup"] label {
        color: #000000 !important;
    }

    /* Inputs */
    input, textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #000000 !important;
    }

    /* Buttons */
    button[kind="primary"], button[kind="secondary"], button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #000000 !important;
        border-radius: 10px !important;
        padding: 0.6rem 1rem !important;
        font-weight: 600 !important;
    }

    button:hover {
        background-color: #f2f2f2 !important;
        color: #000000 !important;
    }

    /* Reduce top padding a bit (looks more "product") */
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 2rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# PLOTLY THEME HELPER — FORCE WHITE BG + BLACK FONT
# --------------------------------------------------
def apply_plotly_white_theme(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="black"),
        title_font=dict(color="black"),
        legend=dict(font=dict(color="black")),
        margin=dict(t=30, b=30, l=30, r=30),
    )
    fig.update_xaxes(
        color="black",
        title_font=dict(color="black"),
        tickfont=dict(color="black"),
        gridcolor="#E5E7EB",
        zerolinecolor="#E5E7EB",
    )
    fig.update_yaxes(
        color="black",
        title_font=dict(color="black"),
        tickfont=dict(color="black"),
        gridcolor="#E5E7EB",
        zerolinecolor="#E5E7EB",
    )
    return fig

# --------------------------------------------------
# STATE INIT
# --------------------------------------------------
if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "answers" not in st.session_state:
    st.session_state.answers = {}

# --------------------------------------------------
# TITLE
# --------------------------------------------------
st.title("💡 AI Investor Style Quiz")
st.caption("Educational demo only — not financial advice.")

# --------------------------------------------------
# QUESTIONS (簡化版示範，可自行改題目/選項/分數)
# 每題三選一：0 / 5 / 10 分
# --------------------------------------------------
QUESTIONS = [
    ("Q1. Your investment drops 20%. What do you do?",
     ["Sell to stop the loss", "Wait and see", "Buy more (long-term view)"], [0, 5, 10]),
    ("Q2. You see a stock going viral online. You...",
     ["Buy immediately", "Read a little then buy", "Research first (risk/valuation)"], [0, 5, 10]),
    ("Q3. You prefer returns that are...",
     ["Stable and low", "Balanced", "High even if volatile"], [0, 5, 10]),
    ("Q4. If prices go up fast, you feel...",
     ["FOMO (must buy now)", "Curious", "Cautious"], [0, 5, 10]),
    ("Q5. You get $1,000. What do you do?",
     ["Save it", "Save some, invest some", "Invest most"], [0, 5, 10]),
    ("Q6. Which sounds most like you?",
     ["Careful", "Balanced", "Bold"], [0, 5, 10]),
    ("Q7. How often would you check results?",
     ["Every day", "Sometimes", "Not often"], [0, 5, 10]),
    ("Q8. A friend says: “This will grow fast!” You...",
     ["Ignore it", "Research first", "Research and try"], [0, 5, 10]),
    ("Q9. If markets fall suddenly, you feel...",
     ["Scared", "Thoughtful", "Ready to act"], [0, 5, 10]),
    ("Q10. Your main goal is...",
     ["Protect money", "Grow slowly", "Grow a lot"], [0, 5, 10]),
]

# --------------------------------------------------
# QUIZ UI
# --------------------------------------------------
st.subheader("✅ Take the Quiz")

for idx, (q, options, scores) in enumerate(QUESTIONS, start=1):
    key = f"q{idx}"
    default_idx = 0
    if key in st.session_state.answers:
        # find selected option index
        try:
            default_idx = options.index(st.session_state.answers[key])
        except ValueError:
            default_idx = 0

    choice = st.radio(q, options, index=default_idx, key=key)

    st.session_state.answers[key] = choice

# --------------------------------------------------
# SUBMIT
# --------------------------------------------------
submit_col1, submit_col2 = st.columns([1, 2])

with submit_col1:
    submitted = st.button("✅ Submit")

with submit_col2:
    st.caption("AI Fair mode: show results instantly after submit.")

if submitted:
    st.session_state.submitted = True

# --------------------------------------------------
# CALCULATE + DASHBOARD
# --------------------------------------------------
if st.session_state.submitted:
    # Calculate risk_score (0-100)
    total = 0
    contributions = []
    labels = []

    for idx, (q, options, scores) in enumerate(QUESTIONS, start=1):
        key = f"q{idx}"
        ans = st.session_state.answers.get(key, options[0])
        s = scores[options.index(ans)]
        total += s
        contributions.append(int((s / 10) * 100))  # per-question contribution (0/50/100)
        labels.append(f"Q{idx}")

    # total max = 10 questions * 10 = 100
    risk_score = total

    st.markdown("---")
    st.header("📊 Your Dashboard")

    # --------------------
    # Risk Gauge (Donut)
    # --------------------
    gauge_fig = go.Figure(
        go.Pie(
            values=[risk_score, 100 - risk_score],
            hole=0.72,
            marker=dict(colors=["#4F6BED", "#E5E7EB"]),
            textinfo="none"
        )
    )
    gauge_fig.update_layout(
        showlegend=False,
        annotations=[
            dict(
                text=f"<b>{risk_score}/100</b>",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=30, color="black")
            )
        ],
    )
    gauge_fig = apply_plotly_white_theme(gauge_fig)
    st.plotly_chart(gauge_fig, use_container_width=True)

    # --------------------
    # Portfolio Allocation (simple mapping demo)
    # --------------------
    # Low score => more bonds/cash; high score => more stocks
    stocks = min(85, max(30, risk_score))
    bonds = min(60, max(10, 100 - risk_score))
    cash = 100 - stocks - bonds
    if cash < 0:
        cash = 0
        bonds = 100 - stocks

    alloc_fig = go.Figure(
        go.Pie(
            labels=["Stocks (Index)", "Bonds", "Cash"],
            values=[stocks, bonds, cash],
            hole=0.6,
            marker=dict(colors=["#636EFA", "#EF553B", "#00CC96"])
        )
    )
    alloc_fig = apply_plotly_white_theme(alloc_fig)
    st.plotly_chart(alloc_fig, use_container_width=True)

    # --------------------
    # Answer Impact (Explainable)
    # --------------------
    st.subheader("📈 Answer Impact (Explainable)")
    impact_fig = go.Figure(
        go.Bar(
            x=contributions,
            y=[f"{labels[i]}: {QUESTIONS[i][0].split('.')[1].strip()}" for i in range(len(labels))],
            orientation="h",
            marker_color="#4F6BED"
        )
    )
    impact_fig.update_layout(
        xaxis=dict(title="Contribution (0–100)"),
        yaxis=dict(title="")
    )
    impact_fig = apply_plotly_white_theme(impact_fig)
    st.plotly_chart(impact_fig, use_container_width=True)

    # --------------------------------------------------
    # RESET
    # --------------------------------------------------
    st.markdown("---")
    reset_clicked = st.button("🔄 Reset for next person")

    if reset_clicked:
        st.session_state.submitted = False
        st.session_state.answers = {}
        st.rerun()

    st.caption("© Demo project for AI Fair — Casey")
