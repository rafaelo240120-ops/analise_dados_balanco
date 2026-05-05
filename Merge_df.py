import requests
import pandas as pd

base_url = "https://laboratoriodefinancas.com/api/v2"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzgwNTcwMTYzLCJpYXQiOjE3Nzc5NzgxNjMsImp0aSI6ImY5YTdmMjExNjBiMzQ3MTU4ZTg4NzA1NzQ0N2UyYTc3IiwidXNlcl9pZCI6Ijk5In0.Z2fBABvjtEqYTUHp-7OmRb1PmuK8A_p5nAm04wqfEIo"

#Ibov
params = {"ticker": "ibov", "data_ini": "2000-01-01", "data_fim": "2025-12-31"}
resp = requests.get(
    f"{base_url}/preco/diversos",
    headers={"Authorization": f"Bearer {token}"},
    params=params,
)
dados = resp.json()
ibov = pd.DataFrame(dados)

#Dolar
params_dolar = {"ticker": "usd_brl", "data_ini": "2000-01-01", "data_fim": "2025-12-31"}
resp_dolar = requests.get(
    f"{base_url}/preco/diversos",
    headers={"Authorization": f"Bearer {token}"},
    params=params_dolar,
)
dados_dolar = resp_dolar.json()
dolar = pd.DataFrame(dados_dolar)

#Garantir que os campos sejam do tip Datatime
ibov["data"] = pd.to_datetime(ibov["data"])
dolar["data"] = pd.to_datetime(dolar["data"])

#Selecionar apenas o preco de fechamento
ibov = ibov[["data", "fechamento"]]
dolar = dolar[["data", "fechamento"]]

#renomeiar as colunas 
ibov = ibov.rename(columns={"fechamento": "ibov"})
dolar = dolar.rename(columns={"fechamento": "dolar"})

# Trasnforma para float 
ibov["ibov"] = ibov["ibov"].astype(float)
dolar["dolar"] = dolar["dolar"].astype(float)

#Merge entre os dois DataFrames através do campo data
df = pd.merge(ibov, dolar, on="data", how="inner")

# Correlação 

df[["ibov", "dolar"]].corr()

# Criação do df de datas
datas = pd.date_range(start="2000-01-01", end="2025-12-31", freq="B") #freq = B para considerar apenas dias úteis
df_base = pd.DataFrame({"data": datas})
df_base = pd.merge(df_base, ibov, on="data", how="left")
df_base = pd.merge(df_base, dolar, on="data", how="left")

#tratamento dos dados faltantes
df_base.isna().sum()
df_base.dropna()
df_base.ffill() # forward fill - preenche os valores faltantes com o valor mais próximo anterior
df_base.bfill() # backward fill - preenche os valores faltantes com o valor mais próximo posterior

# 
df["ret_ibov"] = df["ibov"].pct_change() # calcula a variação percentual do ibov
df["ret_dolar"] = df["dolar"].pct_change() # calcula a variação percentual do dolar

import seaborn as sn

corr = df[["ret_ibov", "ret_dolar"]].corr()
sn.heatmap(corr, annot=True)

#histograma
sn.histplot(df["ret_ibov"], kde=True)

#Boxplot
sn.boxplot(df["ret_ibov"])

# Line
sn.lineplot(df["ret_ibov"])