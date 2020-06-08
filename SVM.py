import os
import time
import pandas as pd
import numpy as np


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def loadData():
    """load the source data"""
    playerData = pd.read_csv(os.path.join(__location__,'./SourceData/player_data.csv'))
    players = pd.read_csv(os.path.join(__location__,'./SourceData/Players.csv'))
    seasonsStats = pd.read_csv(os.path.join(__location__,'./SourceData/Seasons_Stats.csv'), index_col=0)
    glossary = dict(pd.read_csv(os.path.join(__location__,'./SourceData/Seasons_Stats_Glossary.txt'),
                           sep='|', names=['abbv','description'], skip_blank_lines=True).values)

    if (v):
        print(f"playerData shape:{playerData.shape}")
        print(f"players shape:{players.shape}")
        print(f"seasonsStats shape:{seasonsStats.shape}")
    if (v):
        print(playerData)
        print(players)
        print(seasonsStats)
        print(glossary)
        # seasonsStats.rename(columns = glossary, inplace=True)

    return playerData, players, seasonsStats, glossary

def idSuccessOld(seasonsStats, ng):
    playerGames={}
    success_players=[]
    if (v): print(seasonsStats['G'].head())
    for player in seasonsStats['Player']:
      if player not in playerGames.keys():
        playerGames[player]=0
        games=[seasonsStats.loc[seasonsStats['Player']==player, 'G']][0].values
        playerGames[player]=sum(games)
        if playerGames[player] >= ng:
          if (v): print(player, playerGames[player])
          success_players.append(player)

def idSuccessNew(seasonsStats, ng):
    successP = seasonsStats.groupby(['Player'])['G'].sum()
    successP.columns = ['Player', 'G']
    successP = successP >= ng
    if (v): print(successP)
    return successP

if __name__ == "__main__":
    timeStart = time.time()
    v = 0 # flag for verbose printing
    ng = 174 # number of games played needed to be a "successful" player
    playerData, players, seasonsStats, glossary = loadData()
    if 1:
        success_players = idSuccessNew(seasonsStats, ng)
    else:
        success_players = idSuccessOld(seasonsStats, ng)
    

    timeEnd = time.time()
    minutes, seconds = divmod((timeEnd - timeStart), 60)
    print(f'This program took {int(minutes)} minutes and {int(seconds)} seconds to run.')