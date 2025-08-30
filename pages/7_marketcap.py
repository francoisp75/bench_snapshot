import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("Classement des plus grandes entreprises de télécoms")

# Lien vers la source
st.markdown(
    """
    <a href="https://companiesmarketcap.com/fr/telecommunication/plus-grandes-entreprises-de-telecommunications-par-capitalisation-boursiere/" target="_blank">
        <button style="background-color:#4CAF50; color:white; padding:10px 20px; border:none; border-radius:8px; font-size:16px; cursor:pointer;">
            🔗 Voir le classement complet sur CompaniesMarketCap
        </button>
    </a>
    """,
    unsafe_allow_html=True
)

# === Données extraites du site (capture partagée) ===
data = {
    "Rang": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "Nom": [
        "T-Mobile US", "China Mobile", "AT&T", "Verizon", "Deutsche Telekom",
        "SoftBank", "Bharti Airtel", "Comcast", "American Tower", "China Telecom",
        "NTT", "KDDI", "América Móvil", "Saudi Telecom Company", "Singtel", "Orange"
    ],
    "Capitalisation Boursière (Mds €)": [
        242.55, 214.09, 179.12, 159.50, 154.55,
        134.52, 109.92, 107.27, 81.64, 79.43,
        75.00, 56.71, 51.60, 47.77, 47.42, 37.29
    ],
    "Pays": [
        "USA", "Chine", "USA", "USA", "Allemagne",
        "Japon", "Inde", "USA", "USA", "Chine",
        "Japon", "Japon", "Mexique", "Arabie Saoudite", "Singapour", "France"
    ]
}

df = pd.DataFrame(data)

# === Afficher le Top 5 ===
st.subheader("📊 Top 5 des entreprises télécoms par capitalisation boursière")
st.table(df.head(5))

# === Positionnement d’Orange ===
orange_row = df[df["Nom"] == "Orange"]

st.subheader("📍 Positionnement d’Orange")
st.table(orange_row)
