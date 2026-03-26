import requests
import pandas as pd

base_url = "https://laboratoriodefinancas.com/api/v2"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc3MTE4MDM4LCJpYXQiOjE3NzQ1MjYwMzgsImp0aSI6ImI3YWY2NjZiOWIxZjQzYjlhMmI2ZmVhOGFiOGM0ZmVkIiwidXNlcl9pZCI6Ijk5In0.gBQfgMUQxuFm0kh-s5YAYbGKRhazQK3Hl-DVYarMCqM"
resp = requests.get(
    f"{base_url}/bolsa/planilhao",
    headers={"Authorization": f"Bearer {token}"},
    params={"data_base": "2025-03-23"},
)
dados =resp.json()
df = pd.DataFrame(dados)
df2 = df[["ticker", "roe", "p_vp"]]
df2 = df2.assign(rank_roe=df2["roe"].rank(ascending=False))
df2 = df2.assign(rank_p_vp=df2["p_vp"].rank(ascending=True))
df2 = df2.assign(rank_final=df2["rank_roe"] + df2["rank_p_vp"])


print(type(dados))
print(dados)

df2 = df2.sort_values("rank_final", ascending=False)


import requests

base_url = "https://laboratoriodefinancas.com/api/v2"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc3MTE4MDM4LCJpYXQiOjE3NzQ1MjYwMzgsImp0aSI6ImI3YWY2NjZiOWIxZjQzYjlhMmI2ZmVhOGFiOGM0ZmVkIiwidXNlcl9pZCI6Ijk5In0.gBQfgMUQxuFm0kh-s5YAYbGKRhazQK3Hl-DVYarMCqM"
params = {"ticker": "MNPR3", "data_ini": "2025-03-21", "data_fim": "2026-03-23"}
resp = requests.get(
    f"{base_url}/preco/corrigido",
    headers={"Authorization": f"Bearer {token}"},
    params=params,
)
dados = resp.json()
df_preco = pd.DataFrame(dados)

#Rendimento
filtro1 = df_preco["data"] == "2026-03-23"
preco_final = df_preco[filtro1]["fechamento"].iloc[0]
precos_final = float(preco_final)
filtro2 = df_preco["data"] == "2025-03-21"
preco_inicial = df_preco[filtro2]["fechamento"].iloc[0]
preco_inicial = float(preco_inicial)
(preco_final / preco_inicial - 1) * 100

#API ibovespa
import yfinance as yf
#get ticker data
ibov = yf.download("^BVSP", start="2025-03-21")
filtro1 = ibov.index == "2025-03-21"
ibov_inicial = ibov[filtro1]["Close"].iloc[0]
filtro2 = ibov.index == "2026-03-23"
ibov_final = ibov[filtro2]["Close"].iloc[0]
(ibov_final/ibov_inicial-1) * 100 



