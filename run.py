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
    if result[4]:
        if "SO" in result[4]:
            outcome = GameSimulator.default_outcomes[2]
        elif "OT" in result[4]:
            outcome = GameSimulator.default_outcomes[1]
        else:
            outcome = GameSimulator.default_outcomes[0]
        score_text = unicode(result[4])
        scores = [int(score) for score in score_text.replace(u" SO","").replace(u" OT", "").split("-")]
        if scores[0] > scores[1]:
            assigned_outcome = (outcome[0], outcome[1], scores)
        else:
            assigned_outcome = (outcome[1], outcome[0], scores)

    league.add_fixture((result[1], result[2], assigned_outcome))

start = time.time()
progress = Progress()
finals = []
range_max = 50000
for i in range(0, range_max):
    league.reset()
    out = league.play_games()
    finals.append(out)

    #print "TEAM, W, RW, L, OTL, SOL, PTS, %Chance"

    #for team in out:
    #    print "%s, %d, %d, %d, %d, %d, %d" % (team.name, team.wins, team.regulation_wins, team.losses, team.overtime_losses, team.shootout_losses, team.points)

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

print "TEAM, W, RW, L, OTL, SOL, PTS, %Chance"

for team, total in team_standings.items():
    print "%s, %d, %d, %d, %d, %d, %d, %f%%" % (team.name, team.wins, team.regulation_wins, team.losses, team.overtime_losses, team.shootout_losses, team.points,  (total * 1.0/range_max * 1.0) * 100.0)


print "%d in %f" % (range_max, end-start)
#for f in final:
#    print f.name, f.points, len(f.outcomes)
