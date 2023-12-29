import requests
import json
import os

api_key = "RGAPI-55b26ace-b436-4959-85ea-4a37d9aae3e9"
puuid = "1zs-4YJRd-Aryf6sljOC7sGTV2RbESk4igXM5yZqrM_a_0U3i07S4p-ZDI7mhnMS44g2kMJM1A-WTg"
# print(api_key)
# print(puuid)

if not os.path.exists('Hadoop/Data'):
    os.mkdir('Hadoop/Data')

# Get match id by puuid
request_for_match_id = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=100&api_key={api_key}"
respond = requests.get(request_for_match_id)
matchIds = json.loads(respond.text)
print(matchIds)


# Get match by match id 
for id, matchId in enumerate(matchIds) :
    requestUrl_for_matchInfor_byId = f"https://asia.api.riotgames.com/lol/match/v5/matches/{matchId}?api_key={api_key}"
    respondMatch = requests.get(requestUrl_for_matchInfor_byId)
    datas = json.loads(respondMatch.text)
    if "info" in datas: 
        dataPar = datas["info"]["participants"] 
        for i, data in enumerate(dataPar):
            file_name = f'Match{id+1}_player{i+1}.json'
            with open(f'Hadoop/Data/{file_name}', 'w') as f:
                json.dump(data, f)