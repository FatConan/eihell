import json
import os

with open(os.path.join(os.path.abspath("../resources"), 'assists-and-scorers.json'), 'rb') as input:
    scorers = json.load(input)


counter = {}

for scorer in scorers:

    title = "_".join([x if x is not None else '' for x in scorer])
    try:
        counter[title] += 1
    except KeyError:
        counter[title] = 1

print json.dumps(counter)