# from gilcko2 import Player
import trueskill

MU = 1500.0
SIGMA = MU / 3
BETA = SIGMA / 2
TAU = SIGMA / 100

trueskill_env = trueskill.TrueSkill(mu=MU,
                                    sigma=SIGMA,
                                    beta=BETA,
                                    tau=TAU,
                                    draw_probability=0)


class Player:

    all_players = dict()

    def __init__(self, name):
        self.name = name
        self.absence = 0
        self.score = []
        self.rating = trueskill_env.create_rating()
        Player.all_players[name] = self
        print "New player: %s" % name

    def print_rating(self):
        absence_note = " (absent: %d)" % self.absence if self.absence > 0 else ""
        print "%.2f\t%.2f\t%s" % (self.rating.mu, self.rating.sigma, self.name+absence_note)

    def print_score(self):
        print "%.2f\t%.2f\t%s" % (self.total_income, self.avg_income, self.name)

    def update_score(self, score):
        self.score.append(score)

    def update_absence(self, absent):
        if absent:
            self.absence += 1
        else:
            self.absence = 0

    @staticmethod
    def get(name):
        if name in Player.all_players:
            return Player.all_players[name]
        else:
            return Player(name)

    @property
    def total_income(self):
        return sum(self.score)

    @property
    def avg_income(self):
        return self.total_income/1.0/len(self.score)


class Game:
    def __init__(self, player_scores, blind_size=40):

        money_won = 0.0
        money_lost = 0.0

        for player_name in player_scores.keys():
            player = Player.get(player_name)

            if player_scores[player_name] > 0:
                money_won += player_scores[player_name]
            else:
                money_lost -= player_scores[player_name]

            player.update_score(player_scores[player_name])

        print ""
        print "Money won: %.2f" % money_won
        print "Money lost: %.2f" % money_lost

        for player in Player.all_players.values():
            player.update_absence(player.name not in player_scores.keys())

        players = [Player.get(name) for name in player_scores.keys()]
        rating_groups = [(p.rating,) for p in players]

        # max_score = max(player_scores.values())
        # min_score = max(player_scores.values())
        # max_score = max(max_score, -min_score)
        ranks = [-v for v in player_scores.values()]
        # print zip(player_scores.keys(), ranks)

        rated_rating_groups = trueskill_env.rate(rating_groups, ranks)
        for i in range(len(players)):
            players[i].rating = rated_rating_groups[i][0]


def normalize(player_score, blind_size):
    return 1.0 - player_score/2.0/blind_size


def print_top_k_rating(k=0):
    print "\nRating\tSigma\tName"
    active_players = filter(lambda p: p.absence <= 3, Player.all_players.values())
    sorted_players = sorted(active_players, key=lambda p: p.rating, reverse=True)
    if k == 0:
        k = len(sorted_players)
    for player in sorted_players[:k]:
        player.print_rating()


def print_top_k_score(k=0):
    print "\nGain\tAvg\tName"
    active_players = filter(lambda p: p.absence <= 3, Player.all_players.values())
    sorted_players = sorted(active_players, key=lambda p: p.total_income, reverse=True)
    if k == 0:
        k = len(sorted_players)
    for player in sorted_players[:k]:
        player.print_score()
