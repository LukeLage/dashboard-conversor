import requests
import json
from datetime import datetime

# Definindo as informações da API de conversão de moedas

api_key = "498f6e26b7357461501f4d23"
moeda_base = "BRL"
moedas_destino = [
    "USD",  # Dólar
    "EUR",  # Euro
    "GBP",  # Libra Esterlina
    "CNY",   # Yuan Chinês
    "ARS",  # Peso Argentino
    "CAD",  # Dólar Canadense
    "CLP",  # Peso Chileno
    "MXN",  # Peso Mexicano
]
arquivo_saida = "cotacoes.json"

def taxas_atualizadas():
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{moeda_base}"
    response = requests.get(url)
    
    if response.status_code == 200:
        dados = response.json()
        if dados ["result"] == "success":
            return {moeda: dados["conversion_rates"][moeda] for moeda in moedas_destino}
    raise Exception("Erro ao obter dados da API")

def salvar_cotacoes(dados):
    with open(arquivo_saida, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
    print(f"Dados salvos em {arquivo_saida}")

def main():
    try:
        print("Atualizando taxas de câmbio...")
        dados_atualizados = taxas_atualizadas()
        salvar_cotacoes(dados_atualizados)
        
        print("Taxas de câmbio atualizadas com sucesso!")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()