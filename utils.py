from datetime import datetime
import pyautogui
import requests
import json
import os
from config import API_KEY, url, url1
import pandas as pd
from log_config import configurar_logger

# Função para classificar o tipo de estabelecimento

def classificar_tipo(types):
    if "restaurant" in types:
        return "Restaurante"
    if "gym" in types:
        return "Academia"
    if "ice_cream" in types or "food" in types:
        return "Sorveteria"
    return "Outro"

# Função para buscar lugares na API do Google

def api_places(texto):
    logger = configurar_logger("Utils-API")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Nome do arquivo JSON
    NOME_ARQUIVO = f"resultados_places_{timestamp}.json"

    # Caminho da pasta onde está o .py
    PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))

    # Caminho completo do arquivo JSON
    CAMINHO_JSON = os.path.join(PASTA_SCRIPT, NOME_ARQUIVO)

    # Parâmetros da requisição
    try:
        params = {
            "query": texto,
            "key": API_KEY
        }
        logger.info(f"buscando os places IDs")
        # Pesquisa e recebe os places Ids dos lugares encontrados
        response = requests.get(url, params=params)
        dados = response.json()
        if dados.get("status") == "REQUEST_DENIED":
            logger.error(f"API Key inválida ou sem permissão: {dados.get('error_message')}")
            pyautogui.alert(
                text='Chave da API inválida ou sem permissão. O programa será encerrado.',
                title='Aviso',
                button='OK'
            )
            exit()

        if dados.get("status") != "OK":
            logger.error(f"Erro retornado pela API: {dados.get('status')}")
            pyautogui.alert(
                text='Erro retornado pela API. O programa será encerrado.',
                title='Aviso',
                button='OK'
            )
            exit()
        placeid = [id["place_id"] for id in dados["results"][:5]]
        logger.info(f"Places IDs foram  encontrados")
        resultados = []
    except Exception as e:
        logger.error(f"Erro ao buscar places IDs: {e}")
        return
    
    logger.info(f"Buscando detalhes dos lugares encontrados")
    # Para cada place Id, busca os detalhes do lugar
    try:
        for pid in placeid:
            params = {
                "place_id": pid,
                "fields": "name,types,rating,user_ratings_total,formatted_address",
                "language": "pt-BR",
                "key": API_KEY
            }

            # Faz a requisição para obter os detalhes dos lugares encontrados

            res = requests.get(url1, params=params)
            detalhes = res.json().get("result", {})

            resultados.append({
                "nome": detalhes.get("name"),
                "tipo": classificar_tipo(detalhes.get("types", [])),
                "nota": detalhes.get("rating"),
                "avaliacoes": detalhes.get("user_ratings_total"),
                "endereco": detalhes.get("formatted_address")
            })
    except Exception as e:
        logger.error(f"Erro ao buscar detalhes dos lugares: {e}")
        return

    # Coloca em forma de dicionário para salvar em JSON
    jsonfinal = {"resultados": resultados}

    # Salva o arquivo JSON com os resultados
    logger.info("Salvando os detalhes dos lugares no arquivo JSON")
    with open(CAMINHO_JSON, "w", encoding="utf-8") as f:
        json.dump(jsonfinal, f, ensure_ascii=False, indent=2)
    logger.info("Arquivo JSON ferado.")
    # Retorna os resultados para uso posterior
    logger.info(f"Detalhes dos lugares foram obtidos com sucesso")
    return jsonfinal


# Função para gerar o arquivo Excel com os resultados
def gerarexcel(resultado):
    nome = []
    tipo = []
    nota = []
    avaliacoes = []
    endereco = []
    logger = configurar_logger("Utils-Excel")
    # Extrai os dados do resultado e organiza em listas
    logger.info("Extraindo dados para o Excel")
    for item in resultado.get("resultados", []):
        nome.append(item.get("nome"))
        tipo.append(item.get("tipo"))
        nota.append(item.get("nota"))
        avaliacoes.append(item.get("avaliacoes"))
        endereco.append(item.get("endereco"))

    # Define as colunas e as informações para o DataFrame
    logger.info("Gerando DataFrame para o Excel")
    dados = {
        "Nome": nome,
        "Tipo": tipo,
        "Nota": nota,
        "Avaliações": avaliacoes,
        "Endereço": endereco
    }

    # Cria o DataFrame e salva em um arquivo Excel com timestamp como nome
    tabela = pd.DataFrame(dados)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    tabela.to_excel(f"lugares-{timestamp}.xlsx", index=False)
    logger.info("Arquivo Excel gerado com sucesso")
