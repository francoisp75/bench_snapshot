import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Visualisation KPI - Operating Cash Flow / Revenue LTM (2Q25)")

# Charger les données
df = pd.read_excel("data/Bench_Viz.xlsx")

# Nettoyage colonnes
df.columns = df.columns.str.strip()
df["kpi"] = df["kpi"].astype(str).str.strip()
df["operator"] = df["operator"].astype(str).str.strip()

# Sélecteur d'opérateurs
all_operators = sorted(df["operator"].dropna().unique().tolist())
selected_operators = st.multiselect(
    "Sélectionnez les opérateurs à afficher :",
    options=all_operators,
    default=all_operators
)

# Filtrer uniquement OPCF
df = df[df["kpi"].str.lower() == "operating cash flow / revenue"].copy()

# Nettoyage des colonnes 2Q25 et 2Q24 si disponibles
for col in ["2Q25", "2Q24"]:
    if col in df.columns:
        df[col] = (
            df[col].astype(str)
            .str.replace("%", "", regex=False)
            .str.replace(",", ".", regex=False)
            .str.strip()
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")
        if df[col].max() <= 1.0:
            df[col] *= 100
    else:
        df[col] = None

df = df.dropna(subset=["2Q25"])
df = df[df["operator"].isin(selected_operators)]

# Calcul de la variation si 2Q24 disponible
if "2Q24" in df.columns:
    df["variation_pt"] = df["2Q25"] - df["2Q24"]
else:
    df["variation_pt"] = 0

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

# Tri pour légende (haut → bas)
df = df.sort_values("2Q25", ascending=False)
ordered_operators = df["operator"].unique().tolist()

# Préparer texte hover
def make_hover(row):
    color = "green" if row["variation_pt"] > 0 else ("red" if row["variation_pt"] < 0 else "black")
    return f"<b>{row['operator']}</b><br>Taux 2Q25 : {row['2Q25']:.1f}%<br>Variation : <span style='color:{color}'>{row['variation_pt']:+.1f} pt</span>"

df["hover_text"] = df.apply(make_hover, axis=1)
df["x"] = "OPCF"

# Affichage graphique
fig = px.scatter(
    df,
    x="x",
    y="2Q25",
    color="operator",
    category_orders={"operator": ordered_operators},
    color_discrete_map=operator_colors,
    height=650
)

# Associer tooltip point par point
for trace in fig.data:
    op = trace.name
    mask = df["operator"] == op
    trace.customdata = df.loc[mask, ["hover_text"]].values.tolist()
    trace.update(marker=dict(size=14), hovertemplate="%{customdata[0]}<extra></extra>")

# Ajustement automatique de l'échelle Y
ymax = df["2Q25"].max() + 5

fig.update_layout(
    title="Taux OPCF LTM (2Q25) par opérateur",
    xaxis=dict(showticklabels=False, title=""),
    yaxis=dict(range=[0, ymax], title="Taux (%)", gridcolor="lightgray"),
    plot_bgcolor="white",
    legend_title="Opérateur"
)

st.plotly_chart(fig, use_container_width=True)
