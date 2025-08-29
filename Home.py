import streamlit as st

st.set_page_config(page_title="Benchmark KPI Telco", layout="wide")

st.title("📊 Dashboard KPI Télécoms")
st.markdown("""
Bienvenue dans ce tableau de bord digital.
**Comment Orange se positionne vs ses pairs sur les KPI financiers?**

Utilisez le **menu à gauche** pour naviguer entre les indicateurs clés :
- **Page 1** : Revenu
- **Page 2** : Revenu Europe
- **Page 3** : EBITDAaL
- **Page 4** : Capex
- **Page 5** : OPCF

Les données affichées couvrent les périodes de **2Q24 à 2Q25** et sont présentées par **opérateur**, **zone géographique** et **type de KPI**.
""")
