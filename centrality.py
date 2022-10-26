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
    pass_count_France = 0
    pass_count_Romania = 0
    player_passes_France = {}
    player_passes_Romania = {}
    positions_F = {}
    positions_R = {}
    for event in events:
        if event["eventId"] == 8: #eventId for a pass
            if event["teamId"] == 4418 and event["matchId"] == 1694392: #France
                if(event["tags"][0]["id"]) == 1801: # accurate pass
                    for player in players:
                        if event["playerId"] == player["wyId"]:
                            player_name_F = player["shortName"]
                            if player_name_F in player_passes_France:
                                player_passes_France[player_name_F] +=1
                            else:
                                player_passes_France[player_name_F] = 1
                                positions_F[player_name_F] = player["role"]["code2"]

                pass_count_France +=1
            if event["teamId"] == 11944: #Romania
                if(event["tags"][0]["id"]) == 1801: # accurate pass
                    for player in players:
                        if event["playerId"] == player["wyId"]:
                            player_name_R = player["shortName"]
                            if player_name_R in player_passes_Romania:
                                player_passes_Romania[player_name_R] +=1
                            else:
                                positions_R[player_name_R] = player["role"]["code2"]
                                player_passes_Romania[player_name_R] =1
                pass_count_Romania +=1

    print(positions_F)
    print(positions_R)




    connection = []
    all_passes_F = []
    starting_lineup = []
    for event in events:
        if event["teamId"] == 4418 and event["matchId"] == 1694390:#France
            current_player = event["playerId"]
            for player in players:
                if current_player == player["wyId"]:
                    current_player = player["shortName"]
            if len(connection) == 1:
                connection.append(current_player)
                if connection[0] != connection[1]:
                    all_passes_F.append(tuple(connection))
                    connection = []
            else:
                if (event["eventId"] == 8 and event["tags"][0]["id"] == 1801) :
                    connection.append(current_player)
    passes_dict = []
    for x in all_passes_F:
        weight = all_passes_F.count(x)
        new_tuple = x + (weight,)
        if new_tuple not in passes_dict:
            passes_dict.append(new_tuple)
    GF = nx.Graph()
    GF.add_weighted_edges_from(passes_dict)
    edges = GF.edges()
    color_map = []
    for node in GF:
        if node == "H. Lloris":
            color_map.append('green')
        else:
            color_map.append('blue')
    weights = [GF[u][v]['weight'] for u,v in edges]
    nx.draw(GF, with_labels = True, node_color = color_map, width=weights)
    plt.show()
    all_passes_R = []
    for event in events:
        if event["teamId"] == 11944 and event["matchId"] == 1694390: #Romania
            current_player = event["playerId"]
            for player in players:
                if current_player == player["wyId"]:
                    current_player = player["shortName"]
            if len(connection) == 1:
                connection.append(current_player)
                if connection[0] != connection[1]:
                    all_passes_R.append(tuple(connection))
                    connection = []
            else:
                if (event["eventId"] == 8 and event["tags"][0]["id"] == 1801) :
                    connection.append(current_player)

    passes_dict_R = []
    for x in all_passes_R:
        weight = all_passes_R.count(x)
        new_tuple = x + (weight,)
        if new_tuple not in passes_dict_R:
            passes_dict_R.append(new_tuple)

    GR = nx.Graph()
    GR.add_weighted_edges_from(passes_dict_R)
    edges = GR.edges()
    weights = [GR[u][v]['weight'] for u,v in edges]
    nx.draw(GR, with_labels = True, width=weights)
    plt.show()







if __name__ == "__main__" :
    main()
