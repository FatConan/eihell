#!/usr/bin/python
# -*- coding: UTF-8 -*-

from scraper.fixture_scraper import Scraper
from generators.game_simulator import *
from helpers.progress import Progress
import time

Scraper.scrape()
results = Scraper.read_stored_json()
league = League()

for result in results:
    teamA = Team(result[1])
    teamB = Team(result[2])
    league.add_team(teamA)
    league.add_team(teamB)

    assigned_outcome = None
    print(result)
    if result[4]:

        if "SHOOTOUT" == result[5]:
            outcome = GameSimulator.default_outcomes[2]
        elif "OT" == result[5]:
            outcome = GameSimulator.default_outcomes[1]
        else:
            outcome = GameSimulator.default_outcomes[0]

        home_score, away_score = result[3], result[4]

        if home_score is not None and away_score is not None and home_score > away_score:
            assigned_outcome = (outcome[0], outcome[1], [home_score, away_score])
        elif home_score is not None and away_score is not None:
            assigned_outcome = (outcome[1], outcome[0], [home_score, away_score])

    league.add_fixture((result[1], result[2], assigned_outcome))
    print(league)
start = time.time()
progress = Progress()
finals = []
range_max = 50000
for i in range(0, range_max):
    league.reset()
    out = league.play_games()
    finals.append(out)
    progress.progress_bar(range_max, i, "Simulating ")

end = time.time()
team_standings = {}

for final in finals:
    for i, team in enumerate(final):
        if i < 8:
            addition = 1
        else:
            addition = 0
        try:
            team_standings[team] += addition
        except KeyError:
            team_standings[team] = addition

print("TEAM, W, RW, L, OTL, SOL, PTS, %Chance")

for team, total in team_standings.items():
    print("%s, %d, %d, %d, %d, %d, %d, %f%%" % (team.name, team.wins, team.regulation_wins, team.losses, team.overtime_losses, team.shootout_losses, team.points,  (total * 1.0/range_max * 1.0) * 100.0))


print("%d in %f" % (range_max, end-start))

