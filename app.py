import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

st.set_page_config(page_title="Painel Financeiro", layout="wide")
st.title("📊 Painel Financeiro")

st.markdown("Faça upload da sua planilha `.ods` ou `.xlsx` contendo os dados de gastos.")

# Botão para baixar planilha exemplo
with open("exemplo_planilha.xlsx", "rb") as file:
    st.download_button(
        label="📥 Baixar planilha exemplo",
        data=file,
        file_name="exemplo_planilha.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

uploaded_file = st.file_uploader("Selecione sua planilha", type=["ods", "xlsx"])

if uploaded_file:
    try:
        # Leitura da planilha
        df = pd.read_excel(
            uploaded_file,
            engine="odf" if uploaded_file.name.endswith(".ods") else "openpyxl"
        )

        # Limpa espaços nos nomes das colunas
        df.columns = [col.strip() for col in df.columns]

        # Renomeia coluna Mês se necessário
        if 'Mês ' in df.columns:
            df.rename(columns={'Mês ': 'Mês'}, inplace=True)

        # Função de limpeza de valores
        def limpar_valor(valor):
            if isinstance(valor, str):
                valor = valor.replace('R$', '').strip()
                valor = re.sub(r'\.(?=\d{3}(,|$))', '', valor)
                valor = valor.replace(',', '.')
            try:
                return float(valor)
            except:
                return 0.0

        # Aplica limpeza
        df['Valor (R$)'] = df['Valor (R$)'].apply(limpar_valor)

        # Organiza meses na ordem correta
        ordem_meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                       'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        df['Mês'] = pd.Categorical(df['Mês'], categories=ordem_m_
