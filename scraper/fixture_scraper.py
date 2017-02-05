#coding: utf-8
import json
import os
from bs4 import BeautifulSoup
import requests


class Scraper(object):
    @classmethod
    def scrape(cls):
        response = requests.get('https://eliteleague.co.uk/dask-fixtures/')
        print response.text
        soup = BeautifulSoup(response.text, "lxml")

        try:
            table = soup.select("table.sstable")[0]
            table_text = unicode(table)
        except IndexError:
            print "Missing results table"
            table_text = None

        results = []
        if table_text is not None:
            table = BeautifulSoup(table_text, "lxml")
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

            with open(os.path.join(os.path.abspath("resources"), "table.json"), "wb") as json_file:
                json.dump(results, json_file)

    @classmethod
    def read_stored_json(cls):
         with open(os.path.join(os.path.abspath("resources"),"table.json"), "rb") as json_file:
                return json.load(json_file)






