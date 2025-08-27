import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Visualisation KPI - Operating Cash Flow / Revenue (2Q25)")

# Charger les données
df = pd.read_excel("data/Bench_Viz.xlsx")

# Nettoyage colonnes
df.columns = df.columns.str.strip()
df["kpi"] = df["kpi"].astype(str).str.strip()
df["operator"] = df["operator"].astype(str).str.strip()

# Liste des opérateurs avant filtrage
all_operators = sorted(df["operator"].dropna().unique().tolist())

# Sélecteur d'opérateurs
selected_operators = st.multiselect(
    "Sélectionnez les opérateurs à afficher :",
    options=all_operators,
    default=all_operators
)

# Filtrer uniquement OPCF
df = df[df["kpi"].str.lower() == "operating cash flow / revenue"].copy()

# Nettoyage des valeurs % de la colonne 2Q25
df["2Q25"] = (
    df["2Q25"].astype(str)
    .str.replace('%', '', regex=False)
    .str.replace(',', '.', regex=False)
    .str.strip()
)
df["2Q25"] = pd.to_numeric(df["2Q25"], errors='coerce')

# Convertir en pourcentage si < 1
if df["2Q25"].max() <= 1.0:
    df["2Q25"] *= 100

df = df.dropna(subset=["2Q25"])

# Filtrer selon les opérateurs sélectionnés
df = df[df["operator"].isin(selected_operators)]

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
    "Elisa": "yellow"
}

# Préparer les données pour le graphe
df["x"] = "OPCF"
df["label"] = df.apply(lambda row: f"{row['operator']}<br>{row['2Q25']:.1f}%", axis=1)
df["color"] = df["operator"].map(operator_colors).fillna("gray")

# Affichage graphique
fig = px.scatter(
    df,
    x="x",
    y="2Q25",
    color="operator",
    color_discrete_map=operator_colors,
    height=650,
    width=100
)

fig.update_traces(marker=dict(size=14), textposition="top center")
fig.update_layout(
    title="Taux OPCF (2Q25) par opérateur",
    xaxis=dict(showticklabels=False, title=""),
    yaxis=dict(range=[0, 60], title="Taux (%)", gridcolor='lightgray'),
    plot_bgcolor="white"
)

st.plotly_chart(fig, use_container_width=True)
