import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

st.set_page_config(page_title="Painel Financeiro", layout="wide")
st.title("📊 Painel Financeiro")

st.markdown("Faça upload da sua planilha `.ods` ou `.xlsx` contendo os dados de gastos.")

# 📥 Botão para baixar planilha exemplo
with open("exemplo_planilha.xlsx", "rb") as file:
    btn = st.download_button(
        label="📥 Baixar planilha exemplo",
        data=file,
        file_name="exemplo_planilha.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

uploaded_file = st.file_uploader("Selecione sua planilha", type=["ods", "xlsx"])

if uploaded_file:
    try:
        # 🧾 Leitura do arquivo
        df = pd.read_excel(
            uploaded_file,
            engine="odf" if uploaded_file.name.endswith(".ods") else "openpyxl"
        )

        # 🔠 Corrige nomes das colunas (tira espaços extras)
        df.columns = [col.strip() for col in df.columns]

        # 🛠 Renomeia a coluna "Mês " se necessário
        if 'Mês ' in df.columns:
            df.rename(columns={'Mês ': 'Mês'}, inplace=True)

        # 💰 Limpa os valores com R$, vírgulas etc.
        def limpar_valor(valor):
            if isinstance(valor, str):
                valor = valor.replace('R$', '').strip()
                valor = re.sub(r'\.(?=\d{3}(,|$))', '', valor)  # remove pontos de milhar
                valor = valor.replace(',', '.')  # vírgula decimal
            try:
                return float(valor)
            except:
                return 0.0

        df['Valor (R$)'] = df['Valor (R$)'].apply(limpar_valor)

        # 📅 Ordena os meses corretamente
        ordem_meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                       'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        df['Mês'] = pd.Categorical(df['Mês'], categories=ordem_meses, ordered=True)
        df = df.sort_values('Mês')

        # 🔍 Filtros na barra lateral
        st.sidebar.header("🔎 Filtros")
        meses_unicos = df['Mês'].dropna().unique()
        filtro_mes = st.sidebar.multiselect("Filtrar por mês:", options=meses_unicos, default=meses_unicos)

        categorias_unicas = df['Descrição'].dropna().unique()
        filtro_categoria = st.sidebar.multiselect("Filtrar por categoria:", options=categorias_unicas)

        # 🔍 Aplica os filtros de forma independente
        df_filtrado = df.copy()
        if filtro_mes:
            df_filtrado = df_filtrado[df_filtrado['Mês'].isin(filtro_mes)]
        if filtro_categoria:
            df_filtrado =_
