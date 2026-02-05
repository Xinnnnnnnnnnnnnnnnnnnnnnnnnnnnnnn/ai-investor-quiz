import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="AI Investor Style Quiz",
    page_icon="💡",
    layout="centered",
)

# -----------------------------
# Global CSS (force white bg + black text, including buttons)
# -----------------------------
st.markdown(
    """
    <style>
    /* App background */
    .stApp {
        background-color: #ffffff !important;
        color: #111111 !important;
    }

    /* Main text */
    html, body, [class*="css"]  {
        color: #111111 !important;
    }

    /* Headers */
    h1, h2, h3, h4, h5, h6, p, li, span, label, div {
        color: #111111 !important;
    }

    /* Sidebar (if any) */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        color: #111111 !important;
    }

    /* Radio labels */
    div[role="radiogroup"] label {
        color: #111111 !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: #ffffff !important;
        color: #111111 !important;
        border: 1px solid #111111 !important;
        border-radius: 10px !important;
        padding: 0.5rem 0.9rem !important;
        font-weight: 600 !important;
    }
    .stButton > button:hover {
        background-color: #f3f3f3 !important;
        color: #111111 !important;
        border: 1px solid #111111 !important;
    }

    /* Checkbox label */
    .stCheckbox label {
        color: #111111 !important;
    }

    /* Fix markdown links */
    a { color: #1a73e8 !important; }

    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Plotly helpers (IMPORTANT: gauge cannot use update_xaxes/yaxes)
# -----------------------------
def apply_plotly_white_cartesian(fig: go.Figure) -> go.Figure:
    """For bar / line / scatter / pie (charts that may have axes)"""
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="#111111", size=14),
        title=dict(font=dict(color="#111111")),
        legend=dict(font=dict(color="#111111"), bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=40, r=40, t=60, b=40),
    )

    # Only apply axes updates if the figure has axes
    # (Pie technically doesn't need, but safe; it will just ignore)
    try:
        fig.update_xaxes(
            tickfont=dict(color="#111111"),
            titlefont=dict(color="#111111"),
            gridcolor="#eaeaea",
            zerolinecolor="#eaeaea",
        )
        fig.update_yaxes(
            tickfont=dict(color="#111111"),
            titlefont=dict(color="#111111"),
            gridcolor="#eaeaea",
            zerolinecolor="#eaeaea",
        )
    except Exception:
        pass

    return fig


def apply_plotly_white_gauge(fig: go.Figure) -> go.Figure:
    """For indicator / gauge charts (NO x/y axes)"""
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="white",
        font=dict(color="#111111"),
        margin=dict(l=40, r=40, t=40, b=40),
    )
    return fig


# -----------------------------
# Session state init
# -----------------------------
if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "answers" not in st.session_state:
    st.session_state.answers = {}

# -----------------------------
# App title
# -----------------------------
st.title("💡 AI Investor Style Quiz")
st.caption("Educational demo only — not financial advice.")

st.subheader("📱 Take the Quiz")
st.write("Answer 10 simple questions. You'll get a risk score, investor type, and a sample portfolio.")

# -----------------------------
# Question bank (simple version)
# Each option contributes points (0-10). Total mapped to 0-100.
# -----------------------------
QUESTIONS = [
    ("Q1. Your investment drops 20%. What do you do?",
     [("Sell to stop the loss", 0),
      ("Wait and see", 5),
      ("Buy more (if you believe in it)", 10)]),

    ("Q2. You prefer investments that are…",
     [("Very stable", 0),
      ("Some risk, some stability", 5),
      ("High growth potential", 10)]),

    ("Q3. How long can you hold an investment?",
     [("Less than 1 year", 0),
      ("1–3 years", 5),
      ("3+ years", 10)]),

    ("Q4. If the market is very volatile, you…",
     [("Feel stressed and avoid it", 0),
      ("Stay cautious", 5),
      ("Feel excited / see opportunity", 10)]),

    ("Q5. You get $1,000. What do you do?",
     [("Save it", 0),
      ("Save some, invest some", 5),
      ("Invest most", 10)]),

    ("Q6. Which sounds most like you?",
     [("Careful", 0),
      ("Balanced", 5),
      ("Bold", 10)]),

    ("Q7. How often would you check results?",
     [("Every day", 0),
      ("Sometimes", 5),
      ("Not often", 10)]),

    ("Q8. A friend says: “This will grow fast!” You…",
     [("Ignore it", 0),
      ("Research first", 5),
      ("Research and try", 10)]),

    ("Q9. If markets fall suddenly, you feel…",
     [("Scared", 0),
      ("Thoughtful", 5),
      ("Ready to act", 10)]),

    ("Q10. Your main goal is…",
     [("Protect money", 0),
      ("Grow slowly", 5),
      ("Grow a lot", 10)]),
]

# -----------------------------
# Render quiz
# -----------------------------
with st.form("quiz_form"):
    for q_text, options in QUESTIONS:
        labels = [x[0] for x in options]
        # default = first option placeholder not needed; keep stable
        choice = st.radio(q_text, labels, key=q_text)
        st.session_state.answers[q_text] = choice

    submitted = st.form_submit_button("✅ Submit")

# -----------------------------
# Scoring logic
# -----------------------------
def get_points(q_text: str, choice: str) -> int:
    for qt, opts in QUESTIONS:
        if qt == q_text:
            for label, pts in opts:
                if label == choice:
                    return pts
    return 0

def calc_risk_score(answers: dict) -> int:
    # Each question gives 0/5/10, total 0-100
    total = 0
    for q_text, choice in answers.items():
        total += get_points(q_text, choice)
    # total is already 0-100 because 10 questions * 10 max = 100
    return int(total)

def investor_type(score: int) -> str:
    if score <= 33:
        return "Conservative"
    elif score <= 66:
        return "Balanced"
    else:
        return "Growth"

def portfolio_by_type(inv_type: str):
    # Simple illustrative allocations
    if inv_type == "Conservative":
        return {"Bonds": 60, "Stocks (Index)": 25, "Cash": 15}
    if inv_type == "Balanced":
        return {"Bonds": 40, "Stocks (Index)": 40, "Cash": 20}
    return {"Bonds": 20, "Stocks (Index)": 70, "Cash": 10}

def build_contrib_df(answers: dict) -> pd.DataFrame:
    rows = []
    for i, (q_text, _) in enumerate(QUESTIONS, start=1):
        choice = answers.get(q_text, "")
        pts = get_points(q_text, choice)
        # convert to 0-100 contribution (0/50/100) for "explainable" bar
        contrib = int((pts / 10) * 100)
        rows.append({"Question": f"{i}", "Contribution": contrib, "Choice": choice})
    df = pd.DataFrame(rows)
    return df

# -----------------------------
# After submit: show dashboard
# -----------------------------
if submitted:
    st.session_state.submitted = True

if st.session_state.submitted:
    answers = st.session_state.answers
    risk_score = calc_risk_score(answers)
    inv_type = investor_type(risk_score)
    alloc = portfolio_by_type(inv_type)
    contrib_df = build_contrib_df(answers)

    st.divider()
    st.header("📊 Your Dashboard")
    st.write(f"**Investor Type:** {inv_type}")
    st.write(f"**Risk Score:** {risk_score}/100")

    # ---- Gauge (INDICATOR) ----
    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=risk_score,
            number={"font": {"color": "#111111", "size": 54}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#111111"},
                "bar": {"color": "#1f77b4"},
                "bgcolor": "white",
                "borderwidth": 1,
                "bordercolor": "#dddddd",
                "steps": [
                    {"range": [0, 33], "color": "#cfe2f3"},
                    {"range": [33, 66], "color": "#9fc5e8"},
                    {"range": [66, 100], "color": "#ea9999"},
                ],
            },
        )
    )
    gauge = apply_plotly_white_gauge(gauge)
    st.plotly_chart(gauge, use_container_width=True)

    # ---- Donut portfolio ----
    labels = list(alloc.keys())
    values = list(alloc.values())

    donut = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.6,
                textinfo="percent",
                textfont=dict(color="#111111", size=16),
            )
        ]
    )
    donut.update_layout(
        title="Sample Portfolio (Illustrative)",
        showlegend=True,
    )
    donut = apply_plotly_white_cartesian(donut)
    st.plotly_chart(donut, use_container_width=True)

    # ---- Answer Impact (Explainable) ----
    st.subheader("📈 Answer Impact (Explainable)")
    # show in descending order to make it more readable
    plot_df = contrib_df.sort_values("Contribution", ascending=True)

    bar = go.Figure(
        data=[
            go.Bar(
                x=plot_df["Contribution"],
                y=plot_df["Question"],
                orientation="h",
                text=plot_df["Contribution"].astype(str),
                textposition="outside",
                textfont=dict(color="#111111"),
            )
        ]
    )
    bar.update_layout(
        xaxis_title="Contribution (0–100)",
        yaxis_title="Question #",
        margin=dict(l=40, r=40, t=60, b=40),
    )
    bar = apply_plotly_white_cartesian(bar)
    st.plotly_chart(bar, use_container_width=True)

    # ---- AI Fair reset ----
    st.write("")
    col1, col2 = st.columns([1, 2])
