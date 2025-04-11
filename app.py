import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Painel Financeiro", layout="wide")
st.title("📊 Painel Financeiro")

st.markdown("Faça upload da sua planilha `.ods` ou `.xlsx` contendo os dados de gastos.")

uploaded_file = st.file_uploader("Selecione sua planilha", type=["ods", "xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, engine="odf" if uploaded_file.name.endswith(".ods") else "openpyxl")
        df.columns = [col.strip() for col in df.columns]  # Limpa espaços
if 'Mês ' in df.columns:
    df.rename(columns={'Mês ': 'Mês'}, inplace=True)

        
        # Corrige valores com vírgula e símbolo de R$
        df['Valor (R$)'] = (
            df['Valor (R$)']
            .astype(str)
            .str.replace('R$', '', regex=False)
            .str.replace('.', '', regex=False)  # remove separador de milhar
            .str.replace(',', '.', regex=False)  # troca vírgula decimal por ponto
            .astype(float)
        )

        # Exibir tabela
        st.subheader("📋 Tabela de Gastos")
        st.dataframe(df)

        # Total por mês
        st.subheader("📅 Gastos por Mês")
        gastos_mes = df.groupby("Mês")['Valor (R$)'].sum().reset_index()
st.bar_chart(gastos_mes.set_index("Mês"))

        # Total geral
        st.metric("💰 Total Geral de Gastos", f"R$ {df['Valor (R$)'].sum():,.2f}".replace('.', ',').replace(',', '.', 1))

    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo: {e}")
else:
    st.info("Faça o upload de uma planilha para começar.")
