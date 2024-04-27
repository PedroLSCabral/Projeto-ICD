#Função para juntar todos as tabelas filtradas
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

colors = ['#1f77b4', '#ff7f0e', '#d62728', '#9467bd', '#666666'] 
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

    bar_width = 0.4

    bar_positions = np.arange(len(maps_vct))

    fig, ax = plt.subplots(figsize=(15, 8))

    ax.barh(bar_positions + bar_width/2, maps_vct['Total Defender Side Win Percentage'], bar_width, label='Defesa', color=colors[0])

    ax.barh(bar_positions - bar_width/2, maps_vct['Total Attacker Side Win Percentage'], bar_width, label='Ataque', color=colors[1])

    ax.set_yticks(bar_positions)
    ax.set_yticklabels(maps_vct['Map'])
    ax.set_ylabel("Mapas")
    ax.set_xlabel('Porcentagem de Vitória')
    ax.set_title('Porcentagem de Vitória por Mapa e Lado')
    ax.legend(loc="lower right")

    for pos in range (10, 51, 10):
        ax.axvline(x=pos, color=colors[4], linestyle='dotted') 
  

    plt.show()

#Função para Montar o grafico dos agentes
def mostraGraficoAgent(agents_vct):

    
    bar_width = 0.6  # Largura da barra
    bar_positions = np.arange(len(agents_vct))

    fig, ax = plt.subplots(figsize=(10, 8))

    ax.barh(bar_positions - bar_width/2, agents_vct['Pick Rate (%)'], bar_width, label='Pick Rate (%)', color=colors[1])

    ax.set_yticks(bar_positions)
    ax.set_yticklabels(agents_vct['Agent'])
    ax.set_xlabel('Porcentagem de Escolha')
    ax.set_title('Porcentagem de Escolha por Agente')
    ax.legend()

    for pos in range (10, 51, 10):
        ax.axvline(x=pos, color=colors[4], linestyle='-') 

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


def agentsKD(dataset, tournament):
    players = dataset[(dataset['Tournament'] == tournament) &
                      (dataset['Stage'] == 'All Stages') &
                      (dataset['Match Type'] == 'All Match Types')]

    # filtra as linhas onde o número de agents é exatamente 1
    players = players[players['Agents'].str.count(',') == 0]

    agents_kd = players[['Agents', 'Kills:Deaths']]

    agents_kd = agents_kd.groupby('Agents')['Kills:Deaths'].mean().reset_index()

    agents_kd = agents_kd.sort_values(by='Kills:Deaths', ascending=False).round(2)

    return agents_kd



def mudancaValores(dataset):
    if dataset['Team A'] == 'Team Vikings':
        if dataset['Team A Score'] > dataset['Team B Score']:
            return 1
        elif dataset['Team A Score'] < dataset['Team B Score']:
            return 0

    elif dataset['Team B'] == 'Team Vikings':
        if dataset['Team B Score'] > dataset['Team A Score']:
            return 1
        elif dataset['Team B Score'] < dataset['Team A Score']:
            return 0


def partidasGanhas(dataset, time, tournament):
    dataset['Tournament'] = dataset['Tournament'].astype(str)
    dataset['Team A'] = dataset['Team A'].astype(str)
    dataset['Team B'] = dataset['Team B'].astype(str)

    matches_champions = dataset[
        (dataset['Tournament'] == tournament) & 
        ((dataset['Team A'] == time) | 
         (dataset['Team B'] == time))
    ]

    matches_champions.loc[:, 'Team A Score'] = matches_champions['Team A Score'].astype(int)
    matches_champions.loc[:, 'Team B Score'] = matches_champions['Team B Score'].astype(int)

    matches_champions_copy = matches_champions.copy()

    matches_champions_copy['Result'] = matches_champions_copy.apply(mudancaValores, axis=1)

    matches_champions_copy.drop('Match Result', axis=1, inplace=True)

    return (matches_champions_copy['Result'] == 1).sum()


def mapasJogados(dataset, time, tournament):
    matches_champions = dataset[
        (dataset['Tournament'] == tournament) & 
        dataset['Match Name'].str.contains(time)]

    return matches_champions['Map'].count()

def acsOverview(teams, dataset):
    team_means = []

    for team in teams:
        team_acs_mean = dataset[dataset["Team"] == team]["Average Combat Score"].mean().round(2)
        team_means.append(team_acs_mean)

    team_matches_count = [len(dataset[dataset["Team"] == team]["Match Name"].unique()) for team in teams]

    overview_table = pd.DataFrame({
        "Team": teams,
        "Matches Count": team_matches_count,  
        "Mean ACS": team_means
    })

    return overview_table


def agentsYear(dataset, year):
    agents_vctYear_bar = dataset

    agents_vctYear_bar['Year'] = year

    agents_vctYear_ord = dataset.sort_values(by='Pick Rate', ascending=False)

    agents_vctYear_ord = agents_vctYear_ord.head(22)

    return agents_vctYear_ord

