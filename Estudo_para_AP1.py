import pandas as pd
import requests

# ============================================================
# LISTA E DICIONÁRIO
# ============================================================

# LISTA: sequência ordenada, acesso por índice (começa no 0)
frutas = ["maçã", "banana", "laranja", "uva"]
frutas[0]   # "maçã"
frutas[1]   # "banana"
frutas[3]   # "uva"

# DICIONÁRIO: acesso por chave (sem posição)
aluno = {
    "nome": "Rafael Diniz",
    "idade": 21,
    "curso": "Ciências Econômicas"
}
aluno["nome"]   # "Rafael Diniz"
aluno["idade"]  # 21


# ============================================================
# LEITURA DE DADOS
# ============================================================

df = pd.read_csv(r"arquivo.csv")
df = pd.read_excel(r"arquivo.xlsx")
# o r antes do caminho permite usar barras normais


# ============================================================
# INSPEÇÃO INICIAL
# ============================================================

df.shape            # (linhas, colunas)
df.dtypes           # tipos de cada coluna: object=texto, int64=inteiro, float64=decimal
df.isnull().sum()   # conta valores nulos por coluna
df.head()           # primeiras 5 linhas
df.columns          # nomes das colunas


# ============================================================
# FILTROS
# ============================================================

# 1. NUMÉRICO: coluna é número → usa > < >= <= ==
filtro = df["score"] > 90
filtro = df["world_rank"] <= 100
filtro = df["valor"] == 5000

# 2. TEXTO EXATO: correspondência exata com ==
filtro = df["country"] == "Brazil"
filtro = df["company_size"] == "L"

# 3. TEXTO PARCIAL: usa .str.contains()
filtro = df["institution"].str.contains("^C")           # começa com C (regex)
filtro = df["nome"].str.contains("Pedro", case=False)   # ignora maiúscula/minúscula
filtro = df["SERNOME"].str.contains("bovino", case=False)

# 4. FILTRO COMBINADO
# & = E (as duas condições precisam ser verdade)
filtro = (df["country"] == "US") & (df["score"] > 80)
# | = OU (basta uma ser verdade)
filtro = (df["country"] == "Brazil") | (df["country"] == "Argentina")
# IMPORTANTE: cada condição precisa estar entre parênteses ()

# 5. APLICANDO O FILTRO COM .loc
df.loc[filtro]                                          # todas as colunas
df.loc[filtro, ["institution", "country"]]              # só colunas escolhidas

# RESUMO RÁPIDO DE FILTROS:
# coluna numérica?  → > < >= <= ==
# texto exato?      → == "valor"
# texto parcial?    → .str.contains("algo")
# duas condições?   → (filtro1) & (filtro2)
# uma ou outra?     → (filtro1) | (filtro2)


# ============================================================
# CRIAR NOVA COLUNA
# ============================================================

# basta definir o nome da nova coluna com base nas existentes
df["ticket_medio"] = df["vendas"] / df["clientes"]
df["meta_batida"] = df["vendas"] >= 13000   # retorna True/False


# ============================================================
# RANKEAR E ORDENAR
# ============================================================

# .rank() → cria coluna de posição sem mudar a ordem do df
df["rank_roic"] = df["roic"].rank(ascending=False)          # maior valor = posição 1
df["rank_ey"] = df["earning_yield"].rank(ascending=False)

# combinando dois ranks num score final
df["rank_final"] = (df["rank_roic"] + df["rank_ey"]) / 2

# .sort_values() → reordena o df
carteira = df.sort_values("rank_final").head(20)   # os 20 melhores

# RESUMO:
# rank()        → pontua cada linha (para usar depois em cálculos)
# sort_values() → ordena para ver ou pegar os dados


# ============================================================
# ESTATÍSTICAS: MIN, MAX, MÉDIA, DESVIO PADRÃO
# ============================================================

df["score"].mean()   # média
df["score"].max()    # maior valor
df["score"].min()    # menor valor
df["score"].std()    # desvio padrão


# ============================================================
# GROUPBY
# ============================================================

# estrutura sempre em 3 partes:
# df.groupby("coluna_agrupadora")["coluna_calculada"].operacao()

df.groupby("country")["score"].sum()    # soma
df.groupby("country")["score"].mean()   # média
df.groupby("country")["score"].min()    # menor
df.groupby("country")["score"].max()    # maior
df.groupby("country")["score"].count()  # quantidade
df.groupby("country")["score"].mean().idxmax()  # país com maior média (retorna o NOME)

# groupby com dois grupos (combinação)
df.groupby(["nome_pais", "descricao"])["valor"].sum()

# groupby com vários cálculos ao mesmo tempo → .agg()
resumo = df.groupby("filial").agg(
    total_vendas   = ("vendas", "sum"),
    media_ticket   = ("ticket_medio", "mean"),
    total_clientes = ("clientes", "sum")
).reset_index()
# .reset_index() transforma a coluna agrupadora de índice de volta em coluna normal

# RESUMO DE DECISÃO:
# "total por país"       → groupby("pais")["valor"].sum()
# "média por ano"        → groupby("ano")["score"].mean()
# "quantos por país"     → groupby("pais")["col"].count()
# "quem tem maior média" → groupby("pais")["score"].mean().idxmax()
# "resumo completo"      → groupby().agg(...)


# ============================================================
# API COM REQUESTS
# ============================================================

# fluxo: seu código → requisição → servidor → resposta (JSON) → DataFrame

# ESTRUTURA PADRÃO (sem token, sem filtro)
url = "https://brasilapi.com.br/api/banks/v1"
response = requests.get(url)
response.status_code    # 200=ok | 404=não existe | 401=precisa token | 500=erro servidor
dados = response.json()
df = pd.DataFrame(dados)

# COM PARÂMETROS (filtros na URL)
params = {
    "formato": "json",
    "dataInicial": "01/01/2024",
    "dataFinal": "31/12/2024"
}
response = requests.get(url, params=params)

# COM TOKEN (autenticação)
token = "eyJhbGci..."
response = requests.get(
    url,
    headers={"Authorization": f"Bearer {token}"}
)

# COM TOKEN E PARÂMETROS
response = requests.get(
    url,
    headers={"Authorization": f"Bearer {token}"},
    params={"data_base": "2021-04-01"}
)

# FORMATOS DE RESPOSTA JSON:

# resposta direta → lista de dicionários → direto pro DataFrame
dados = response.json()
df = pd.DataFrame(dados)

# resposta com chave → precisa entrar na chave primeiro
dados = response.json()
dados = dados["value"]
df = pd.DataFrame(dados)

# resposta aninhada → usa json_normalize
dados = response.json()
dados = dados[0]["municipios"]
df = pd.json_normalize(dados)

# ATENÇÃO: status_code é atributo, sem parênteses!
# response.status_code  ✅ CERTO
# response.status_code() ❌ ERRADO