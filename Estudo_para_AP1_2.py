import pandas as pd
import requests


# ============================================================
# LISTA E DICIONÁRIO
# ============================================================

# LISTA:
# - usa colchetes [ ]
# - é uma sequência ORDENADA de elementos
# - acessamos pelo ÍNDICE (posição numérica começando no 0)

frutas = ["maçã", "banana", "laranja", "uva"]
frutas[0]   # "maçã"   → primeiro elemento (índice 0)
frutas[1]   # "banana" → segundo elemento  (índice 1)
frutas[3]   # "uva"    → quarto elemento   (índice 3)

# DICIONÁRIO:
# - usa chaves { }
# - NÃO tem posição/ordem
# - acessamos pelo NOME DA CHAVE
# - cada item é um par chave: valor

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

# Fazemos o download do arquivo, copiamos o caminho e lemos como DataFrame (df)
# O "r" antes da string permite usar as barras normais do Windows sem precisar escapar

df = pd.read_csv(r"arquivo.csv")       # para arquivos .csv
df = pd.read_excel(r"arquivo.xlsx")    # para arquivos .xlsx


# ============================================================
# INSPEÇÃO INICIAL
# ============================================================

# Funções para explorar o DataFrame logo após ler os dados:

df.shape             # retorna (nº de linhas, nº de colunas)
df.dtypes            # mostra o tipo de cada coluna:
                     #   object  → texto (str)
                     #   int64   → número inteiro
                     #   float64 → número com decimal
df.isnull().sum()    # conta quantos valores nulos (vazios) há em cada coluna
df.head()            # mostra as primeiras 5 linhas
df.columns           # lista os nomes de todas as colunas


# ============================================================
# FILTROS
# ============================================================

# Um filtro cria uma "máscara" de True/False para cada linha.
# Depois aplicamos com .loc para exibir só as linhas que interessam.

# ----- 1. FILTRO NUMÉRICO -----
# Quando a coluna é número e você quer comparar valores.
# Operadores: >  <  >=  <=  ==

filtro = df["score"] > 90           # linhas onde score é maior que 90
filtro = df["world_rank"] <= 100    # linhas onde rank é até 100
filtro = df["valor"] == 5000        # linhas onde valor é exatamente 5000

# Situações: "mostre universidades com score > 90", "ranks entre 50 e 100"

# ----- 2. FILTRO DE TEXTO EXATO -----
# Quando você quer correspondência EXATA com um valor de texto.
# Usa o operador ==

filtro = df["country"] == "Brazil"      # só linhas onde country é exatamente "Brazil"
filtro = df["company_size"] == "L"      # só linhas onde company_size é "L"

# Situações: "mostre só o Brasil", "só empresas grandes"

# ----- 3. FILTRO DE TEXTO PARCIAL -----
# Quando você quer texto que CONTÉM algo, não precisa ser exato.
# Usa .str.contains()

filtro = df["institution"].str.contains("^C")             # começa com a letra C (^ = início)
filtro = df["nome"].str.contains("Pedro", case=False)     # contém "Pedro", ignora maiúscula
filtro = df["SERNOME"].str.contains("bovino", case=False) # contém "bovino", ignora maiúscula

# Situações: "universidades cujo nome começa com C", "passageiros com nome John"

# ----- 4. FILTRO COMBINADO -----
# Quando tem mais de uma condição ao mesmo tempo.
# IMPORTANTE: cada condição deve estar entre parênteses ( ), senão dá erro!

# & = E → as DUAS condições precisam ser verdade
filtro = (df["country"] == "US") & (df["score"] > 80)

# | = OU → basta UMA das condições ser verdade
filtro = (df["country"] == "Brazil") | (df["country"] == "Argentina")

# ----- 5. APLICANDO O FILTRO COM .loc -----
# Depois de criar o filtro, usamos .loc para aplicar e escolher quais colunas mostrar.

df.loc[filtro]                                    # retorna todas as colunas
df.loc[filtro, ["institution", "country"]]        # retorna só as colunas escolhidas

