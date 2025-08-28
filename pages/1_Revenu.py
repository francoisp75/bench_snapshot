
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

operators = ['ORA', 'VOD', 'DT', 'BT', 'TIM','TEF']
periods = ['2Q24', '3Q24', '4Q24', '1Q25', '2Q25']

st.title("Page 1 – Revenu")
st.write("Évolution de la croissance organique YoY des revenus (Europe / non Europe / Groupe)")

# --- Menu de sélection des opérateurs ---
selected_ops = st.multiselect(
    "Choisissez les opérateurs à afficher :",
    operators,
    default=operators  # par défaut tous sélectionnés
)

# --- Boucle uniquement sur les opérateurs choisis ---
for op in selected_ops:
    op_df = df[df['operator'] == op]

    europe_vals     = op_df[op_df['scope'] == 'Europe'][periods].values.flatten() if not op_df[op_df['scope'] == 'Europe'].empty else [float('nan')]*5
    non_europe_vals = op_df[op_df['scope'] == 'non Europe'][periods].values.flatten() if not op_df[op_df['scope'] == 'non Europe'].empty else [float('nan')]*5
    group_vals      = op_df[op_df['scope'] == 'Group'][periods].values.flatten() if not op_df[op_df['scope'] == 'Group'].empty else [float('nan')]*5

    fig, ax = plt.subplots(figsize=(10, 5))
    x = range(len(periods))
    bar_width = 0.35

    # Barres
    bars1 = ax.bar([i - bar_width/2 for i in x], europe_vals, width=bar_width, color='blue', label='Europe')
    bars2 = ax.bar([i + bar_width/2 for i in x], non_europe_vals, width=bar_width, color='pink', label='non Europe')

    # Ligne
    ax.plot(x, group_vals, color='black', marker='o', label='Group', linewidth=2)

    # Ligne horizontale zéro
    ax.axhline(0, color='gray', linewidth=1)

    # Labels sur barres et courbe
    for bar in bars1:
        height = bar.get_height()
        if not pd.isna(height):
            offset = 3 if height >= 0 else -10
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

    ax.yaxis.set_visible(False)
    ax.grid(False)

    ax.set_title(f"{op} – Croissance organique YoY des revenus")
    ax.legend()

    # Ajuster limites Y
    all_vals = [v for v in list(europe_vals) + list(non_europe_vals) + list(group_vals) if not pd.isna(v)]
    ymin = min(all_vals) * 1.2 if min(all_vals) < 0 else min(all_vals) * 0.8
    ymax = max(all_vals) * 1.2 if max(all_vals) > 0 else max(all_vals) * 0.8
    ax.set_ylim(ymin, ymax)

    st.pyplot(fig)
