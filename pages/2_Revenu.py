import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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
    default=operators
)

for op in selected_ops:
    op_df = df[df['operator'] == op]

    europe_vals     = op_df[op_df['scope'] == 'Europe'][periods].values.flatten() if not op_df[op_df['scope'] == 'Europe'].empty else [None]*5
    non_europe_vals = op_df[op_df['scope'] == 'non Europe'][periods].values.flatten() if not op_df[op_df['scope'] == 'non Europe'].empty else [None]*5
    group_vals      = op_df[op_df['scope'] == 'Group'][periods].values.flatten() if not op_df[op_df['scope'] == 'Group'].empty else [None]*5

    fig = go.Figure()

    # Barres Europe / non Europe
    fig.add_trace(go.Bar(
        x=periods,
        y=europe_vals,
        name='Europe',
        marker_color='blue',
        text=[f"{v:.1f}%" if v is not None else "" for v in europe_vals],
        textposition='outside'
    ))

    fig.add_trace(go.Bar(
        x=periods,
        y=non_europe_vals,
        name='non Europe',
        marker_color='pink',
        text=[f"{v:.1f}%" if v is not None else "" for v in non_europe_vals],
        textposition='outside'
    ))

    # Ligne Group avec labels en gras
    fig.add_trace(go.Scatter(
        x=periods,
        y=group_vals,
        mode='lines+markers+text',
        name='Group',
        line=dict(color='black', width=2),
        text=[f"{v:.1f}%" if v is not None else "" for v in group_vals],
        textposition='top center',
        textfont=dict(family="Arial Black, sans-serif", size=12, color='black')  # <-- texte gras via policetextf
    ))

    # Layout
    fig.update_layout(
        title=f"{op} – Croissance organique YoY des revenus",
        barmode='group',
        yaxis_title='%',
        xaxis_title='Période',
        yaxis=dict(showgrid=False),
        xaxis=dict(tickmode='linear'),
        showlegend=True,
        margin=dict(t=50, b=50, l=20, r=20),
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)
