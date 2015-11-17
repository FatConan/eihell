import os
import json

dataLoaded = None
with open(os.path.join(os.path.abspath("../resources"),"roster.json"), 'rb') as data:
    dataLoaded = json.load(data)

print dataLoaded

def process_file(txt_file):
    game_definition = txt_file.readline().split(" at ")
    print game_definition


for name in [x for x in os.listdir("../resources") if x.endswith('.txt')]:
    with open(os.path.join(os.path.abspath("../resources"), name), 'rb') as txt_file:
        process_file(txt_file)

