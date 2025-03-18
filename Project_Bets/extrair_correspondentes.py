# Importar bibliotecas necessárias
import pandas as pd
import openpyxl

# Carregar o cabeçalho para verificar os nomes das colunas
df_cabecalho = pd.read_excel(
    r"C:\Users\gusta\OneDrive\Desktop\Projeto Python\Automacoes\Automacao_leads\Project_Bets\202503CORRESPONDENTES.xlsx",
    engine="openpyxl",
    nrows=1
)


# Definir as colunas que vamos utilizar
colunas_utilizadas = [
    "CNPJ da Contratante", 
    "Nome da Contratante", 
    "CNPJ do Correspondente",
    "Nome do Correspondente", 
    "Tipo de Instalação", 
    "Nº de Ordem da Instalação",
    "MUNICIPIO IBGE", 
    "Município da Instalação", 
    "UF",
    "Inc.I",
    "Inc.II", 
    "Inc.III", 
    "Inc.IV", 
    "Inc.V", 
    "Inc.VI", 
    "Inc.VIII"

]

colunas_utilizadas = [col.strip() for col in colunas_utilizadas]

# Ler apenas as colunas necessárias do Excel
df_colunas_utilizadas = pd.read_excel(
    r"C:\Users\gusta\OneDrive\Desktop\Projeto Python\Automacoes\Automacao_leads\Project_Bets\202503CORRESPONDENTES.xlsx",
    engine="openpyxl",
    usecols=colunas_utilizadas
)

novos_nomes_col = {
    "CNPJ da Contratante":"CnpjContratante",  
    "Nome da Contratante":"NomeContratante", 
    "CNPJ do Correspondente":"CnpjCorrespondente",
    "Nome do Correspondente":"NomeCorrespondente",
    "Tipo de Instalação":"Tipo",
    "Nº de Ordem da Instalação":"Ordem",
    "MUNICIPIO IBGE":"MunicipioIBGE",
    "Município da Instalação":"Municipio"
}

# renomeando as colunas antes de continuar o processo
df_colunas_utilizadas.rename(columns=novos_nomes_col, inplace=True)

# Definir colunas de CNPJ
colunas_cnpj = ["CnpjContratante","CnpjCorrespondente"]

df_colunas_utilizadas[colunas_cnpj] = df_colunas_utilizadas[colunas_cnpj].astype(str)
df_colunas_utilizadas[colunas_cnpj] = df_colunas_utilizadas[colunas_cnpj].apply(lambda x: x.str.zfill(8))

# Remover espaços das colunas que não quero
colunas_para_corrigir = ["NomeContratante","NomeCorrespondente","Ordem","Tipo","Municipio"]

df_colunas_utilizadas[colunas_para_corrigir] = df_colunas_utilizadas[colunas_para_corrigir].apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# Ajustar a coluna de Municipio q ta cagada

df_colunas_utilizadas["MunicipioIBGE"] = df_colunas_utilizadas["MunicipioIBGE"].astype(str).str.replace(".0","",regex=False)

# Identificar todas as colunas que começam com "Inc."
colunas_para_concatenar = [col for col in df_colunas_utilizadas.columns if col.startswith("Inc.")]

# Remover espaços em branco das colunas "Inc."
df_colunas_utilizadas.loc[:, colunas_para_concatenar] = df_colunas_utilizadas.loc[:, colunas_para_concatenar].apply(
    lambda x: x.str.strip() if x.dtype == "object" else x
)

# Substituir espaços vazios por None
df_colunas_utilizadas.loc[:, colunas_para_concatenar] = df_colunas_utilizadas.loc[:, colunas_para_concatenar].replace(r'^\s*$', None, regex=True)


# Criando a nova coluna "ServicosCorrespondentes" sem espaços e sem vírgulas desnecessárias
df_colunas_utilizadas["ServicosCorrespondentes"] = df_colunas_utilizadas[colunas_para_concatenar].apply(
    lambda row: ", ".join(row.dropna().astype(str).str.strip()).replace(", ,", ","), axis=1
)

# Remover as colunas originais "Inc." para manter apenas "ServicosCorrespondentes"
df_colunas_utilizadas.drop(columns=colunas_para_concatenar, inplace=True)

# Criando uma coluna para data

df_colunas_utilizadas["Posicao"]="2025-03-01"

# Mais um Print para ver o corpo do arquivo
#print(df_colunas_utilizadas[["MunicipioIBGE", "ServicosCorrespondentes","Posicao"]].head())

# Ordem das colunas do arquivo final

ordem_colunas = [
    "CnpjContratante",  
    "NomeContratante", 
    "CnpjCorrespondente",
    "NomeCorrespondente",
    "Tipo",
    "Ordem",
    "MunicipioIBGE",
    "Municipio",
    "UF",
    "ServicosCorrespondentes",
    "Posicao"
]

# Comando para fazer essa reogarnização

df_colunas_utilizadas = df_colunas_utilizadas.reindex(columns=ordem_colunas)


# Salvar o novo arquivo Excel corretamente
nome_arquivo = "bancocentral_correspbancario_20250317_00001.csv"
df_colunas_utilizadas.to_csv(nome_arquivo, index=False, sep=";", encoding="utf-8-sig")

# 📌 Mensagem que aparece quando o Excel é salvo corretamente
print(f"O Arquivo {nome_arquivo} Deu bom! Foguete não da RÉ kkkkkk🚀")
