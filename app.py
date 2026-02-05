import streamlit as st
import plotly.graph_objects as go

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="AI Investor Style Quiz",
    layout="centered"
)

# --------------------------------------------------
# GLOBAL CSS – FORCE WHITE BACKGROUND + BLACK TEXT
# --------------------------------------------------
st.markdown(
    """
    <style>
    html, body, [class*="stApp"] {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    h1, h2, h3, h4, h5, h6, p, span, label {
        color: #000000 !important;
    }

    /* Radio buttons & text */
    div[role="radiogroup"] label {
        color: #000000 !important;
    }

    /* Buttons */
    button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #000000 !important;
        border-radius: 8px !important;
    }

    button:hover {
        background-color: #f2f2f2 !important;
        color: #000000 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------
st.title("💡 AI Investor Style Quiz")
st.caption("Educational demo only — not financial advice.")

# --------------------------------------------------
# SAMPLE RESULT (for demo)
# --------------------------------------------------
risk_score = 15

# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------
st.header("📊 Your Dashboard")

# --------------------
# Risk Gauge (Donut)
# --------------------
gauge_fig = go.Figure(
    go.Pie(
        values=[risk_score, 100 - risk_score],
        hole=0.7,
        marker=dict(colors=["#4F6BED", "#E5E7EB"]),
        textinfo="none"
    )
)

gauge_fig.update_layout(
    showlegend=False,
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(color="black"),
    annotations=[
        dict(
            text=f"<b>{risk_score}/100</b>",
            x=0.5,
            y=0.5,
            font_size=28,
            showarrow=False,
            font_color="black"
        )
    ],
    margin=dict(t=20, b=20, l=20, r=20)
)

st.plotly_chart(gauge_fig, use_container_width=True)

# --------------------
# Portfolio Allocation
# --------------------
alloc_fig = go.Figure(
    go.Pie(
        labels=["Stocks (Index)", "Bonds", "Cash"],
        values=[70, 20, 10],
        hole=0.6,
        marker=dict(colors=["#636EFA", "#EF553B", "#00CC96"])
    )
)

alloc_fig.update_layout(
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(color="black"),
    margin=dict(t=20, b=20, l=20, r=20)
)

st.plotly_chart(alloc_fig, use_container_width=True)

# --------------------
# Answer Impact Chart
# --------------------
st.subheader("📈 Answer Impact (Explainable)")

impact_fig = go.Figure(
    go.Bar(
        x=[60, 100, 55, 95, 80],
        y=[
            "Q1: Loss reaction",
            "Q2: Extra money",
            "Q3: Price change",
            "Q4: Checking frequency",
            "Q5: Risk goal"
        ],
        orientation="h",
        marker_color="#4F6BED"
    )
)

impact_fig.update_layout(
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(color="black"),
    xaxis=dict(
        title="Contribution (0–100)",
        color="black"
    ),
    yaxis=dict(color="black"),
    margin=dict(t=20, b=20, l=80, r=20)
)

st.plotly_chart(impact_fig, use_container_width=True)

# --------------------------------------------------
# RESET BUTTON
# --------------------------------------------------
st.markdown("---")
st.button("🔄 Reset for next person")

st.caption("© Demo project for AI Fair — Casey")
