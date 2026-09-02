import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Titre de la page
st.set_page_config(page_title="Europe Revenue Growth", layout="wide")
st.title("Europe Geographic TOTAL Revenue Growth in 1H 2026")
st.write("Organic, YoY evolution")

# Données
data_growth = {
    "operator": ["Digi", "Iliad", "DT", "ORA", "KPN", "TIM", "BT", "VOD", "ELISA", "TEF","SFR"],
    "growth_pct": [10.6, 3.4, 2.3, 1.0, 0.7, 0.2, -0.1, -0.7, -0.8, -2.3,-8.9],
    "total_rev_bn": [1.2, 5.2, 19.1, 14.2, 2.9, 4.6, 10.0, 13.6, 1.1, 10.2,4.1],
}
df = pd.DataFrame(data_growth)

# Couleurs dynamiques : orange pour ORA, gris sinon
def set_color(row):
    if row["operator"] == "ORA":
        return "orange"
    else:
        return "lightgray"

df["color"] = df.apply(set_color, axis=1)

# Création du bar chart
fig = go.Figure()
fig.add_trace(
    go.Bar(
        x=df["operator"],
        y=df["growth_pct"],
        marker_color=df["color"],
        text=[f"{val:.1f}%" for val in df["growth_pct"]],
        textposition="outside",
        textfont=dict(color="black", size=10, family="Arial Black"),
        customdata=df["total_rev_bn"],
        hovertemplate="<b>%{x}</b><br>Growth: %{y:.1f}%<br>Revenue: %{customdata} Bn€<extra></extra>",
    )
)

# Position verticale des boîtes sous les barres
y_box = min(df["growth_pct"]) - 3

# Ajouter les boîtes avec chiffres
for i, row in df.iterrows():
    fig.add_annotation(
        x=row["operator"],
        y=y_box,
        text=f"<b>{row['total_rev_bn']}</b>",
        showarrow=False,
        font=dict(size=11, color="white" if row["operator"] == "ORA" else "black"),
        align="center",
        bgcolor=row["color"],
        borderpad=4
    )

# Ajouter le texte "Bn€" à gauche de la ligne
fig.add_annotation(
    x=-0.6,
    y=y_box,
    text="<b>Bn€</b>",
    showarrow=False,
    font=dict(size=11, color="black"),
    align="right",
    xref="x",
    yref="y"
)

# Mise en forme
fig.update_layout(
    xaxis=dict(
        tickfont=dict(size=11, color="black"),
        tickvals=df["operator"],
        ticktext=[f"<b>{op}</b>" for op in df["operator"]],
        tickangle=-45
    ),
    yaxis=dict(
        visible=False,
        range=[-10, max(df["growth_pct"]) + 5]
    ),
    plot_bgcolor="white",
    margin=dict(t=120, b=120),
    showlegend=False
)

# Affichage Streamlit
st.plotly_chart(fig, use_container_width=True)
