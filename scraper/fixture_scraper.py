#coding: utf-8
import json
import os
from bs4 import BeautifulSoup
import requests
import re


class Scraper(object):
    SCORE_MATCHER = re.compile("""([0-9]+)–([0-9]+) FINAL(( - )(SHOOTOUT|OT))*""")

    @classmethod
    def scrape(cls):
        response = requests.get('https://eliteleague.co.uk/game-centre/schedule/?season_id=18470')
        soup = BeautifulSoup(response.text, 'lxml')
        table = None

        try:
            table = soup.select("section.container")[0]
        except IndexError:
            print("Missing results table")

        results = []
        if table is not None:
            current_date = None
            rows = table.find_all("div")
            for i, row in enumerate(rows):
                classes = row['class']
                if 'date-row' in classes:
                    current_date = row.text
                elif 'game-row' in classes:
                    home_team = row.find("span", class_="home-team").text
                    away_team = row.find("span", class_="away-team").text
                    score = row.find("span", class_="score").text

                    score_parts = cls.SCORE_MATCHER.match(score)

                    if score_parts:
                        home_score, away_score, _, _, outcome = score_parts.groups()
                        if outcome is None:
                            outcome = "DEFAULT"
                    else:
                        home_score = None
                        away_score = None
                        outcome = None

                    data = {
                        "date": current_date,
                        "home": home_team,
                        "away": away_team,
                        "home_score": home_score,
                        "away_score": away_score,
                        "outcome_descriptor": outcome
                    }
                    results.append(data)

            with open(os.path.join(os.path.abspath("resources"), "table.json"), "w") as json_file:
                json.dump(results, json_file)

    @classmethod
    def read_stored_json(cls):
         with open(os.path.join(os.path.abspath("resources"), "table.json"), "r") as json_file:
                return json.load(json_file)