# COLA RÁPIDA — qual filtro usar?
# coluna numérica?   → > < >= <= ==
# texto exato?       → == "valor"
# texto parcial?     → .str.contains("algo")
# duas condições?    → (filtro1) & (filtro2)
# uma ou outra?      → (filtro1) | (filtro2)


# ============================================================
# CRIAR NOVA COLUNA
# ============================================================

# Para criar uma nova coluna, basta "chamar" o df com o novo nome
# e definir o que ela é com base nas colunas existentes.

df["ticket_medio"] = df["vendas"] / df["clientes"]   # divisão entre colunas
df["meta_batida"] = df["vendas"] >= 13000            # retorna True ou False por linha


# ============================================================
# RANKEAR E ORDENAR
# ============================================================

# ----- .rank() — RANKEAR -----
# Cria uma NOVA COLUNA com a posição/pontuação de cada linha.
# O DataFrame NÃO muda de ordem, cada linha só ganha um número.
# ascending=False → maior valor recebe posição 1 (rank do melhor)
# ascending=True  → menor valor recebe posição 1

df["rank_roic"] = df["roic"].rank(ascending=False)
df["rank_ey"]   = df["earning_yield"].rank(ascending=False)

# Exemplo visual:
# ANTES:                  DEPOIS:
# ticker  roic            ticker  roic  rank_roic
# PETR4   0.35            PETR4   0.35      3
# VALE3   0.52            VALE3   0.52      1
# ITUB4   0.41            ITUB4   0.41      2

# combinando dois ranks num score final (Magic Formula)
df["rank_final"] = (df["rank_roic"] + df["rank_ey"]) / 2

# ----- .sort_values() — ORDENAR -----
# Reordena as linhas do DataFrame pelo valor de uma coluna.
# Usado depois do rank para pegar os melhores.

carteira = df.sort_values("rank_final").head(20)   # os 20 menores ranks (melhores)

# RESUMO:
# rank()        → quando você quer PONTUAR cada linha para usar depois em cálculos
# sort_values() → quando você quer VER ou PEGAR os dados em ordem


# ============================================================
# CALCULAR MIN, MAX, MÉDIA E DESVIO PADRÃO
# ============================================================

# Seleciona a coluna com df["coluna"] e chama a função desejada:

df["score"].mean()   # média dos valores
df["score"].max()    # maior valor
df["score"].min()    # menor valor
df["score"].std()    # desvio padrão (o quanto os valores variam)


# ============================================================
# GROUPBY
# ============================================================

# O GroupBy agrupa as linhas pelo valor de uma coluna e calcula
# algo em cima de cada grupo. Pense assim:
# "Pega todas as linhas do Brasil → soma as vendas delas"
# "Pega todas as linhas dos EUA   → soma as vendas delas"
# ...e assim por diante para cada país.

# ESTRUTURA SEMPRE EM 3 PARTES:
# df.groupby("coluna_agrupadora")["coluna_calculada"].operacao()
#              ↑ 1. agrupar          ↑ 2. coluna         ↑ 3. calcular

df.groupby("country")["score"].sum()     # soma do score por país
df.groupby("country")["score"].mean()    # média do score por país
df.groupby("country")["score"].min()     # menor score por país
df.groupby("country")["score"].max()     # maior score por país
df.groupby("country")["score"].count()   # quantas linhas por país

# idxmax() → retorna o NOME DO GRUPO com maior valor (não o valor em si)
df.groupby("country")["score"].mean().idxmax()   # qual país tem maior média?

# ----- GROUPBY COM DOIS GRUPOS -----
# Agrupa por combinação de duas colunas.
# Forma um grupo para cada combinação: Brasil+ProdutoA, Brasil+ProdutoB, etc.

df.groupby(["nome_pais", "descricao"])["valor"].sum()

# ----- GROUPBY COM VÁRIOS CÁLCULOS AO MESMO TEMPO → .agg() -----
# Em vez de rodar um cálculo por vez, você pede tudo de uma vez
# e já nomeia cada coluna nova.

resumo = df.groupby("filial").agg(
    total_vendas   = ("vendas", "sum"),        # soma de vendas por filial
    media_ticket   = ("ticket_medio", "mean"), # média do ticket por filial
    total_clientes = ("clientes", "sum")       # soma de clientes por filial
).reset_index()

