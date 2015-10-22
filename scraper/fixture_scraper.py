#coding: utf-8
import json
import os
import sys
sys.path.extend(['C:\\Users\\Fat\\Dropbox\\eliteHockey'])

from bs4 import BeautifulSoup
import requests
import time
from generators.game_simulator import League, Team, GameSimulator
from helpers.progress import Progress


class Scraper(object):
    @classmethod
    def scrape(cls):
        response = requests.get('http://www.eliteleague.co.uk/fixtures-s12347')
        soup = BeautifulSoup(response.text, "lxml")

        try:
            table = soup.select("div.games table.rosterTable")[0]
            table_text = unicode(table)
        except IndexError:
            table_text = None

        results = []
        if table_text is not None:
            table = BeautifulSoup(table_text)
            rows = table("tr")

            header = {}
            for i, row in enumerate(rows):
                if row("th"):
                    tds = row("th")
                    header = dict([(t.get_text(), i) for i, t in enumerate(tds)])
                elif row("td"):
                    if i % 2== 0:
                        tds = row("td")
                        if 'League' in tds[header.get('Game ID')].get_text():
                            data = [tds[header.get('Date')], tds[header.get('Visiting Team')], tds[header.get('Home Team')], tds[header.get('Game ID')], tds[header.get('Score')]]
                            results.append([t.get_text() for t in data])

            with open(os.path.join(os.path.abspath("../resources"),"table.json"), "wb") as json_file:
                json.dump(results, json_file)

    @classmethod
    def read_stored_json(cls):
         with open(os.path.join(os.path.abspath("../resources"),"table.json"), "rb") as json_file:
                return json.load(json_file)

if __name__ == '__main__':

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
    range_max = 1000000
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





