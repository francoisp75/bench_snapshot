import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Visualisation KPI - Capex / Revenue LTM (2Q25)")

# Charger les données
df = pd.read_excel("data/Bench_Viz.xlsx")

# Nettoyage colonnes
df.columns = df.columns.str.strip()
df["kpi"] = df["kpi"].astype(str).str.strip()
df["operator"] = df["operator"].astype(str).str.strip()

# Filtrer uniquement Capex / Revenue
df = df[df["kpi"].str.lower() == "capex / revenue"].copy()

# --- Nettoyage des colonnes 2Q25 et 2Q24 ---
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

# --- Calcul de la variation en points ---
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
    "Elisa": "yellow"
}

# Sélecteur d'opérateurs
operators = df["operator"].dropna().unique().tolist()
selected_operators = st.multiselect(
    "Sélectionnez les opérateurs à afficher :",
    options=operators,
    default=operators
)

df = df[df["operator"].isin(selected_operators)]

# --- Tri des opérateurs pour la légende (haut → bas) ---
df = df.sort_values("2Q25", ascending=False)
ordered_operators = df["operator"].unique().tolist()

# --- Texte pour hover ---
def make_hover(row):
    color = "green" if row["variation_pt"] > 0 else ("red" if row["variation_pt"] < 0 else "black")
    return (
        f"<b>{row['operator']}</b><br>"
        f"Taux 2Q25 : {row['2Q25']:.1f}%<br>"
        f"Variation : <span style='color:{color}'>{row['variation_pt']:+.1f} pt</span>"
    )

df["hover_text"] = df.apply(make_hover, axis=1)
df["x"] = "Capex / Revenue"

# --- Graphique ---
fig = px.scatter(
    df,
    x="x",
    y="2Q25",
    color="operator",
    category_orders={"operator": ordered_operators},
    color_discrete_map=operator_colors,
    height=650,
    width=100
)

# Associer tooltip point par point
for trace in fig.data:
    op = trace.name
    mask = df["operator"] == op
    trace.customdata = df.loc[mask, ["hover_text"]].values.tolist()
    trace.update(marker=dict(size=14), hovertemplate="%{customdata[0]}<extra></extra>")

fig.update_layout(
    title="Capex / Revenue LTM (2Q25) par opérateur",
    xaxis=dict(showticklabels=False, title=""),
    yaxis=dict(range=[0, 40], title="Taux (%)", gridcolor="lightgray"),
    plot_bgcolor="white",
    legend_title="Opérateur"
)

st.plotly_chart(fig, use_container_width=True)
