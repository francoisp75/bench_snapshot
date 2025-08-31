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

# Highlight Orange
df["label"] = [
    f"<span style='color:orange'>{r}. {op}</span>" if op == "Orange"
    else f"{r}. {op}"
    for r, op in zip(df["rank"], df["operator"])
]

# Flèches croissance
df["growth_arrow"] = ["↑" if val > 0 else "↓" for val in df["growth"]]
df["growth_color"] = ["green" if val > 0 else "red" for val in df["growth"]]
df["growth_text"] = [f"{val:+.1f}%" for val in df["growth"]]

# === Layout Streamlit ===
st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align:center;'>Global Top13</h1>", unsafe_allow_html=True)

# === Graphique combiné ===
colors = ["orange" if op == "Orange" else "lightgray" for op in df["operator"]]

fig = go.Figure()

# Barres CA
fig.add_trace(go.Bar(
    y=df["label"],
    x=df["revenue"],
    orientation="h",
    marker=dict(color=colors),
    text=None,
    cliponaxis=False,
    hovertemplate="%{y}<br>Chiffre d’affaires: %{x} Mds €<extra></extra>"
))

# Placement automatique du chiffre CA à droite de la barre
for y, x, val, op in zip(df["label"], df["revenue"], df["revenue"], df["operator"]):
    fig.add_annotation(
        x=x + max(1, 0.02*x),  # petit décalage proportionnel
        y=y,
        text=f"{val:.1f}",      # juste le chiffre, plus Mds €
        font=dict(color="black" if op != "Orange" else "orange", size=12),
        showarrow=False,
        align="left"
    )

# Flèches + croissance à droite du chiffre CA
for y, x, arrow, pct, color in zip(df["label"], df["revenue"], df["growth_arrow"], df["growth_text"], df["growth_color"]):
    fig.add_annotation(
        x=x + max(6, 0.08*x),  # décalage proportionnel
        y=y,
        text=f"<b>{arrow} {pct}</b>",
        font=dict(color=color, size=12, family="Arial Black"),
        showarrow=False,
        align="left"
    )

fig.update_layout(
    title=dict(
        text="Chiffre d’affaires (Mds€) et Taux de croissance S1 2025",
        x=0.5, xanchor="center"
    ),
    yaxis=dict(
        autorange="reversed",
        categoryorder="array",
        categoryarray=df["label"]
    ),
    xaxis=dict(visible=False),
    bargap=0.5,
    margin=dict(l=120, r=150, t=60, b=40),
    height=650
)

st.plotly_chart(fig, use_container_width=True)
