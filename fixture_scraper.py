#coding: utf-8
import json
import datetime
import os
from bs4 import BeautifulSoup
import requests
import re
import dateparser


class Scraper(object):
    SCORE_MATCHER = re.compile("""([0-9]+):([0-9]+)(( - )(SHOOTOUT|OT))*""")
    SPLIT_FIXTURE = re.compile("""\s{2,}""")
    @classmethod
    def scrape(cls):
        response = requests.get('https://www.eliteleague.co.uk/schedule?id_season=2&id_team=0&id_month=999')
        soup = BeautifulSoup(response.text, 'html.parser')
        table = None

        try:
            table = soup.select("div.container-fluid")[0]
        except IndexError:
            print("Missing results table")

        results = []
        if table is not None:
            current_date = None
            for i, row in enumerate(table.find_all(["h2", "div"])):
                classes = row['class']
                if row.name == "h2":
                    current_date = datetime.datetime.strptime(row.get_text().split(" ")[1], '%d.%m.%Y')
                elif row.name == "div" and "justify-content-center" in classes:
                    away_team, score, home_team = [x for x in cls.SPLIT_FIXTURE.split(row.get_text()) if x]
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
                        "date": current_date.strftime("%Y-%m-%d"),
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


if __name__ == "__main__":
    Scraper.scrape()



