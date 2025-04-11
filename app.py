import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

st.set_page_config(page_title="Painel Financeiro", layout="wide")
st.title("📊 Painel Financeiro")

st.markdown("Faça upload da sua planilha `.ods` ou `.xlsx` contendo os dados de gastos.")

# Botão para baixar planilha exemplo
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
        # Lê a planilha
        df = pd.read_excel(
            uploaded_file,
            engine="odf" if uploaded_file.name.endswith(".ods") else "openpyxl"
        )

        # Limpa os nomes das colunas
        df.columns = [col.strip() for col in df.columns]

        # Renomeia a coluna se estiver com espaço
        if 'Mês ' in df.columns:
            df.rename(columns={'Mês ': 'Mês'}, inplace=True)

        # Função para limpar valores
        def limpar_valor(valor):
            if isinstance(valor, str):
                valor = valor.replace('R$', '').strip()
                valor = re.sub(r'\.(?=\d{3}(,|$))', '', valor)
                valor = valor.replace(',', '.')
            try:
                return float(valor)
            except:
                return 0.0

        # Aplica a função
        df['Valor (R$)'] = df['Valor (R$)'].apply(limpar_valor)

        # Organiza os meses na ordem correta
        ordem_meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                       'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        df['Mês'] = pd.Categorical(df['Mês'], categories=ordem_meses, ordered=True)
        df = df.sort_values('Mês')

        # Filtros
        st.sidebar.header("🔎 Filtros")
        filtro_mes = st.sidebar.multiselect("Filtrar por mês:", options=df['Mês'].dropna().unique())
        filtro_categoria = st.sidebar.multiselect("Filtrar por categoria:", options=df['Descrição'].dropna().unique())

        df_filtrado = df.copy()

        if filtro_mes:
            df_filtrado = df_filtrado[df_filtrado['Mês'].isin(filtro_mes)]
        if filtro_categoria:
            df_filtrado = df_filtrado[df_filtrado['Descrição'].isin(filtro_categoria)]

        # Exibir a tabela
        st.subheader("📋 Tabela de Gastos")
        st.dataframe(df_filtrado)

        # Gráfico de barras
        st.subheader("📅 Gastos por Mês")
        gastos_mes = df_filtrado.groupby("Mês")['Valor (R$)'].sum().reset_index()
        st.bar_chart(gastos_mes.set_index("Mês"))

        # Gráfico de pizza por categoria
        st.subheader("📊 Gastos por Categoria")
        gastos_categoria = df_filtrado.groupby("Descrição")['Valor (R$)'].sum()
        st.pyplot(gastos_categoria.plot.pie(autopct='%1.1f%%', figsize=(6,6), ylabel=''))

        # Total geral
        total = df_filtrado['Valor (R$)'].sum()
        total_formatado = f"R$ {total:,.2f}".replace(".", ",").replace(",", ".", 1)
        st.metric("💰 Total Geral de Gastos", total_formatado)

    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo: {e}")

else:
    st.info("Faça o upload de uma planilha para começar.")
