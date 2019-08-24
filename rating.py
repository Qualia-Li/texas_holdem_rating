from gilcko2 import Player

all_players = dict()


class Game:
    def __init__(self, player_scores):
        for player_name in player_scores.keys():
            if player_name not in all_players:
                all_players[player_name] = Player()
        players = [all_players[player_name] for player_name in player_scores.keys()]
        player_ratings = [player.rating for player in players]
        player_deviations = [player.rd for player in players]

        for player_name in player_scores.keys():
            player = all_players[player_name]
            score = normalize(player_scores[player_name])
            score_list = [score] * len(players)
            player.update_player(player_ratings, player_deviations, score_list)


def normalize(score):
    return score/100.0+0.5


def print_top_k_rating(k=0):
    sorted_players = sorted(all_players.items(), key=lambda p: p[1].rating, reverse=True)
    if k == 0:
        k = len(sorted_players)
    for player in sorted_players[:k]:
        print "%.2f\t%s" % (player[1].rating, player[0])
