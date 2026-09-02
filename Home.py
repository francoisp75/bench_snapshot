import streamlit as st

st.set_page_config(page_title="Benchmark KPI Telco", layout="wide")

st.title("📊 Dashboard KPI Télécoms")
st.markdown("""
Bienvenue dans ce tableau de bord digital.
**Comment Orange se positionne vs ses pairs sur les KPI financiers?**

Utilisez le **menu à gauche** pour naviguer entre les indicateurs clés :
- **Page 1** : Top14
- **Page 2** : Revenu
- **Page 3** : Revenu Europe
- **Page 4** : EBITDAaL
- **Page 5** : Capex
- **Page 6** : OPCF
- **Page 7** : Market Cap

Les données affichées couvrent les périodes de **2Q25 à 2Q26** et sont présentées par **opérateur**, **zone géographique** et **type de KPI**.
""")
