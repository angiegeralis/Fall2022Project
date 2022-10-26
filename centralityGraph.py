import json
import networkx as nx
import matplotlib.pyplot as plt

def main():
    with open("events/events_European_Championship.json", "r") as read_file:
        events = json.load(read_file)
    with open("players.json", "r") as read_file:
        players = json.load(read_file)
    with open("matches/matches_European_Championship.json", "r") as read_file:
        matches = json.load(read_file)
    with open("teams.json", "r") as read_file:
        teams = json.load(read_file)

    centrality_graph_Euro("France", "Romania")

def find_team_id(team_name):
    with open("teams.json", "r") as read_file:
        teams = json.load(read_file)
    for team in teams:
        if team["officialName"] == team_name:
            return team["wyId"]

def find_match_id(team1, team2):
    with open("matches/matches_European_Championship.json", "r") as read_file:
        matches = json.load(read_file)
    for match in matches:
        label_name = str(team1 + " - " + team2)
        label_name2 = str(team2 + " - " + team1)
        if label_name in match["label"] or label_name2 in match["label"]:
            return match["wyId"]

def find_lineup(match_id, team_id):
    with open("matches/matches_European_Championship.json", "r") as read_file:
        matches = json.load(read_file)
    lineup = []
    for match in matches:
        if match["wyId"] == match_id:
            for player in match["teamsData"][str(team_id)]["formation"]["lineup"]:
                #print(player["playerId"])
                lineup.append(player["playerId"])
    return lineup

def centrality_graph_Euro(home, away):
    with open("events/events_European_Championship.json", "r") as read_file:
        events = json.load(read_file)
    with open("players.json", "r") as read_file:
        players = json.load(read_file)
    #look up match, if doesnt exist throw error
    #if exists, save match id and team ids
    home_id = find_team_id(home)
    away_id = find_team_id(away)
    match_id = find_match_id(home, away)
    connection_home = []
    connection_away = []
    home_passes = []
    away_passes = []
    keeper_home = find_lineup(match_id, home_id)[-1]
    keeper_away = find_lineup(match_id, away_id)[-1]

    for event in events:
        if event["teamId"] == home_id and event["matchId"] == match_id:
            current_player = event["playerId"]
            for player in players:
                if current_player == player["wyId"]:
                    if current_player not in find_lineup(match_id, home_id):
                        current_player = 0 #ignore because didnt start
                    else:
                        current_player = player["shortName"]
            if len(connection_home) == 1:
                connection_home.append(current_player)
                if connection_home[0] != connection_home[1] and current_player != 0:
                    home_passes.append(tuple(connection_home))
                    connection_home = []
            else:
                if (event["eventId"] == 8 and event["tags"][0]["id"] == 1801 and current_player != 0):
                    connection_home.append(current_player)
    home_centrality = []
    for x in home_passes:
        weight = home_passes.count(x)
        new_tuple = x + (weight,)
        if new_tuple not in home_centrality:
            home_centrality.append(new_tuple)
    G_home = nx.Graph()
    G_home.add_weighted_edges_from(home_centrality)
    edges = G_home.edges()
    color_map = []
    for player in players:
        if keeper_home == player["wyId"]:
            keeper_home = player["shortName"]

    for node in G_home:
        if node == keeper_home:
            color_map.append('green')
        else:
            color_map.append('blue')

    weights = [G_home[u][v]['weight'] for u,v in edges]
    nx.draw(G_home, with_labels = True, node_color = color_map, width=weights)
    plt.show()

    for event in events:
        if event["teamId"] == away_id and event["matchId"] == match_id:
            current_player = event["playerId"]
            for player in players:
                if current_player == player["wyId"]:
                    if current_player not in find_lineup(match_id, away_id):
                        current_player = 0 #ignore because didnt start
                    else:
                        current_player = player["shortName"]
            if len(connection_away) == 1:
                connection_away.append(current_player)
                if connection_away[0] != connection_away[1] and current_player != 0:
                    away_passes.append(tuple(connection_away))
                    connection_away = []
            else:
                if (event["eventId"] == 8 and event["tags"][0]["id"] == 1801 and current_player != 0):
                    connection_away.append(current_player)
    away_centrality = []
    for x in away_passes:
        weight = away_passes.count(x)
        new_tuple = x + (weight,)
        if new_tuple not in away_centrality:
            away_centrality.append(new_tuple)
    G_away = nx.Graph()
    G_away.add_weighted_edges_from(away_centrality)
    edges = G_away.edges()
    color_map = []
    for player in players:
        if keeper_away == player["wyId"]:
            keeper_away = player["shortName"]

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
