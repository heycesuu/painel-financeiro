import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

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

        # Trata os valores como vírgula, R$ e ponto de milhar
        def limpar_valor(valor):
            if isinstance(valor, str):
                valor = valor.replace('R$', '').strip()
                valor = re.sub(r'\.(?=\d{3}(,|$))', '', valor)  # remove ponto só se for milhar
                valor = valor.replace(',', '.')  # vírgula decimal vira ponto
            try:
                return float(valor)
            except:
                return 0.0

        df['Valor (R$)'] = df['Valor (R$)'].apply(limpar_valor)

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
        st.metric("💰 Total Geral de Gastos", total_formatado)

    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo: {e}")

else:
    st.info("Faça o upload de uma planilha para começar.")
