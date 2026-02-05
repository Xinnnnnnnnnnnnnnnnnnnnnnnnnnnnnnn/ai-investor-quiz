import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# -----------------------------
# Page + Global Style (White BG + Black Text)
# -----------------------------
st.set_page_config(
    page_title="AI Investor Style Quiz",
    page_icon="💡",
    layout="centered",
)

st.markdown(
    """
<style>
/* App background */
html, body, [data-testid="stAppViewContainer"]{
    background: #ffffff !important;
    color: #111111 !important;
}

/* Main text */
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] span,
label, .stRadio label, .stSelectbox label, .stTextInput label {
    color: #111111 !important;
}

/* Sidebar (if any) */
[data-testid="stSidebar"]{
    background: #ffffff !important;
    color: #111111 !important;
}

/* Buttons: force white bg + black text */
.stButton > button {
    background: #ffffff !important;
    color: #111111 !important;
    border: 1px solid #111111 !important;
    border-radius: 10px !important;
    padding: 0.6rem 1rem !important;
    font-weight: 600 !important;
}
.stButton > button:hover {
    background: #f2f2f2 !important;
    color: #111111 !important;
}

/* Inputs borders */
div[data-baseweb="select"] > div,
input, textarea {
    border: 1px solid #cccccc !important;
}

/* Remove dark leftovers */
[data-testid="stHeader"]{
    background: rgba(255,255,255,0) !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# -----------------------------
# Helpers: Force Plotly White + Black Fonts
# -----------------------------
def apply_plotly_white(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="#111111", size=14),
        title=dict(font=dict(color="#111111")),
        legend=dict(
            font=dict(color="#111111"),
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(0,0,0,0)",
        ),
        margin=dict(l=40, r=40, t=60, b=40),
    )
    fig.update_xaxes(
        color="#111111",
        tickfont=dict(color="#111111"),
        titlefont=dict(color="#111111"),
        gridcolor="#eaeaea",
        zerolinecolor="#eaeaea",
    )
    fig.update_yaxes(
        color="#111111",
        tickfont=dict(color="#111111"),
        titlefont=dict(color="#111111"),
        gridcolor="#eaeaea",
        zerolinecolor="#eaeaea",
    )
    return fig


# -----------------------------
# Quiz Data (10 Questions, each option has score)
# You can edit wording/options freely.
# -----------------------------
QUESTIONS = [
    {
        "id": 1,
        "question": "Q1. Your investment drops 20%. What do you do?",
        "options": [("Sell to stop the loss", 5), ("Wait and see", 10), ("Buy more (if plan is solid)", 15)],
    },
    {
        "id": 2,
        "question": "Q2. Your friend says: “This is a sure win!” You…",
        "options": [("Avoid it", 5), ("Research first", 10), ("Try a small amount", 15)],
    },
    {
        "id": 3,
        "question": "Q3. Which feels most comfortable?",
        "options": [("Stable and predictable", 5), ("Balanced growth", 10), ("High growth (accept swings)", 15)],
    },
    {
        "id": 4,
        "question": "Q4. How long do you want to hold an investment?",
        "options": [("Short-term", 15), ("Mid-term", 10), ("Long-term", 5)],
    },
    {
        "id": 5,
        "question": "Q5. You get $1,000. What do you do?",
        "options": [("Save it", 5), ("Save some, invest some", 10), ("Invest most", 15)],
    },
    {
        "id": 6,
        "question": "Q6. Which sounds most like you?",
        "options": [("Careful", 5), ("Balanced", 10), ("Bold", 15)],
    },
    {
        "id": 7,
        "question": "Q7. How often would you check results?",
        "options": [("Every day", 15), ("Sometimes", 10), ("Not often", 5)],
    },
    {
        "id": 8,
        "question": "Q8. Prices go up quickly. You…",
        "options": [("Feel FOMO and chase", 15), ("Stay calm and follow plan", 10), ("Take profit carefully", 5)],
    },
    {
        "id": 9,
        "question": "Q9. If markets fall suddenly, you feel…",
        "options": [("Scared", 5), ("Thoughtful", 10), ("Ready to act", 15)],
    },
    {
        "id": 10,
        "question": "Q10. Your main goal is…",
        "options": [("Protect money", 5), ("Grow slowly", 10), ("Grow a lot", 15)],
    },
]

# Score range: min 50, max 150 (10 questions * 5~15)
MIN_SCORE = 10 * 5
MAX_SCORE = 10 * 15

def normalize_to_0_100(raw_score: int) -> int:
    raw_score = max(MIN_SCORE, min(MAX_SCORE, raw_score))
    return round((raw_score - MIN_SCORE) / (MAX_SCORE - MIN_SCORE) * 100)

def allocation_from_risk(risk_0_100: int) -> dict:
    # Example mapping (edit as you like)
    if risk_0_100 <= 33:
        return {"Stocks (Index)": 30, "Bonds": 50, "Cash": 20}
    elif risk_0_100 <= 66:
        return {"Stocks (Index)": 55, "Bonds": 35, "Cash": 10}
    else:
        return {"Stocks (Index)": 70, "Bonds": 20, "Cash": 10}

def investor_type_from_risk(risk_0_100: int) -> str:
    if risk_0_100 <= 33:
        return "Conservative"
    elif risk_0_100 <= 66:
        return "Balanced"
    else:
        return "Growth"

# -----------------------------
# Session State
# -----------------------------
if "answers" not in st.session_state:
    st.session_state.answers = {}  # {qid: (label, score)}

if "submitted" not in st.session_state:
    st.session_state.submitted = False

# -----------------------------
# UI
# -----------------------------
st.title("💡 AI Investor Style Quiz")
st.caption("Educational demo only — not financial advice.")

# AI Fair mode reset
col_a, col_b = st.columns([1, 1])
with col_a:
    if st.button("🔄 Reset for next person"):
        st.session_state.answers = {}
        st.session_state.submitted = False
        st.rerun()
with col_b:
    st.markdown("AI Fair mode: Reset after each user ✅")

st.divider()
st.header("✅ Take the Quiz")

# Render questions
for q in QUESTIONS:
    qid = q["id"]
    labels = [opt[0] for opt in q["options"]]
    label_to_score = {opt[0]: opt[1] for opt in q["options"]}

    default_index = 0
    if qid in st.session_state.answers:
        prev_label = st.session_state.answers[qid][0]
        if prev_label in labels:
            default_index = labels.index(prev_label)

    choice = st.radio(
        q["question"],
        options=labels,
        index=default_index,
        key=f"q_{qid}",
    )

    st.session_state.answers[qid] = (choice, label_to_score[choice])

st.divider()

# Submit
if st.button("✅ Submit"):
    st.session_state.submitted = True

# -----------------------------
# Results Dashboard
# -----------------------------
if st.session_state.submitted:
    # Compute scores
    raw_total = sum(v[1] for v in st.session_state.answers.values())
    risk_score = normalize_to_0_100(raw_total)
    inv_type = investor_type_from_risk(risk_score)
    alloc = allocation_from_risk(risk_score)

    st.header("📊 Your Dashboard")
    st.write(f"**Investor Type:** {inv_type}")
    st.write(f"**Risk Score:** {risk_score}/100")

    # 1) Gauge (Risk Score)
    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=risk_score,
            number={"font": {"color": "#111111", "size": 48}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#111111"},
                "bar": {"color": "#1f77b4"},
                "bgcolor": "white",
                "borderwidth": 1,
                "bordercolor": "#cccccc",
                "steps": [
                    {"range": [0, 33], "color": "#d9edf7"},
                    {"range": [33, 66], "color": "#bcdff5"},
                    {"range": [66, 100], "color": "#f8d7da"},
                ],
                "threshold": {
                    "line": {"color": "#111111", "width": 6},
                    "thickness": 0.75,
                    "value": risk_score,
                },
            },
        )
    )
    gauge.update_layout(height=420)
    gauge = apply_plotly_white(gauge)
    st.plotly_chart(gauge, use_container_width=True)

    # 2) Donut (Allocation)
    alloc_labels = list(alloc.keys())
    alloc_values = list(alloc.values())
    donut = px.pie(
        names=alloc_labels,
        values=alloc_values,
        hole=0.60,
    )
    donut.update_traces(
        textposition="inside",
        textfont=dict(color="#111111", size=16),
    )
    donut.update_layout(
        title="Suggested Sample Allocation (Demo)",
        showlegend=True,
    )
    donut = apply_plotly_white(donut)
    st.plotly_chart(donut, use_container_width=True)

    # 3) Answer Impact (Explainable) — per question contribution (0-100 scale)
    # Convert each selected option score -> 0~100 impact
    contrib = []
    for q in QUESTIONS:
        qid = q["id"]
        picked_score = st.session_state.answers[qid][1]
        impact_0_100 = round((picked_score - 5) / (15 - 5) * 100)
        contrib.append({"Question": f"{qid}", "Impact": impact_0_100})

    df = contrib
    bar = px.bar(
        df,
        x="Impact",
        y="Question",
        orientation="h",
        title="Answer Impact (Explainable)",
        range_x=[0, 100],
    )
    bar.update_layout(
        xaxis_title="Contribution (0–100)",
        yaxis_title="Question",
    )
    bar.update_traces(marker_line_width=0)
    bar = apply_plotly_white(bar)
    st.plotly_chart(bar, use_container_width=True)

    st.caption("© Demo project for AI Fair — Casey")
