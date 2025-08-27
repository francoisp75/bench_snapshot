import streamlit as st

st.set_page_config(page_title="Dashboard KPI Télécoms", layout="wide")

st.title("📊 Dashboard KPI Télécoms")
st.markdown("""
Bienvenue dans le tableau de bord multi-pages.

Utilisez le **menu à gauche** pour naviguer entre les indicateurs clés :
- **Page 1** : Revenu
- **Page 2** : EBITDAaL
- **Page 3** : Capex
- **Page 4** : OPCF

Les données affichées couvrent les périodes de **2Q24 à 2Q25** et sont présentées par **opérateur**, **zone géographique** et **type de KPI**.
""")
