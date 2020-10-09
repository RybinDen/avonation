import json
class Radio:
    stationName = []
    station = [] #url
    stationNumber = 0
    def __init__(self):
        with open('../radio.txt', 'r', encoding='utf-8') as f:
            for item in f.readlines():
                data = json.loads(item)
                self.stationName.append(data['name'])
                self.station.append(data['url'])
