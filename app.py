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

# 🧹 Função para limpar valores
def limpar_valor(valor):
    if isinstance(valor, str):
        valor = valor.replace('R$', '').strip()
        valor = re.sub(r'\.(?=\d{3}(,|$))', '', valor)  # remove ponto de milhar
        valor = valor.replace(',', '.')  # vírgula decimal vira ponto
    try:
        return float(valor)
    except:
        return 0.0

# 📂 Upload da planilha
uploaded_file = st.file_uploader("Selecione sua planilha", type=["ods", "xlsx"])

if uploaded_file:
    try:
        # 📄 Lê a planilha
        df = pd.read_excel(
            uploaded_file,
            engine="odf" if uploaded_file.name.endswith(".ods") else "openpyxl"
        )

        # 🔠 Corrige nomes das colunas
        df.columns = [col.strip() for col in df.columns]
        if 'Mês ' in df.columns:
            df.rename(columns={'Mês ': 'Mês'}, inplace=True)

        # 💰 Limpa valores
        df['Valor (R$)'] = df['Valor (R$)'].apply(limpar_valor)

        # 📅 Ordena os meses corretamente
        ordem_meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                       'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        df['Mês'] = pd.Categorical(df['Mês'], categories=ordem_meses, ordered=True)
        df = df.sort_values('Mês')

        # 🧭 Filtros
        st.sidebar.header("🔎 Filtros")

        meses_unicos = df['Mês'].dropna().unique()
        filtro_mes = st.sidebar.multiselect("Filtrar por mês:", options=meses_unicos, default=meses_unicos)

        categorias_unicas = df['Descrição'].dropna().unique()
        filtro_categoria = st.sidebar.multiselect("Filtrar por categoria:", options=categorias_unicas, default=categorias_unicas)

        # 🔍 Aplica os filtros
        df_filtrado = df[(df['Mês'].isin(filtro_mes)) & (df['Descrição'].isin(filtro_categoria))]

        # 📋 Tabela
        st.subheader("📋 Tabela de Gastos")
        st.dataframe(df_filtrado)

        # 📊 Gráfico de barras por mês
        st.subheader("📅 Gastos por Mês")
        gastos_mes = df_filtrado.groupby("Mês")['Valor (R$)'].sum().reset_index()
        st.bar_chart(gastos_mes.set_index("Mês"))

        # 🥧 Gráfico de pizza por categoria
        st.subheader("📌 Gastos por Categoria")
        gastos_categoria = df_filtrado.groupby("Descrição")['Valor (R$)'].sum()
        fig, ax = plt.subplots()
        ax.pie(gastos_categoria, labels=gastos_categoria.index, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        st.pyplot(fig)

        # 💰 Total
        total = df_filtrado['Valor (R$)'].sum()
        total_formatado = f"R$ {total:,.2f}".replace(".", ",").replace(",", ".", 1)
        st.metric("💰 Total Geral de Gastos", total_formatado)

    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo: {e}")

else:
    st.info("Faça o upload de uma planilha para começar.")
