import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# === Données ===
data = {
    "operator": [
        "China Mobile", "Verizon", "Deutsche Telekom", "AT&T", "NTT",
        "Comcast", "China Telecom", "China Unicom", "América Móvil",
        "SoftBank", "Orange", "Vodafone", "KDDI"
    ],
    "revenue": [68.6, 62.3, 58.4, 56.3, 42.7, 37.1, 34.3, 25.3, 21.4, 20.9, 19.9, 18.7, 18.5],
    "growth": [-0.5, 3.4, 3.9, 2.8, 0.3, -0.4, 1.3, 1.4, 9.8, 9.1, 0.3, 3.4, 3.9],
}

df = pd.DataFrame(data)
df["rank"] = range(1, len(df) + 1)

# Ranking : seul Orange en orange
df["label"] = [
    f"<span style='color:orange'>{r}.</span> <span style='color:orange'>{op}</span>" if op == "Orange"
    else f"{r}. {op}"
    for r, op in zip(df["rank"], df["operator"])
]

# === Layout Streamlit ===
st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align:center;'>Global Top13</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

# === Graphique CA ===
with col1:
    colors = ["orange" if op == "Orange" else "lightgray" for op in df["operator"]]
    text_colors = ["orange" if op == "Orange" else "black" for op in df["operator"]]

    fig_revenue = go.Figure(go.Bar(
        y=df["label"],
        x=df["revenue"],
        orientation="h",
        marker=dict(color=colors),
        text=[f"{val} Mds €" for val in df["revenue"]],
        textposition="outside",
        textfont=dict(color=text_colors),
        cliponaxis=False  # éviter que le texte soit coupé
    ))
    fig_revenue.update_layout(
        title=dict(text="Chiffre d’affaires en Mds € au 1S 2025", x=0.5),
        yaxis=dict(autorange="reversed"),
        xaxis=dict(visible=False),
        width=600,   # largeur réduite
        height=700,
        margin=dict(l=120, r=50, t=80, b=40),  # marges pour laisser place aux étiquettes
        uniformtext_minsize=10
    )
    st.plotly_chart(fig_revenue, use_container_width=False)

# === Graphique Croissance ===
with col2:
    colors_growth = ["lightgreen" if val >= 0 else "red" for val in df["growth"]]
    fig_growth = go.Figure(go.Bar(
        y=df["label"],
        x=df["growth"],
        orientation="h",
        marker=dict(color=colors_growth),
        text=[f"{val} %" for val in df["growth"]],
        textposition="outside",
        cliponaxis=False
    ))
    fig_growth.update_layout(
        title=dict(text="Taux de croissance organique", x=0.5),
        yaxis=dict(autorange="reversed", showticklabels=False),
        xaxis=dict(visible=False),
        width=400,   # largeur plus compacte
        height=700,
        margin=dict(l=40, r=80, t=80, b=40),
        uniformtext_minsize=10
    )
    st.plotly_chart(fig_growth, use_container_width=False)
