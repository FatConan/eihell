import random

class GameSimulator(object):
    default_outcomes = [(('Win', 2, None), ('Loss', 0, None)), (('Win OT', 2, None),('Loss OT', 1, None)), (('Win SO', 2, None),('Loss SO', 1, None)), (('Win', 2, None), ('Loss', 0, None))]
    order = [0, 1]

    @classmethod
    def simulate(cls, teams, outcomes, order):
        outcome = random.choice(outcomes)

        random.shuffle(order)
        primary = teams[order[0]]
        secondary = teams[order[1]]

        primary.add_outcome(outcome[0])
        secondary.add_outcome(outcome[1])

class Team(object):
    def __init__(self, name):
        self.name = name
        self.outcomes = []
        self.points = 0

    def add_outcome(self, outcome):
        self.outcomes.append(outcome)
        self.points += outcome[1]


    @property
    def wins(self):
        return len([outcome for outcome in self.outcomes if "Win" in outcome[0]])

    @property
    def regulation_wins(self):
        return len([outcome for outcome in self.outcomes if outcome[0] == "Win"])

    @property
    def losses(self):
        return len([outcome for outcome in self.outcomes if outcome[0] == "Loss"])

    @property
    def overtime_losses(self):
        return len([outcome for outcome in self.outcomes if outcome[0] == "Loss OT"])

    @property
    def shootout_losses(self):
        return len([outcome for outcome in self.outcomes if outcome[0] == "Loss SO"])

    def reset(self):
        self.points = 0
        self.outcomes = []

class League(object):
    def __init__(self):
        self.teams = {}
        self.fixtures = []

    def reset(self):
        for t in self.teams.values():
            t.reset()

    def add_team(self, team):
        if self.teams.get(team.name) is None:
            self.teams[team.name] = team

    def add_fixture(self, fixture):
        self.fixtures.append(fixture)

    def play_games(self):
        for team_name_a, team_name_b, already_played in self.fixtures:
            if not already_played:
                GameSimulator.simulate((self.teams.get(team_name_a), self.teams.get(team_name_b)), GameSimulator.default_outcomes, GameSimulator.order)
            else:
                self.teams.get(team_name_a).add_outcome(already_played[0])
                self.teams.get(team_name_b).add_outcome(already_played[1])

        league_final = self.teams.values()
        league_final.sort(key=lambda x: -x.points)
        return league_final


if __name__ == '__main__':
    teams = [Team('Team A'), Team('Team B')]

    for i in range(0, 52):
        GameSimulator.simulate(teams, GameSimulator.default_outcomes, GameSimulator.order)

    for t in teams:
        print t.name, t.points, t.outcomes