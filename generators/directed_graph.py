#coding: utf-8
import os
import json
import re

team = ['Edinburgh', 'Edn']
period_names = ['1st Period', '2nd Period', '3rd Period', '1st OT Period']
period_line_re = '(%(period)s)(?:[\s]*)(?:-)' % {'period': '|'.join(period_names)}
c_period_line_re = re.compile(period_line_re)

#period_line_re = '(%(period)s)\w*(?:-)\w*([0-9]+),\w*(%(team)s),\w*(.+) ([0-9]+) (.+), [0-9]+:[0-9]+ .+ \.' % {'period': '|'.join(period_names), 'team': '|'.join(team)}
period_line_re = '(?:(?:[\s]*)(?P<goalnumber>[0-9]+),(?:[\s]*)(?P<team>[\w]+),(?:[\s]*)(?P<scorer>[\S]+)(?:[\s]*)(?P<teamgoalnumber>[0-9]+)' % {'team': '|'.join(team)}
period_line_re += '(?:(?:[\s]*)|(?:[\s]*)\((?P<assists>[\w, ]+)\),(?:[\s]*))'
period_line_re += '[0-9]+:[0-9]+(?:[\s]*)(?:\(PP\)|\(SH\)|\(EN\))*\.)'
print period_line_re
compiled = re.compile(period_line_re)


dataLoaded = None
with open(os.path.join(os.path.abspath("../resources"),"roster.json"), 'rb') as data:
    dataLoaded = json.load(data)

print dataLoaded


pairs = []

def reading_period(stripped_line):
    possible_period_line = stripped_line
    for name in period_names:
        if possible_period_line.startswith(name):
            line = possible_period_line.split("Penalties")[0]
            cleaned_of_period = c_period_line_re.sub("", line)
            matches = compiled.finditer(cleaned_of_period)
            for m in matches:
                #print "MATCH", m.groups('whole')[0]
                #print m.groupdict()
                if m.get("team") in team:
                    pass

            return True
    return False



def process_file(txt_file):
    game_definition = txt_file.readline().strip().split(" at ")
    txt_file.readline() #blank line
    time_and_location = txt_file.readline().strip().split(" - ")
    away_team_and_score = txt_file.readline().strip().split(" - ")
    home_team_and_score = txt_file.readline().strip().split(" - ")

    while reading_period(txt_file.readline()):
        continue

    #first_period_line = txt_file.readline().strip()
    #second_period_line = txt_file.readline().strip()
    #third_period_line = txt_file.readline().strip()

for name in [x for x in os.listdir("../resources") if x.endswith('.txt')]:
    with open(os.path.join(os.path.abspath("../resources"), name), 'rb') as txt_file:
        process_file(txt_file)
