#coding: utf-8
import requests
import os
from bs4 import BeautifulSoup

fixture_list_url = "http://www.leaguestat.com/elite/elite/en/stats/schedule.php?view=season&team_id=13&season_id=16&home_away=&division_id="

response = requests.get(fixture_list_url)
soup = BeautifulSoup(response.text, "lxml")

try:
    table = soup.select("table.schedule-season")[0]
    for a in table.select("td.ls-gamelinks a"):
        if a["title"] == "Text Game Report":
            with open(os.path.join(os.path.abspath("../resources"),"%s.txt" % a["href"]), "wb") as text_file:
                print "Reading url %s" % a['href']
                resp = requests.get("http://www.leaguestat.com/elite/elite/en/stats/%s" % a['href'])
                s = BeautifulSoup(resp.text, "lxml")
                s_text = unicode(s.select("body")[0])
                text_file.write(s_text.encode("utf-8").replace('\xc2\xa0', ' ').replace('<body>', '').replace('</body>', '').replace('<br clear="all"/>', '').replace('<br/><br/>', '\n').replace('<br/>', '\n').strip())

    #print table
except Exception, e:
    print e

