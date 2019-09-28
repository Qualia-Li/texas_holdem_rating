from gilcko2 import Player

all_players = dict()
all_players_income = dict()


class Game:
    def __init__(self, player_scores):

        money_won = 0.0
        money_lost = 0.0

        for player_name in player_scores.keys():
            if player_name not in all_players:
                all_players[player_name] = Player()
                all_players_income[player_name] = 0
                print "New player: " + player_name
            if player_scores[player_name] > 0:
                money_won += player_scores[player_name]
            else:
                money_lost -= player_scores[player_name]
            all_players_income[player_name] += player_scores[player_name]

        print ""
        print "Money won: %.2f" % money_won
        print "Money lost: %.2f" % money_lost

        players = [all_players[player_name] for player_name in player_scores.keys()]
        player_ratings = [player.rating for player in players]
        player_deviations = [player.rd for player in players]

        max_score = max([score[1] for score in player_scores.items()])
        min_score = min([score[1] for score in player_scores.items()])
        max_score = max(max_score, -min_score)

        for player_name in player_scores.keys():
            player = all_players[player_name]
            score = normalize(player_scores[player_name], max_score)
            score_list = [score] * len(players)
            player.update_player(player_ratings, player_deviations, score_list)


def normalize(player_score, max_score):
    return player_score/2.0/max_score + 0.5


def print_top_k_rating(k=0):
    print ""
    sorted_players = sorted(all_players.items(), key=lambda p: p[1].rating, reverse=True)
    if k == 0:
        k = len(sorted_players)
    for player in sorted_players[:k]:
        print "%.2f\t%s" % (player[1].rating, player[0])


def print_top_k_income(k=0):
    sorted_players = sorted(all_players_income.items(), key=lambda p: p[1], reverse=True)
    if k == 0:
        k = len(sorted_players)
    for player in sorted_players[:k]:
        print "%s\t%s" % (player[1], player[0])
