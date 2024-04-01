#Função para juntar todos as tabelas filtradas
import pandas as pd

def juntar_tabelas(dataframe, coluna, valor):
    df_concatenado = pd.concat(dataframe)

    concatenado = df_concatenado.groupby(coluna)[valor].sum()


    return concatenado.reset_index()