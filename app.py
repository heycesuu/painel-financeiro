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

uploaded_file = st.file_uploader("Selecione sua planilha", type=["ods", "xlsx"])

if uploaded_file:
    try:
        # 📄 Lê a planilha
        df = pd.read_excel(
            uploaded_file,
            engine="odf" if uploaded_file.name.endswith(".ods") else "openpyxl"
        )

        # 🔠 Corrige nomes das col
