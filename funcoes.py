#Função para juntar todos as tabelas filtradas
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Função para juntar todas as tabelas filtradas
def juntar_tabelas(dataframe, coluna, valor):
    dataset_concatenado = pd.concat(dataframe)

    concatenado = dataset_concatenado.groupby(coluna)[valor].sum()

    return concatenado.reset_index()

#Função para mostrar descrição da tabela
def descricao_tabela(dataframe, coluna, name):
    return dataframe[dataframe[coluna] == name].describe()

#Função para Montar o grafico dos mapas;
def mostraGraficoMap(maps_vct):

    bar_width = 0.35

    bar_positions = np.arange(len(maps_vct))

    fig, ax = plt.subplots(figsize=(11, 5))

    ax.barh(bar_positions + bar_width/2, maps_vct['Total Defender Side Win Percentage'], bar_width, label='Defesa', color='orange')

    ax.barh(bar_positions - bar_width/2, maps_vct['Total Attacker Side Win Percentage'], bar_width, label='Ataque', color='blue')

    ax.set_yticks(bar_positions)
    ax.set_yticklabels(maps_vct['Map'])
    ax.set_ylabel("Mapas")
    ax.set_xlabel('Porcentagem de Vitória')
    ax.set_title('Porcentagem de Vitória por Mapa e Lado')
    ax.legend(loc="lower right")

    plt.show()

#Função para Montar o grafico dos agentes
def mostraGraficoAgent(agents_vct):

    bar_width = 0.6  # Largura da barra
    bar_positions = np.arange(len(agents_vct))

    fig, ax = plt.subplots(figsize=(10, 8))

    ax.barh(bar_positions - bar_width/2, agents_vct['Pick Rate (%)'], bar_width, label='Pick Rate (%)', color='orange')

    ax.set_yticks(bar_positions)
    ax.set_yticklabels(agents_vct['Agent'])
    ax.set_xlabel('Porcentagem de Escolha')
    ax.set_title('Porcentagem de Escolha por Agente')
    ax.legend()

    plt.show()

#Função para mostrar o melhor jogador de uma região
def bestPlayerRegion(dataset, times, tournament):
    lista_jogadores = []

    for team in times:
        players = dataset[
            (dataset['Tournament'] == tournament) &
            (dataset['Stage'] == 'All Stages') &
            (dataset['Match Type'] == 'All Match Types') &
            (dataset['Team'] == team)
        ]

        players_grouped = players.groupby('Player').agg({
            'Kills': 'sum',
            'Kills Per Round': 'mean',
            'Average Damage Per Round': 'mean',
            'Headshot %': lambda x: pd.to_numeric(x.str.replace('%', ''), errors='coerce').mean(),
            'Kills:Deaths': 'mean'
        }).reset_index()

        players_grouped['Kills Mean'] = players_grouped['Kills'] / players_grouped.shape[0]
        players_grouped['Kills Per Round Mean'] = players_grouped['Kills Per Round']
        players_grouped['Average Damage Per Round Mean'] = players_grouped['Average Damage Per Round']
        players_grouped['Headshot % Mean'] = players_grouped['Headshot %']
        players_grouped['Kills:Deaths Mean'] = players_grouped['Kills:Deaths']

        lista_jogadores.append(players_grouped)

    
    jogadores = pd.concat(lista_jogadores).reset_index(drop=True)

    best_player = jogadores.sort_values(by='Kills Mean', ascending=False).head(1)

    return best_player