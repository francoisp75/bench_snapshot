import pandas as pd
import plotly.graph_objects as go

# Données
data_growth = {
    "operator": ["Digi", "KPN", "Iliad", "Elisa", "TIM", "TEF", "DT", "BT", "ORA", "VOD"],
    "growth_pct": [17.5, 4.4, 3.6, 3.0, 1.6, 0.2, 0.1, -2.0, -2.1, -2.6],
    "total_rev_bn": [1.1, 2.9, 5.0, 1.1, 4.5, 10.5, 18.7, 11.8, 13.5, 12.4],
}
df = pd.DataFrame(data_growth)

# Couleurs dynamiques : orange pour ORA, rouge clair si négatif, gris sinon
def set_color(row):
    if row["operator"] == "ORA":
        return "orange"
    #elif row["growth_pct"] < 0:
        #return "lightcoral"
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

# Ajouter les boîtes (uniquement chiffres)
for i, row in df.iterrows():
    fig.add_annotation(
        x=row["operator"],
        y=y_box,
        text=f"<b>{row['total_rev_bn']}</b>",   # <-- uniquement la valeur
        showarrow=False,
        font=dict(size=11, color="white" if row["operator"] == "ORA" else "black"),
        align="center",
        bgcolor=row["color"],
        borderpad=4
    )

# Ajouter le texte "Bn€" à gauche de la ligne (une seule fois)
fig.add_annotation(
    x=-0.6,  # position légèrement à gauche du 1er opérateur
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
    title=dict(
        text="Europe geographic  TOTAL revenue growth in 1H 2025<br>(organic, YoY evolution)",
        x=0.5,
        y=0.95,
        xanchor="center",
        yanchor="top",
        font=dict(size=16, family="Arial", color="black")
    ),
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

# Pour Streamlit
# st.plotly_chart(fig, use_container_width=True)

fig.show()
