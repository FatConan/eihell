#coding: utf-8
import requests
import os
from bs4 import BeautifulSoup
import json

fixture_list_url = "http://www.leaguestat.com/elite/elite/en/stats/roster.php?season_id=16&team_id=13"

response = requests.get(fixture_list_url)
soup = BeautifulSoup(response.text, "lxml")

try:
    roster = {}
    for table in soup.find('div', id='rosterBlock').select("table"):
        playerNumber = None
        for i, tr in enumerate(table.select("tr")):
            playerRow = False
            for j, td in enumerate(tr.select("td")):
                print j, td
                if j == 0 and td.get_text().isnumeric():
                    playerRow = True
                    playerNumber = td.get_text()
                if j == 1 and playerRow:
                    playerName = td.get_text()
                    roster[playerNumber] = playerName

    with open(os.path.join(os.path.abspath("../resources"),"roster.json"), "wb") as text_file:
        json.dump(roster, text_file)

    #print table
except Exception, e:
    print e

