import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Données
data_growth = {
    "operator": ["Digi", "KPN", "Iliad", "Elisa", "TIM", "TEF", "DT", "BT", "ORA", "VOD"],
    "growth_pct": [17.5, 4.4, 3.6, 3.0, 1.6, 0.2, 0.1, -2.0, -2.1, -2.6],
    "total_rev_bn": [1.1, 2.9, 5.0, 1.1, 4.5, 10.5, 18.7, 11.8, 13.5, 12.4],
}

df = pd.DataFrame(data_growth)

# Couleurs : orange pour ORA, gris clair pour les autres
df["color"] = df["operator"].apply(lambda x: "orange" if x == "ORA" else "lightgray")

# Création du bar chart
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=df["operator"],
        y=df["growth_pct"],
        marker_color=df["color"],
        text=[f"{val:.1f}%" for val in df["growth_pct"]],
        textposition="outside",
        textfont=dict(color="black", size=13, family="Arial Black"),  # % en gras noir
        hovertemplate="<b>%{x}</b><br>Growth: %{y:.1f}%<extra></extra>",
    )
)

# Ajouter les boîtes en dessous
for i, row in df.iterrows():
    fig.add_annotation(
        x=row["operator"],
        y=-7,  # un peu plus bas pour laisser respirer
        text=f"<b>{row['total_rev_bn']} Bn€</b>",
        showarrow=False,
        font=dict(size=11, color="white" if row["operator"] == "ORA" else "black"),
        align="center",
        bgcolor=row["color"],
        borderpad=4
    )

# Mise en forme
fig.update_layout(
    title=dict(
        text="Europe geographic  TOTAL revenue growth in 1H 2025<br>(organic, YoY evolution)",
        x=0.5,   # centré horizontalement
        y=0.95,  # bien en haut
        xanchor="center",
        yanchor="top",
        font=dict(size=16, family="Arial", color="black")
    ),
    xaxis=dict(
        tickfont=dict(size=11, color="black"),
        tickvals=df["operator"],
        ticktext=[f"<b>{op}</b>" for op in df["operator"]],  # noms en gras noir
    ),
    yaxis=dict(
        visible=False,
        range=[-10, max(df["growth_pct"]) + 5]  # ajuste l’échelle pour lisibilité
    ),
    plot_bgcolor="white",
    margin=dict(t=120, b=100),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)
