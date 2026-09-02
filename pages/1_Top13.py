import pandas as pd
import streamlit as st

# === Données ===
data = {
    "operator": [
        "China Mobile", "DT", "Verizon", "NTT", "Comcast",
         "China Telecom", "ATT","China Unicom", "América Móvil","Orange","VOD",
        "SoftBank", "KDDI", "TEF"
    ],
    "revenue": [67, 60, 59, 41, 34, 33, 27, 25, 23, 21, 21, 20, 17, 16],
    "growth": [-1.1, 4.0, 1.0, 10, -2.9, -4.0, 2.6, 0.6, 1.3, 3.5, 3.6, 7.9, 4.9, 0.4],
}

df = pd.DataFrame(data)
df["rank"] = range(1, len(df) + 1)

# Flèches croissance
df["growth_arrow"] = ["↑" if val > 0 else "↓" for val in df["growth"]]
df["growth_color"] = ["green" if val > 0 else "red" for val in df["growth"]]
df["growth_text"] = [f"{val:+.1f}%" for val in df["growth"]]

# === Layout Streamlit ===
st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align:center;'>Global Top 14</h1>", unsafe_allow_html=True)

# === CSS custom ===
st.markdown("""
    <style>
    .ranking-row {
        display: flex;
        align-items: center;
        justify-content: center; /* centrage horizontal */
        margin: 4px auto;
        padding: 4px 8px;
        border-radius: 6px;
        background-color: #f8f9fa;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        font-family: Arial, sans-serif;
        max-width: 600px; /* largeur max réduite */
    }
    .rank {
        width: 32px;
        font-size: 15px;
        font-weight: bold;
        text-align: right;
        margin-right: 6px; /* espace réduit */
        color: black;
    }
    .rank.orange {
        color: orange;
    }
    .box {
        flex-grow: 1;
        padding: 3px 6px;
        border-radius: 5px;
        font-size: 14px;
        font-weight: 500;
        background-color: white;
        border: 1px solid #ddd;
        max-width: 300px; /* box plus étroite */
        margin-right: 6px; /* espace réduit avec la croissance */
        text-align: left;
    }
    .box.orange {
        color: orange;
        font-weight: bold;
    }
    .growth {
        width: 70px;
        text-align: left;
        font-size: 14px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# === Construction du classement ===
for _, row in df.iterrows():
    operator = row["operator"]
    rank = row["rank"]
    revenue = row["revenue"]
    arrow = row["growth_arrow"]
    growth = row["growth_text"]
    color = row["growth_color"]

    # highlight Orange
    rank_style = "orange" if operator == "Orange" else ""
    box_style = "orange" if operator == "Orange" else ""

    st.markdown(f"""
        <div class="ranking-row">
            <div class="rank {rank_style}">{rank}</div>
            <div class="box {box_style}">{operator} — {revenue:.1f} Mds €</div>
            <div class="growth" style="color:{color};">{arrow} {growth}</div>
        </div>
    """, unsafe_allow_html=True)