def mediaMap(maps_vct_total):
    
    # Aplicando a media nas vazias da linha da Fracture, para que os dados fique mais facil a visualização
    media_fracture_attack = (maps_vct_total.loc[maps_vct_total['Map'] == 'Fracture', 'Attacker Side Win Percentage_y'] +  maps_vct_total.loc[maps_vct_total['Map'] == 'Fracture', 'Attacker Side Win Percentage'])/2 
    media_fracture_defender = (maps_vct_total.loc[maps_vct_total['Map'] == 'Fracture', 'Defender Side Win Percentage_y'] +  maps_vct_total.loc[maps_vct_total['Map'] == 'Fracture', 'Defender Side Win Percentage'])/2

    maps_vct_total.loc[maps_vct_total['Map'] == 'Fracture', 'Attacker Side Win Percentage_x'] = round( media_fracture_attack ,1)
    maps_vct_total.loc[maps_vct_total['Map'] == 'Fracture', 'Defender Side Win Percentage_x'] = round(media_fracture_defender ,1)

    # Aplicando a media nas vazias da linha da Pearl, para que os dados fique mais facil a visualização
    media_pear_attack = (maps_vct_total.loc[maps_vct_total['Map'] == 'Pearl', 'Attacker Side Win Percentage_y'] +  maps_vct_total.loc[maps_vct_total['Map'] == 'Pearl', 'Attacker Side Win Percentage'])/2 
    media_pear_defender = (maps_vct_total.loc[maps_vct_total['Map'] == 'Pearl', 'Defender Side Win Percentage_y'] +  maps_vct_total.loc[maps_vct_total['Map'] == 'Pearl', 'Defender Side Win Percentage'])/2

    maps_vct_total.loc[maps_vct_total['Map'] == 'Pearl', 'Attacker Side Win Percentage_x'] = round(media_pear_attack ,1)
    maps_vct_total.loc[maps_vct_total['Map'] == 'Pearl', 'Defender Side Win Percentage_x'] = round(media_pear_defender ,1)

    # Aplicando a media nas vazias da linha da Breeze, para que os dados fique mais facil a visualização
    media_breeze_attack = (maps_vct_total.loc[maps_vct_total['Map'] == 'Breeze', 'Attacker Side Win Percentage_y'] +  maps_vct_total.loc[maps_vct_total['Map'] == 'Breeze', 'Attacker Side Win Percentage_x'])/2 
    media_breeze_defender =  (maps_vct_total.loc[maps_vct_total['Map'] == 'Breeze', 'Defender Side Win Percentage_y'] +  maps_vct_total.loc[maps_vct_total['Map'] == 'Breeze', 'Defender Side Win Percentage_x'])/2

    maps_vct_total.loc[maps_vct_total['Map'] == 'Breeze', 'Attacker Side Win Percentage'] = round(media_breeze_attack ,1)
    maps_vct_total.loc[maps_vct_total['Map'] == 'Breeze', 'Defender Side Win Percentage'] = round(media_breeze_defender ,1)

    # Aplicando a media nas vazias da linha da Icebox, para que os dados fique mais facil a visualização

    media_icebox_attack = (maps_vct_total.loc[maps_vct_total['Map'] == 'Icebox', 'Attacker Side Win Percentage_y'] +  maps_vct_total.loc[maps_vct_total['Map'] == 'Icebox', 'Attacker Side Win Percentage_x'])/2 
    media_icebox_defender = (maps_vct_total.loc[maps_vct_total['Map'] == 'Icebox', 'Defender Side Win Percentage_y'] +  maps_vct_total.loc[maps_vct_total['Map'] == 'Icebox', 'Defender Side Win Percentage_x'])/2 

    maps_vct_total.loc[maps_vct_total['Map'] == 'Icebox', 'Attacker Side Win Percentage'] = round( media_icebox_attack ,1)
    maps_vct_total.loc[maps_vct_total['Map'] == 'Icebox', 'Defender Side Win Percentage'] = round( media_icebox_defender ,1)

    # Usando os dados para prencher dados vacios na tabela, esse é da lotus
    maps_vct_total.loc[maps_vct_total['Map'] == 'Lotus', 'Attacker Side Win Percentage_x'] = maps_vct_total.loc[maps_vct_total['Map'] == 'Lotus', 'Attacker Side Win Percentage']
    maps_vct_total.loc[maps_vct_total['Map'] == 'Lotus', 'Defender Side Win Percentage_x'] = maps_vct_total.loc[maps_vct_total['Map'] == 'Lotus', 'Defender Side Win Percentage']

    maps_vct_total.loc[maps_vct_total['Map'] == 'Lotus', 'Attacker Side Win Percentage_y'] = maps_vct_total.loc[maps_vct_total['Map'] == 'Lotus', 'Attacker Side Win Percentage']
    maps_vct_total.loc[maps_vct_total['Map'] == 'Lotus', 'Defender Side Win Percentage_y'] = maps_vct_total.loc[maps_vct_total['Map'] == 'Lotus', 'Defender Side Win Percentage']

    return maps_vct_total