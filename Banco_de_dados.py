import sqlite3
import pandas as pd
#Banco de Dados SQLite
nome_db = "cadastro_estudantes.db"
#Criar a conexão com o banco de dados
conn = sqlite3.connect(nome_db)
#Trazer para dentro do Pandas os dados das tabelas do banco de dados
query = "select * from tb_alunos"
df_alunos = pd.read_sql(query, conn)
query = "select * from tb_enderecos"
df_enderecos = pd.read_sql(query, conn)
#Merge entre tb_alunos e tb_enderecos
df = pd.merge(df_alunos, df_enderecos, left_on="endereco_id", right_on="id", how="inner")
df[["nome_aluno", "email", "endereco"]]