# ----- .reset_index() -----
# O groupby transforma a coluna agrupadora em índice (fica "presa" como cabeçalho).
# O reset_index() devolve ela como coluna normal.
#
# Sem reset_index:         Com reset_index:
# filial                    filial  total_vendas
# Centro  39600          0  Centro        39600
# Norte   30700          1  Norte         30700

# COLA RÁPIDA — qual groupby usar?
# "total por país"       → groupby("pais")["valor"].sum()
# "média por ano"        → groupby("ano")["score"].mean()
# "quantos por país"     → groupby("pais")["col"].count()
# "quem tem maior média" → groupby("pais")["score"].mean().idxmax()
# "resumo completo"      → groupby().agg(...)


# ============================================================
# API COM REQUESTS
# ============================================================

# API = forma de pedir dados a um servidor pela internet via código.
# Em vez de abrir um site, você manda um pedido e recebe dados de volta.
# Fluxo: seu código → requisição → servidor → resposta (JSON) → DataFrame

# ----- ESTRUTURA PADRÃO (sem token, sem filtro) -----

url = "https://brasilapi.com.br/api/banks/v1"   # 1. define o endereço
response = requests.get(url)                     # 2. faz o pedido

# 3. verifica se funcionou (ATENÇÃO: é atributo, sem parênteses!)
response.status_code
# 200 → funcionou
# 404 → endereço não existe
# 401 → precisa de token/autenticação
# 500 → erro no servidor

dados = response.json()      # 4. converte a resposta para dicionário/lista Python
df = pd.DataFrame(dados)     # 5. transforma em DataFrame

# ----- COM PARÂMETROS (filtros na URL) -----
# Alguns endpoints aceitam filtros. Passamos como dicionário em params=.
# É como dizer ao servidor: "me manda os dados, mas só de 2024".

params = {
    "formato": "json",
    "dataInicial": "01/01/2024",
    "dataFinal": "31/12/2024"
}
response = requests.get(url, params=params)

# ----- COM TOKEN (autenticação) -----
# Algumas APIs são protegidas. O token vai no headers=, não no params=.

token = "eyJhbGci..."
response = requests.get(
    url,
    headers={"Authorization": f"Bearer {token}"}
)

# ----- COM TOKEN E PARÂMETROS -----
response = requests.get(
    url,
    headers={"Authorization": f"Bearer {token}"},
    params={"data_base": "2021-04-01"}
)

# RESUMO: headers= → onde vai o token | params= → onde vão os filtros

# ----- FORMATOS DE RESPOSTA JSON -----
# O JSON que volta pode ter estruturas diferentes. Veja como tratar cada uma:

# Formato 1: lista de dicionários → direto pro DataFrame
# Ex: [{"nome": "Banco X", "codigo": 1}, {"nome": "Banco Y", "codigo": 2}]
dados = response.json()
df = pd.DataFrame(dados)

# Formato 2: dicionário com chave → precisa entrar na chave primeiro
# Ex: {"value": [{"SERCODIGO": "...", "SERNOME": "..."}, ...]}
dados = response.json()
dados = dados["value"]       # entra na chave "value" antes de virar DataFrame
df = pd.DataFrame(dados)

# Formato 3: JSON aninhado (objetos dentro de objetos) → usa json_normalize
# Ex: [{"estado": "SP", "municipios": [{"nome": "São Paulo"}, ...]}]
dados = response.json()
dados = dados[0]["municipios"]    # navega pela estrutura até os dados que quer
df = pd.json_normalize(dados)     # "planifica" o JSON aninhado em colunas

# COLA RÁPIDA — qual usar?
# sem token, sem filtro    → requests.get(url)
# com filtro               → requests.get(url, params={...})
# com token                → requests.get(url, headers={"Authorization": f"Bearer {token}"})
# com token e filtro       → requests.get(url, headers={...}, params={...})
# resposta direta          → pd.DataFrame(response.json())
# resposta com chave       → pd.DataFrame(response.json()["value"])
# resposta aninhada        → pd.json_normalize(dados)