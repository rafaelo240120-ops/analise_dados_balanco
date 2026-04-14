import pandas as pd
import requests
import yfinance as yf

# Importa as bibliotecas: pandas (tabelas), requests (API), yfinance (Ibovespa)

base_url = "https://laboratoriodefinancas.com/api/v2"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTgwNzA5NjM3MiwiaWF0IjoxNzc1NTYwMzcyLCJqdGkiOiJlNDdiZjIxZTVjZGU0MDk2YjRlMTQ1MmUzN2M4ZDY0YiIsInVzZXJfaWQiOiI5OSJ9.eMgu6ySiRUTkoAjWJOGGXXh4u9BO1gtXeP4p9vtD2tc"

#  1. PLANILHÃO 
resp = requests.get(
    f"{base_url}/bolsa/planilhao",
    headers={"Authorization": f"Bearer {token}"},
    params={"data_base": "2021-04-01"},
)
resp.status_code()  #**

dados = resp.json()
df = pd.DataFrame(dados)

#  2. MAGIC FORMULA 
df2 = df[["ticker", "roic", "earning_yield"]]
# Filtra só as colunas que interessam

df2['rank_roic'] = df2['roic'].rank(ascending=False)
df2['rank_p_ey'] = df2['earning_yield'].rank(ascending=False)
# Ranqueia: maior ROIC e maior Earning Yield 

df2['rank_final'] = (df2['rank_roic'] + df2['rank_p_ey']) / 2
# Combina os dois ranks em um score único (média)

carteira = df2.sort_values('rank_final', ascending=False)['ticker'][:20]
# Ordena pelo rank final e pega as 20 melhores ações

#  3. RETORNO DE CADA AÇÃO 
data_ini = "2021-04-01"
data_fim = "2026-03-30"

retornos = []
for ticker in carteira:
    # Loop: percorre cada uma das 20 ações da carteira
    try:
        resp = requests.get(
            f"{base_url}/preco/corrigido",
            headers={"Authorization": f"Bearer {token}"},
            params={"ticker": ticker, "data_ini": data_ini, "data_fim": data_fim},
        )

        df_preco = pd.DataFrame(resp.json())

        if df_preco.empty or len(df_preco) < 2:
            print(f"  Sem dados: {ticker}")
            continue
        # Pula o ticker se não tiver dados suficientes

        preco_ini = float(df_preco["fechamento"].iloc[0])
        preco_fim = float(df_preco["fechamento"].iloc[-1])
        # Pega o primeiro e o último preço do período

        retorno = (preco_fim / preco_ini - 1) * 100
        # Calcula o retorno total: (preço final / preço inicial - 1) × 100

        retornos.append({"ticker": ticker, "retorno_5Y_%": round(retorno, 2)})
        # Adiciona o resultado na lista

    except Exception as e:
        print(f"  Erro {ticker}: {e}")
        # Se der qualquer erro, imprime e segue para o próximo ticker

df_ret = pd.DataFrame(retornos).sort_values("retorno_5Y_%", ascending=False)
# Transforma a lista em DataFrame e ordena do maior para o menor retorno

#  4. IBOVESPA 
ibov = yf.download("^BVSP", start=data_ini, end=data_fim, auto_adjust=True, progress=False)
close = ibov["Close"].squeeze()
ret_ibov = (float(close.iloc[-1]) / float(close.iloc[0]) - 1) * 100
# Calcula o retorno do Ibovespa no mesmo período

# 5. PONDERAÇÃO ─
df_ret["peso"] = 0.05
# Atribui 5% para cada ação (20 ações × 5% = 100%)

ret_carteira = (df_ret["retorno_5Y_%"] * df_ret["peso"]).sum()
# Multiplica o retorno de cada ação pelo seu peso e soma — retorno total da carteira

#  6. RESULTADO 
print(df_ret.to_string(index=False))
print(f"\nRetorno médio carteira : {ret_carteira:.2f}%")
print(f"Retorno Ibovespa       : {ret_ibov:.2f}%")
print(f"Alpha                  : {ret_carteira - ret_ibov:.2f}%")
