import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from io import BytesIO
from datetime import datetime

from utils.data_processing import load_file
from utils.benchmarking import create_summary, add_rankings, add_price_delta

SAMPLE_PATH = "sample_data/hotel_rates_sample.xlsx"

st.set_page_config(
    page_title="Hotel Rate Shopper MVP",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🏨"
)

# Apply dark theme
st.markdown(
    """
    <style>
    .css-18e3th9 { background: #18191A !important; }
    .stApp, .st-cv, .stDataFrame, .stTable, .st-bw, .st-bx {
        color: #E4E6EB !important;
        background-color: #18191A !important;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background: #242526;
        color: #00D26A !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🏨 Hotel Rate Shopper Benchmarking (MVP)")
st.markdown("Faça upload de sua planilha de tarifas ou use o exemplo. Veja insights competitivos instantâneos!")

with st.sidebar:
    st.header("1. Dados de tarifas")
    use_sample = st.toggle("Usar dados de exemplo", value=True)
    uploaded = st.file_uploader("Envie um arquivo Excel (.xlsx) ou CSV", type=["xlsx", "csv"], disabled=use_sample)
    st.markdown("Formato necessário: hotel, competitor, date, rate.")

    st.header("2. Filtros")
    df = None
    file_name = None
    error = None

    @st.cache_data(show_spinner=False)
    def load_and_prep(file_bytes, filename):
        df = load_file(file_bytes, filename)
        df = add_rankings(df)
        df = add_price_delta(df)
        return df

    if use_sample:
        try:
            with open(SAMPLE_PATH, "rb") as f:
                df = load_and_prep(f.read(), SAMPLE_PATH)
                file_name = SAMPLE_PATH
        except Exception as e:
            error = f"Erro ao carregar dados de exemplo: {e}"
    elif uploaded:
        try:
            df = load_and_prep(uploaded.read(), uploaded.name)
            file_name = uploaded.name
        except Exception as e:
            error = f"Erro ao processar arquivo: {e}"
    else:
        st.info("Envie um arquivo para começar, ou use o exemplo.")

if error:
    st.error(error)
    st.stop()

if df is not None:
    hotels = sorted(df['hotel'].unique())
    competitors = sorted(df['competitor'].unique())
    min_date = df['date'].min()
    max_date = df['date'].max()

    sel_hotels = st.sidebar.multiselect("Hotel(s)", options=hotels, default=hotels)
    sel_date = st.sidebar.date_input(
        "Período", 
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    if isinstance(sel_date, tuple):
        date_from, date_to = sel_date
    else:
        date_from, date_to = min_date, max_date

    # Filtered data
    df_filt = df[
        (df['hotel'].isin(sel_hotels)) &
        (df['date'] >= pd.to_datetime(date_from)) &
        (df['date'] <= pd.to_datetime(date_to))
    ]

    # Summary Table
    summary_df = create_summary(df_filt, pd.to_datetime(date_from), pd.to_datetime(date_to), sel_hotels)

    # Prepare for Excel download: add rankings and deltas for all
    def to_excel_bytes(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name="Benchmark")
        return output.getvalue()

    st.markdown("---")
    tab1, tab2 = st.tabs(["📊 Tabela Resumo", "📈 Tendência de Preços"])

    with tab1:
        st.subheader("Resumo por Hotel e Concorrente")
        # Conditional formatting
        def highlight_rank(row):
            if np.isnan(row['avg_rate']): return ''
            if row['avg_rate'] == summary_df['avg_rate'].min():
                return 'background-color: #2ecc40; color: black; font-weight:bold'
            elif row['avg_rate'] == summary_df['avg_rate'].max():
                return 'background-color: #ff4136; color: white; font-weight:bold'
            return ''
        styled = summary_df.style.applymap(
            lambda v: 'font-weight:bold' if isinstance(v, float) else ''
        ).apply(
            lambda x: [highlight_rank(row) for _, row in summary_df.iterrows()], axis=1
        )
        st.dataframe(
            styled,
            use_container_width=True,
            height=450
        )

        st.download_button(
            label="⬇️ Baixar Benchmark em Excel",
            data=to_excel_bytes(summary_df),
            file_name="benchmark.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.markdown("Legenda: verde = tarifa média mais barata, vermelho = mais cara.")

        st.markdown("**Colunas:** hotel, concorrente, tarifa média, mínima, máxima, mediana, quantidade.")

        st.caption(f"Linhas: {len(summary_df)}")

        st.subheader("Comparação Visual")
        bar = alt.Chart(summary_df).mark_bar().encode(
            x=alt.X('competitor:N', title="Concorrente"),
            y=alt.Y('avg_rate:Q', title="Tarifa Média"),
            color='competitor:N',
            column=alt.Column('hotel:N', title="Hotel"),
            tooltip=['hotel', 'competitor', 'avg_rate', 'min_rate', 'max_rate', 'median_rate']
        ).properties(
            height=300
        )
        st.altair_chart(bar, use_container_width=True)

    with tab2:
        st.subheader("Evolução de Tarifas ao Longo do Tempo")
        if df_filt.empty:
            st.warning("Nenhum dado para o filtro selecionado.")
        else:
            # Line chart: Rate over time per competitor/hotel
            line = alt.Chart(df_filt).mark_line(point=True).encode(
                x=alt.X('date:T', title="Data"),
                y=alt.Y('rate:Q', title="Tarifa"),
                color=alt.Color('competitor:N', title="Concorrente"),
                strokeDash='hotel:N',
                tooltip=['date', 'hotel', 'competitor', 'rate', 'rank', 'price_delta']
            ).properties(
                height=400
            )
            st.altair_chart(line, use_container_width=True)

    st.markdown("---")
    st.caption(f"Arquivo: {file_name} — {len(df)} registros totais.")

else:
    st.info("Envie um arquivo ou use o exemplo para começar.")