import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
from datetime import datetime
from conversor import main

converted_value = 0

# Agrupando informações da API de conversão de moedas
with open("cotacoes.json", "r", encoding="utf-8") as f:
    taxas = json.load(f)

df = pd.DataFrame.from_dict(taxas, orient="index", columns=["Valor"])
df.index.name = "Moeda"
df.reset_index(inplace=True)

# Estrutura física do dashboard
st.set_page_config(
    page_title="Conversor de Real",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Conversor de Real para Moeda Estrangeira")
st.divider()

att = st.button(
    label="Atualizar taxas de câmbio",
    type="primary",
    use_container_width=True,
)

if att == True:
    try:
        main()
        st.success("Taxas de câmbio atualizadas com sucesso!")
    except Exception as e:
        st.error(f"Erro ao atualizar taxas de câmbio: {e}")

# Seleção de moeda
conversion_col1, conversion_col2 = st.columns(2)

with conversion_col1:
    conversion = st.radio(
        "Selecione o tipo de conversão: ",
        options = [
            "Real para moeda estrangeira",
            "Moeda estrangeira para Real"
        ],
        index= None,
    )
    coin = st.selectbox(
        "Escolha uma moeda para a conversão:",
        index=None,
        options=[
            "Dólares",
            "Euros",
            "Libras",
            "Yuas Chinês",
            "Peso Argentino",
            "Dólar Canadense",
            "Peso Chileno",
            "Peso Mexicano",
        ],
        placeholder="Selecione uma opção para conversão",
        accept_new_options=False,
    )

with conversion_col2:
    # Input de valor
    conversion_value = st.number_input(
        label= "Valor a ser convertido: ", 
        min_value= 0.0,
        placeholder= "Digite o valor a ser convertido",
        format= "%.2f",
        step = 1.0,
    )

    do_conversion = st.button(
        label="Converter",
        type="primary",
        use_container_width=True,
    )


st.divider()

# Função que irá fazer a conversão do valor


def converter_moeda(conversion_value, conversion, coin):
    if conversion == "Real para moeda estrangeira":
        coin_dict = {
            "Dólares": "USD",
            "Euros": "EUR",
            "Libras": "GBP",
            "Yuans Chinês": "CNY",
            "Peso Argentino": "ARS",
            "Dólar Canadense": "CAD",
            "Peso Chileno": "CLP",
            "Peso Mexicano": "MXN",
            
        }
    elif conversion == "Moeda estrangeira para Real":
        coin_dict = {
            "Dólares": "USD",
            "Euros": "EUR",
            "Libras": "GBP",
            "Yuans Chinês": "CNY",
            "Peso Argentino": "ARS",
            "Dólar Canadense": "CAD",
            "Peso Chileno": "CLP",
            "Peso Mexicano": "MXN",
        }
    else: 
        raise ValueError("Tipo de conversão não suportado")
    
    # Verifica se a moeda escolhida existe no dicionário
    if coin in coin_dict:
        coin_code = coin_dict[coin]
        taxa = df.loc[df["Moeda"] == coin_code, "Valor"].values[0]
    else: 
        raise ValueError("Moeda não suportada")
    
    # Realiza a conversão
    if conversion == "Real para moeda estrangeira":
        converted_value = conversion_value * taxa
    elif conversion == "Moeda estrangeira para Real":
        converted_value = conversion_value / taxa
    else: 
        raise ValueError("Tipo de conversão não suportado")
    
    return converted_value

# Verifica se o botão de conversão foi pressionado e chama a função
if do_conversion == True:
    try: 
        result = converter_moeda(conversion_value, conversion, coin)
        if conversion == "Real para moeda estrangeira":
            st.success(f"Valor convertido: {result:.2f} {coin}")
        elif conversion == "Moeda estrangeira para Real":
            st.success(f"Valor convertido: R${result:.2f}")
    except ValueError as e:
        st.error(f"Erro: {e}")

# Gráfico de comparação das moedas em relação ao real
st.write(
    "Gráfico mostrando o valor do real em relação às moedas estrangeiras disponíveis na API."
    " O valor do real é considerado 1,00 e as demais moedas são apresentadas em relação a ele."
)

fig, ax = plt.subplots(figsize=(3, 3))
df.plot(
    kind="bar",
    x="Moeda",
    y="Valor",
    ax=ax,
    color="blue",
    legend=False
)
ax.set_xlabel("Moeda")
ax.set_ylabel("Valor (R$)")
st.pyplot(fig)
