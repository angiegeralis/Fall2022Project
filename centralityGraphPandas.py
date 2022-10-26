import json
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

def main():

    home_team = find_team_id("France")
    away_team = find_team_id("Romania")
    centrality_graph_Euro("France","Romania")

def find_team_id(team_name):
    with open("teams.json", "r") as read_file:
        teams = pd.read_json(read_file)
    team_names = teams["officialName"]
    return teams[teams["officialName"] == team_name]["wyId"].values[0]

def find_match_id(team1, team2):
    with open("matches/matches_European_Championship.json", "r") as read_file:
        matches = pd.read_json(read_file)

    label_name = str(team1 + " - " + team2) #potential label 1
    label_name2 = str(team2 + " - " + team1) #potential label 2
    all_matches = matches["label"].values #list of all match labels
    for full_label in all_matches:  #full label is home - away, score (ie. France - Romania, 2 - 1)
        if label_name in full_label or label_name2 in full_label: #check for substring
            matches_label = full_label #assign full label
    return matches[matches["label"] == matches_label]["wyId"].values[0] #find match id of label

def find_lineup(match_id, team_id):
    with open("matches/matches_European_Championship.json", "r") as read_file:
        matches = pd.read_json(read_file)
    with open("players.json", "r") as read_file:
        players = pd.read_json(read_file)

    lineup = []
    lookhere = matches[matches["wyId"] == match_id]
    formation_info = lookhere["teamsData"].values
    for info in formation_info:
        for player in info[str(team_id)]["formation"]["lineup"]:
            lineup.append(player["playerId"])
    return lineup

def find_player_name(player_id):
    with open("players.json", "r") as read_file:
        players = pd.read_json(read_file)

    this_row = players[players["wyId"] == player_id]
    return this_row["shortName"].values[0]

def centrality_graph_Euro(home, away):
    with open("events/events_European_Championship.json", "r") as read_file:
        events = pd.read_json(read_file)
    with open("players.json", "r") as read_file:
        players = pd.read_json(read_file)
    #look up match, if doesnt exist throw error
    #if exists, save match id and team ids
    home_id = find_team_id(home)
    away_id = find_team_id(away)
    match_id = find_match_id(home, away)
    connection_home = []
    connection_away = []
    home_passes = []
    away_passes = []
    keeper_home = find_player_name(find_lineup(match_id, home_id)[-1])
    keeper_away = find_player_name(find_lineup(match_id, away_id)[-1])

    all_passes_home = events[(events["teamId"] == home_id) & (events["matchId"] == match_id) & (events["eventId"] == 8)].values
    all_passes_away = events[(events["teamId"] == away_id) & (events["matchId"] == match_id) & (events["eventId"] == 8)].values

    for x in all_passes_home:
        current_player = players[players["wyId"] == x[3]]
        if len(connection_home) == 1 and x[3] in find_lineup(match_id, home_id):
            current_player = players[players["wyId"] == x[3]]
            connection_home.append(current_player["shortName"].values[0])
            home_passes.append(tuple(connection_home))
            connection_home = []
        else: #this makes it slow
            if x[2][0]['id'] == 1801 and x[3] in find_lineup(match_id, home_id):
                current_player = players[players["wyId"] == x[3]]
                connection_home.append(current_player["shortName"].values[0])
    home_centrality = []
    for pair in home_passes:
        weight = home_passes.count(pair)
        new_tuple = pair + (weight,)
        if new_tuple not in home_centrality:
            home_centrality.append(new_tuple)
    G_home = nx.Graph()
    G_home.add_weighted_edges_from(home_centrality)
    edges = G_home.edges()
    color_map = []

    for node in G_home:
        if node == keeper_home:
            color_map.append('green')
        else:
            color_map.append('blue')

    weights = [G_home[u][v]['weight'] for u,v in edges]
    nx.draw(G_home, with_labels = True, node_color = color_map, width=weights)
    plt.show()

    for x in all_passes_away:
        current_player = players[players["wyId"] == x[3]]
        if len(connection_away) == 1 and x[3] in find_lineup(match_id, away_id):
            current_player = players[players["wyId"] == x[3]]
            connection_away.append(current_player["shortName"].values[0])
            away_passes.append(tuple(connection_away))
            connection_away = []
        else:
            if x[2][0]['id'] == 1801 and x[3] in find_lineup(match_id, away_id):
                current_player = players[players["wyId"] == x[3]]
                connection_away.append(current_player["shortName"].values[0])
    away_centrality = []
    for pair in away_passes:
        weight = away_passes.count(pair)
        new_tuple = pair + (weight,)
        if new_tuple not in away_centrality:
            away_centrality.append(new_tuple)
    G_away = nx.Graph()
    G_away.add_weighted_edges_from(away_centrality)
    edges = G_away.edges()
    color_map = []

    for node in G_away:
        if node == keeper_away:
            color_map.append('green')
        else:
            color_map.append('blue')

    weights = [G_away[u][v]['weight'] for u,v in edges]
    nx.draw(G_away, with_labels = True, node_color = color_map, width=weights)
    plt.show()

if __name__ == "__main__" :
    main()
