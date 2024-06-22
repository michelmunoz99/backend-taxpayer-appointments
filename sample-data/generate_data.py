import json
from geopy.distance import geodesic
from heapq import nlargest
import random

with open('taxpayers.json', 'r') as file:
    taxpayers = json.load(file)

input_location = (19.3797208, -99.1940332)

def calculate_score(taxpayer, input_location):
    age = taxpayer['age']
    accepted_offers = taxpayer['accepted_offers']
    canceled_offers = taxpayer['canceled_offers']
    average_reply_time = taxpayer['average_reply_time']
    client_location = (taxpayer['location']['latitude'], taxpayer['location']['longitude'])

    distance = geodesic(input_location, client_location).kilometers

    age_score = (age / 100) * 10
    distance_score = (1 / (1 + distance)) * 10
    accepted_score = (accepted_offers / 100) * 10
    canceled_score = ((100 - canceled_offers) / 100) * 10
    reply_time_score = ((3600 - average_reply_time) / 3600) * 10

    score = (age_score * 0.1 + 
             distance_score * 0.1 + 
             accepted_score * 0.3 + 
             canceled_score * 0.3 + 
             reply_time_score * 0.2)

    return min(max(score, 1), 10)

for taxpayer in taxpayers:
    taxpayer['score'] = calculate_score(taxpayer, input_location)

few_data_taxpayers = [taxpayer for taxpayer in taxpayers if 0 <= taxpayer['accepted_offers'] <= 10 and 0 <= taxpayer['canceled_offers'] <= 10]

random_selected_taxpayers = random.sample(few_data_taxpayers, min(len(few_data_taxpayers), 3))

remaining_taxpayers = [taxpayer for taxpayer in taxpayers if taxpayer not in random_selected_taxpayers]
top_taxpayers = nlargest(7, remaining_taxpayers, key=lambda x: x['score'])

final_top_taxpayers = top_taxpayers + random_selected_taxpayers

print(json.dumps(final_top_taxpayers, indent=4))

with open('top_taxpayers.json', 'w') as outfile:
    json.dump(final_top_taxpayers, outfile, indent=4)
