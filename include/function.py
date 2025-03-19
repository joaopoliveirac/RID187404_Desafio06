import pandas as pd
import os
from datetime import datetime

def upload_raw_data_to_bronze(nome_arquivo):
    caminho = os.path.join(os.path.dirname(__file__), '..', 'data', nome_arquivo) #obtem o diretorio onde o script ta rodando, sobe um nivel, entra na pasta data e aponta pro arquivo que passou
    df = pd.read_csv(caminho)
    caminho_arquivo_bronze = os.path.join(os.path.dirname(__file__), '..', 'data', 'bronze', 'dados_bronze.csv')
    df.to_csv(caminho_arquivo_bronze, index=False)
    

def process_bronze_to_silver(nome_arquivo):
    caminho = os.path.join(os.path.dirname(__file__), '..', 'data','bronze', nome_arquivo)
    df = pd.read_csv(caminho)
    df.dropna(inplace=True) #dropna remove todas as linhas que possuem pelo menos um valor nulo, inplace aplica direto no df
    df['date_of_birth'] = pd.to_datetime(df['date_of_birth'])
    df['signup_date'] = pd.to_datetime(df['signup_date'])
    df['email'] = df['email'].apply(lambda x: x[:len(x)//2] + '@' + x[len(x)//2:] if '@' not in x else x) #como possui varios tipos de dominions, exemplo example.org, example.net etc esse codigo insere o @ no meio do e-mail, antes do domínio, de forma mais geral, sem se preocupar com o tipo de domínio.
    df['idade'] = df['date_of_birth'].apply(lambda x: (datetime.now() - x).days // 365)
    caminho_arquivo_silver = os.path.join(os.path.dirname(__file__), '..', 'data', 'silver', 'dados_silver.csv')
    df.to_csv(caminho_arquivo_silver, index=False)

def process_silver_to_gold(nome_arquivo):
    caminho = os.path.join(os.path.dirname(__file__), '..', 'data','silver', nome_arquivo)
    df = pd.read_csv(caminho)
    bins = list(range(0, 101, 10))  # Cria intervalos: 0-10, 11-20 ...
    labels = [f"{i}-{i+9}" for i in range(0, 100, 10)]
    df['faixa_etaria'] = pd.cut(df['idade'], bins=bins, labels=labels, right=False)
    agrupados = df.groupby(['faixa_etaria', 'subscription_status'], observed=False).size().reset_index(name='quantidade')
    caminho_arquivo_gold = os.path.join(os.path.dirname(__file__), '..', 'data', 'gold', 'dados_gold.csv')
    caminho_arquivo_gold_agrupados = os.path.join(os.path.dirname(__file__), '..', 'data', 'gold', 'dados_agrupados.csv')
    df.to_csv(caminho_arquivo_gold)
    agrupados.to_csv(caminho_arquivo_gold_agrupados)
    return df









    







