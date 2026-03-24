import requests
import pandas as pd

base_url = "https://laboratoriodefinancas.com/api/v2"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc2NTEyNTA4LCJpYXQiOjE3NzM5MjA1MDgsImp0aSI6IjJhMzc3ZjEwYmY0NjRjOGU5NzFmNTZlZDYwYmE2OWYzIiwidXNlcl9pZCI6Ijk5In0.71YX2ayZ8MOuXfjOW0z8zWGP13W8NjyUZjKGsa3VNf0"
resp = requests.get(
    f"{base_url}/bolsa/planilhao",
    headers={"Authorization": f"Bearer {token}"},
    params={"data_base": "2026-03-23"},
)
dados =resp.json()
df = pd.DataFrame(dados)
maximo = df["roe"].max()
filtro = df["roe"] == maximo
df[filtro]

import requests

base_url = "https://laboratoriodefinancas.com/api/v2"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc2NTEyNTA4LCJpYXQiOjE3NzM5MjA1MDgsImp0aSI6IjJhMzc3ZjEwYmY0NjRjOGU5NzFmNTZlZDYwYmE2OWYzIiwidXNlcl9pZCI6Ijk5In0.71YX2ayZ8MOuXfjOW0z8zWGP13W8NjyUZjKGsa3VNf0"
params = {"ticker": "MNPR3", "data_ini": "2025-03-21", "data_fim": "2026-03-23"}
resp = requests.get(
    f"{base_url}/preco/corrigido",
    headers={"Authorization": f"Bearer {token}"},
    params=params,
)
dados = resp.json()
df_preco = pd.DataFrame(dados)

#Rendimento
#Jeito 1
df_preco["rendimento"] = df_preco["fechamento"].pct_change() * 100
df_preco["rendimento_acumulado"] = (1 + df_preco["rendimento"] / 100).cumprod() - 1
df_preco["rendimento_acumulado"] = df_preco["rendimento_acumulado"] * 100

df_preco[["data", "fechamento", "rendimento", "rendimento_acumulado"]]

#Jeito 2

filtro = df_preco["data"] == "2026-03-23"
preco_final = df_preco[filtro]["fechamento"].iloc[0]
filtro = df_preco["data"] == "2025-03-21"
preco_inicial = df_preco[filtro]["fechamento"].iloc[0]
rendimento = (preco_final / preco_inicial - 1) * 100
rendimento

#ibovespa

import requests

base_url = "https://laboratoriodefinancas.com/api/v2"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc2NTEyNTA4LCJpYXQiOjE3NzM5MjA1MDgsImp0aSI6IjJhMzc3ZjEwYmY0NjRjOGU5NzFmNTZlZDYwYmE2OWYzIiwidXNlcl9pZCI6Ijk5In0.71YX2ayZ8MOuXfjOW0z8zWGP13W8NjyUZjKGsa3VNf0"

params = {"ticker": "ibov", "data_ini": "2025-03-21", "data_fim": "2026-03-23"}
resp = requests.get(
    f"{base_url}/preco/diversos",
    headers={"Authorization": f"Bearer {token}"},
    params=params,
)
dados = resp.json()
df_ibov = pd.DataFrame(dados)
filtro1 = df_ibov["data"] == "2026-03-20"
preco_final = df_ibov[filtro1]["fechamento"].iloc[0]
preco_final = float(preco_final)
filtro2 = df_ibov["data"] == "2025-06-02"
preco_inicial = df_ibov[filtro2]["fechamento"].iloc[0]
preco_inicial = float(preco_inicial)

preco_final/preco_inicial-1