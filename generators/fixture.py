class Team:
    def __init__(self, name):
        self.name = name
        self.points = 0
        self.outcomes_short = {
            'W': 0,
            'L': 0,
            'OT': 0,
        }

        self.fixtures = []

    def add_fixture(self, fixture):

        if fixture.team_a == self:
            self.fixtures.append(fixture)
            self.outcomes_short[fixture.outcome_a] += 1


        elif fixture.tem_b == self:
            self.fixtures.append(fixture)
            self.outcomes_short[fixture.outcome_b] += 1
        else:
            pass


class Teams:
    def __init__(self):
        self.teams = {}

    def add_team(self, name):
        if self.teams.get(name) is None:
            self.teams[name] = Team(name)

    def get_team(self, name):
        return self.teams.get(name)




class Fixture:
    def __init__(self, team_a, team_b, outcome_a, outcome_b, outcome_type, score_a, score_b, fixture_type):
        self.team_a = team_a
        self.team_b = team_b
        self.outcome_a = outcome_a
        self.outcome_b = outcome_b
        self.outcome_type = outcome_type
        self.score_a = score_a
        self.score_b = score_b
        self.fixture_type = fixture_type

        team_a.add_fixture(self)
        team_b.add_fixture(self)

