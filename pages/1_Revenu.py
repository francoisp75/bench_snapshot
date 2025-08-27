""""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Charger et préparer les données
@st.cache_data
def load_data():
    df = pd.read_excel("data/Bench_Viz.xlsx")
    df = df[df['kpi'] == 'YoY organic revenue growth']

    # Convertir les pourcentages texte en float
    for col in ['2Q24', '3Q24', '4Q24', '1Q25', '2Q25']:
        df[col] = df[col].astype(str).str.replace('%','').str.replace(',','.').astype(float)

    return df

df = load_data()

# Liste des opérateurs
operators = ['ORA', 'VOD', 'DT', 'BT', 'TIM']

st.title("Page 1 – Revenu")
st.write("Évolution de la croissance organique YoY des revenus (Europe / non Europe / Groupe)")

for op in operators:
    op_df = df[df['operator'] == op]

    # Extraire les données
    europe = op_df[op_df['scope'] == 'Europe']
    non_europe = op_df[op_df['scope'] == 'non Europe']
    group = op_df[op_df['scope'] == 'Group']

    periods = ['2Q24', '3Q24', '4Q24', '1Q25', '2Q25']

    europe_vals = europe[periods].values.flatten() if not europe.empty else [0]*5
    non_europe_vals = non_europe[periods].values.flatten() if not non_europe.empty else [0]*5
    group_vals = group[periods].values.flatten() if not group.empty else [0]*5

    # Création du graphique
    fig, ax = plt.subplots(figsize=(10, 5))

    x = range(len(periods))
    bar_width = 0.35

    ax.bar([i - bar_width/2 for i in x], europe_vals, width=bar_width, color='blue', label='Europe')
    ax.bar([i + bar_width/2 for i in x], non_europe_vals, width=bar_width, color='pink', label='non Europe')
    ax.plot(x, group_vals, color='black', marker='o', label='Group', linewidth=2)

    ax.set_xticks(x)
    ax.set_xticklabels(periods)
    ax.set_ylabel("YoY Growth (%)")
    ax.set_title(f"{op} – Croissance organique YoY des revenus")
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)

    st.pyplot(fig)


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    df = pd.read_excel("data/Bench_Viz.xlsx")
    df = df[df['kpi'] == 'YoY organic revenue growth']

    periods = ['2Q24', '3Q24', '4Q24', '1Q25', '2Q25']
    for col in periods:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(r'[%]', '', regex=True).str.replace(',', '.', regex=False),
            errors='coerce'
        )
        df[col] = df[col] * 100  # conversion en %
    return df

df = load_data()
operators = ['ORA', 'VOD', 'DT', 'BT', 'TIM']
periods = ['2Q24', '3Q24', '4Q24', '1Q25', '2Q25']

st.title("Page 1 – Revenu")
st.write("Évolution de la croissance organique YoY des revenus (Europe / non Europe / Groupe)")

for op in operators:
    op_df = df[df['operator'] == op]

    europe_vals     = op_df[op_df['scope'] == 'Europe'][periods].values.flatten() if not op_df[op_df['scope'] == 'Europe'].empty else [0]*5
    non_europe_vals = op_df[op_df['scope'] == 'non Europe'][periods].values.flatten() if not op_df[op_df['scope'] == 'non Europe'].empty else [0]*5
    group_vals      = op_df[op_df['scope'] == 'Group'][periods].values.flatten() if not op_df[op_df['scope'] == 'Group'].empty else [0]*5

    fig, ax = plt.subplots(figsize=(10, 5))
    x = range(len(periods))
    bar_width = 0.35

    # Barres
    bars1 = ax.bar([i - bar_width/2 for i in x], europe_vals, width=bar_width, color='blue', label='Europe')
    bars2 = ax.bar([i + bar_width/2 for i in x], non_europe_vals, width=bar_width, color='pink', label='non Europe')

    # Ligne
    ax.plot(x, group_vals, color='black', marker='o', label='Group', linewidth=2)

    # Ajouter les labels sur les barres
    for bar in bars1:
        height = bar.get_height()
        if not pd.isna(height):
            ax.annotate(f"{height:.1f}%",
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8, color='blue')

    for bar in bars2:
        height = bar.get_height()
        if not pd.isna(height):
            ax.annotate(f"{height:.1f}%",
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8, color='darkred')

    # Ajouter les labels sur la courbe Group
    for i, val in enumerate(group_vals):
        if not pd.isna(val):
            ax.annotate(f"{val:.1f}%",
                        xy=(i, val),
                        xytext=(0, 5),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8, color='black')

    # Axe X
    ax.set_xticks(x)
    ax.set_xticklabels(periods)

    # Suppression de l'axe Y et du quadrillage
    ax.yaxis.set_visible(False)
    ax.grid(False)

    ax.set_title(f"{op} – Croissance organique YoY des revenus")
    ax.legend()

    # Ajuster pour que les étiquettes ne soient pas coupées
    ymax = max(list(europe_vals) + list(non_europe_vals) + list(group_vals)) * 1.2
    ax.set_ylim(0, ymax)

    st.pyplot(fig)




import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    df = pd.read_excel("data/Bench_Viz.xlsx")
    df = df[df['kpi'] == 'YoY organic revenue growth']

    periods = ['2Q24', '3Q24', '4Q24', '1Q25', '2Q25']
    for col in periods:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(r'[%]', '', regex=True).str.replace(',', '.', regex=False),
            errors='coerce'
        )
    return df

df = load_data()
operators = ['ORA', 'VOD', 'DT', 'BT', 'TIM']
periods = ['2Q24', '3Q24', '4Q24', '1Q25', '2Q25']

st.title("Page 1 – Revenu")
st.write("Évolution de la croissance organique YoY des revenus (Europe / non Europe / Groupe)")

for op in operators:
    op_df = df[df['operator'] == op]

    europe_vals     = op_df[op_df['scope'] == 'Europe'][periods].values.flatten() if not op_df[op_df['scope'] == 'Europe'].empty else [0]*5
    non_europe_vals = op_df[op_df['scope'] == 'non Europe'][periods].values.flatten() if not op_df[op_df['scope'] == 'non Europe'].empty else [0]*5
    group_vals      = op_df[op_df['scope'] == 'Group'][periods].values.flatten() if not op_df[op_df['scope'] == 'Group'].empty else [0]*5

    fig, ax = plt.subplots(figsize=(10, 5))
    x = range(len(periods))
    bar_width = 0.35

    # Barres
    bars1 = ax.bar([i - bar_width/2 for i in x], europe_vals, width=bar_width, color='blue', label='Europe')
    bars2 = ax.bar([i + bar_width/2 for i in x], non_europe_vals, width=bar_width, color='pink', label='non Europe')

    # Ligne
    ax.plot(x, group_vals, color='black', marker='o', label='Group', linewidth=2)

    # Ajouter les labels sur les barres
    for bar in bars1:
        height = bar.get_height()
        if not pd.isna(height):
            ax.annotate(f"{height:.1f}%",
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # décalage vertical
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8, color='blue')

    for bar in bars2:
        height = bar.get_height()
        if not pd.isna(height):
            ax.annotate(f"{height:.1f}%",
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8, color='darkred')

    # Ajouter les labels sur la courbe Group
    for i, val in enumerate(group_vals):
        if not pd.isna(val):
            ax.annotate(f"{val:.1f}%",
                        xy=(i, val),
                        xytext=(0, 5),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8, color='black')

    ax.set_xticks(x)
    ax.set_xticklabels(periods)
    ax.set_ylabel("YoY Growth (%)")
    ax.set_title(f"{op} – Croissance organique YoY des revenus")
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)

    # Étendre un peu l'axe Y pour éviter que les labels soient coupés
    ymax = max(list(europe_vals) + list(non_europe_vals) + list(group_vals)) * 1.2
    ax.set_ylim(0, ymax)

    st.pyplot(fig)
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    df = pd.read_excel("data/Bench_Viz.xlsx")
    df = df[df['kpi'] == 'YoY organic revenue growth']

    periods = ['2Q24', '3Q24', '4Q24', '1Q25', '2Q25']
    for col in periods:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(r'[%]', '', regex=True).str.replace(',', '.', regex=False),
            errors='coerce'
        )
        df[col] = df[col] * 100  # conversion en %
    return df

df = load_data()
operators = ['ORA', 'VOD', 'DT', 'BT', 'TIM']
periods = ['2Q24', '3Q24', '4Q24', '1Q25', '2Q25']

st.title("Page 1 – Revenu")
st.write("Évolution de la croissance organique YoY des revenus (Europe / non Europe / Groupe)")

for op in operators:
    op_df = df[df['operator'] == op]

    europe_vals     = op_df[op_df['scope'] == 'Europe'][periods].values.flatten() if not op_df[op_df['scope'] == 'Europe'].empty else [0]*5
    non_europe_vals = op_df[op_df['scope'] == 'non Europe'][periods].values.flatten() if not op_df[op_df['scope'] == 'non Europe'].empty else [0]*5
    group_vals      = op_df[op_df['scope'] == 'Group'][periods].values.flatten() if not op_df[op_df['scope'] == 'Group'].empty else [0]*5

    fig, ax = plt.subplots(figsize=(10, 5))
    x = range(len(periods))
    bar_width = 0.35

    # Barres
    bars1 = ax.bar([i - bar_width/2 for i in x], europe_vals, width=bar_width, color='blue', label='Europe')
    bars2 = ax.bar([i + bar_width/2 for i in x], non_europe_vals, width=bar_width, color='pink', label='non Europe')

    # Ligne
    ax.plot(x, group_vals, color='black', marker='o', label='Group', linewidth=2)

    # Ajouter les labels sur les barres
    for bar in bars1:
        height = bar.get_height()
        if not pd.isna(height):
            offset = 3 if height >= 0 else -10  # au-dessus si positif, en dessous si négatif
            va = 'bottom' if height >= 0 else 'top'
            ax.annotate(f"{height:.1f}%",
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, offset),
                        textcoords="offset points",
                        ha='center', va=va, fontsize=8, color='blue')

    for bar in bars2:
        height = bar.get_height()
        if not pd.isna(height):
            offset = 3 if height >= 0 else -10
            va = 'bottom' if height >= 0 else 'top'
            ax.annotate(f"{height:.1f}%",
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, offset),
                        textcoords="offset points",
                        ha='center', va=va, fontsize=8, color='darkred')

    # Ajouter les labels sur la courbe Group
    for i, val in enumerate(group_vals):
        if not pd.isna(val):
            offset = 5 if val >= 0 else -10
            va = 'bottom' if val >= 0 else 'top'
            ax.annotate(f"{val:.1f}%",
                        xy=(i, val),
                        xytext=(0, offset),
                        textcoords="offset points",
                        ha='center', va=va, fontsize=8, color='black')

    # Axe X
    ax.set_xticks(x)
    ax.set_xticklabels(periods)

    # Suppression de l'axe Y et du quadrillage
    ax.yaxis.set_visible(False)
    ax.grid(False)

    ax.set_title(f"{op} – Croissance organique YoY des revenus")
    ax.legend()

    # Ajuster limites Y (haut et bas) pour inclure valeurs négatives
    all_vals = list(europe_vals) + list(non_europe_vals) + list(group_vals)
    ymin = min(all_vals) * 1.2 if min(all_vals) < 0 else 0
    ymax = max(all_vals) * 1.2 if max(all_vals) > 0 else 0
    ax.set_ylim(ymin, ymax)

    st.pyplot(fig)
