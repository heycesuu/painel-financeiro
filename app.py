import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Painel Financeiro", layout="wide")
st.title("📊 Painel Financeiro")

st.markdown("Faça upload da sua planilha `.ods` ou `.xlsx` contendo os dados de gastos.")

uploaded_file = st.file_uploader("Selecione sua planilha", type=["ods", "xlsx"])

if uploaded_file:
    try:
        # Lê a planilha (ODS ou XLSX)
        df = pd.read_excel(
            uploaded_file,
            engine="odf" if uploaded_file.name.endswith(".ods") else "openpyxl"
        )

        # Limpa os espaços dos nomes das colunas
        df.columns = [col.strip() for col in df.columns]

        # Corrige o nome da coluna 'Mês ' para 'Mês'
        if 'Mês ' in df.columns:
            df.rename(columns={'Mês ': 'Mês'}, inplace=True)

        # Trata os valores com vírgula, R$ e ponto de milhar
        df['Valor (R$)'] = (
            df['Valor (R$)']
            .astype(str)
            .str.replace('R$', '', regex=False)
            .str.replace('.', '', regex=False)  # remove separador de milhar
            .str.replace(',', '.', regex=False)  # troca vírgula decimal por ponto
            .astype(float)
        )

        # Exibir a tabela
        st.subheader("📋 Tabela de Gastos")
        st.dataframe(df)

        # Agrupar por mês e mostrar gráfico
        st.subheader("📅 Gastos por Mês")
        gastos_mes = df.groupby("Mês")['Valor (R$)'].sum().reset_index()
        st.bar_chart(gastos_mes.set_index("Mês"))

        # Mostrar total geral
        total = df['Valor (R$)'].sum()
        total_formatado = f"R$ {total:,.2f}".replace(".", ",").replace(",", ".", 1)

