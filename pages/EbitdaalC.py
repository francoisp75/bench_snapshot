import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Visualisation KPI - EBITDAaL rate LTM (2Q25)")

# Charger les données
df = pd.read_excel("data/Bench_Viz.xlsx")

# Nettoyage colonnes
df.columns = df.columns.str.strip()
df["kpi"] = df["kpi"].astype(str).str.strip()
df["operator"] = df["operator"].astype(str).str.strip()

# Filtrer uniquement EBITDAaL rate
df = df[df["kpi"].str.lower() == "ebitdaal rate"].copy()

# Nettoyage des colonnes 2Q25 et 2Q24
for col in ["2Q25", "2Q24"]:
    df[col] = (
        df[col].astype(str)
        .str.replace("%", "", regex=False)
        .str.replace(",", ".", regex=False)
        .str.strip()
    )
    df[col] = pd.to_numeric(df[col], errors="coerce")
    if df[col].max() <= 1.0:
        df[col] *= 100

df = df.dropna(subset=["2Q25", "2Q24"])

# Calcul variation en points
df["variation_pt"] = df["2Q25"] - df["2Q24"]

# Couleurs fixes pour chaque opérateur
operator_colors = {
    "DT": "deeppink",
    "VOD": "red",
    "TEF": "darkblue",
    "ORA": "orange",
    "BT": "purple",
    "TI": "deepskyblue",
    "KPN": "darkgreen",
    "Iliad": "black",
    "Digi": "gray",
    "Elisa": "yellow",
}

# Sélecteur d'opérateurs pour afficher les points
operators = df["operator"].dropna().unique().tolist()
selected_operators = st.multiselect(
    "Sélectionnez les opérateurs à afficher :",
    options=operators,
    default=operators,
)
df = df[df["operator"].isin(selected_operators)]

# Sélecteur d'opérateurs pour afficher les labels
label_operators = st.multiselect(
    "Sélectionnez les opérateurs pour afficher le label à droite :",
    options=selected_operators,
    default=[],
)

# Tri des opérateurs pour la légende (du plus haut au plus bas)
df = df.sort_values("2Q25", ascending=False)
ordered_operators = df["operator"].unique().tolist()

# Texte pour hover
def make_hover(row):
    color = "green" if row["variation_pt"] > 0 else ("red" if row["variation_pt"] < 0 else "black")
    return (
        f"<b>{row['operator']}</b><br>"
        f"Taux 2Q25 : {row['2Q25']:.1f}%<br>"
        f"Variation : <span style='color:{color}'>{row['variation_pt']:+.1f} pt</span>"
    )
df["hover_text"] = df.apply(make_hover, axis=1)
df["x"] = "EBITDAaL"

# Création du graphique
fig = px.scatter(
    df,
    x="x",
    y="2Q25",
    color="operator",
    category_orders={"operator": ordered_operators},
    color_discrete_map=operator_colors,
    height=650,
    width=100,
)

# Appliquer hover
for trace in fig.data:
    op = trace.name
    mask = df["operator"] == op
    trace.customdata = df.loc[mask, ["hover_text"]].values.tolist()
    trace.update(marker=dict(size=14), hovertemplate="%{customdata[0]}<extra></extra>")

# Ajouter labels à droite pour les opérateurs sélectionnés
for _, row in df[df["operator"].isin(label_operators)].iterrows():
    fig.add_annotation(
        x=0.12,  # position à droite du point
        y=row["2Q25"],
        xref="paper",
        yref="y",
        text=f"{row['operator']} {row['2Q25']:.1f}% ({row['variation_pt']:+.1f} pt)",
        showarrow=False,
        font=dict(color=operator_colors.get(row["operator"], "black"), size=12),
        align="left",
    )

fig.update_layout(
    title="Taux EBITDAaL LTM (2Q25) par opérateur",
    xaxis=dict(showticklabels=False, title=""),
    yaxis=dict(range=[20, 50], title="Taux (%)", gridcolor="lightgray"),
    plot_bgcolor="white",
    legend_title="Opérateur",
)

st.plotly_chart(fig, use_container_width=True)
