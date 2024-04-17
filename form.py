import requests
import datetime
import pytz
import json
import math

""" https://www.buda.com/api/v2/markets/btc-clp/trades?timestamp=1709308800&limit=50 """

dt = datetime.datetime(2024, 3, 1, 13, 0, 0)
timezone = pytz.timezone('Etc/GMT+3')
dt = timezone.localize(dt)
last_timestamp = int(dt.timestamp() * 1000)
TIMESTAMP_2024_12 = 1709305200000 # 1709305200000 is the timestamp for 2024-03-01 12:00:00 GMT-3
TIMESTAMP_2024_13 = 1709308800000 # 1709308800000 is the timestamp for 2024-03-01 13:00:00 GMT-3
TIMESTAMP_2023_12 = 1677682800000 # 1677682800000 is the timestamp for 2023-03-01 12:00:00 GMT-3
TIMESTAMP_2023_13 = 1677686400000 # 1677686400000 is the timestamp for 2023-03-01 13:00:00 GMT-3

market_id = 'btc-clp'
callNumber = 0

# 2024 entries

while(last_timestamp > TIMESTAMP_2024_12):
    if callNumber > 4:
        break
    url = f'https://www.buda.com/api/v2/markets/{market_id}/trades?timestamp={last_timestamp}"&"limit=50'
    response = requests.get(url)
    dataAdd = response.json()
    if(last_timestamp == TIMESTAMP_2024_13):
        data = dataAdd
    else:
        data['trades']['entries'] += dataAdd['trades']['entries']
    last_timestamp = int(dataAdd['trades']['last_timestamp'])
    callNumber += 1

json_str = json.dumps(data, indent=4)

entries = json.loads(json_str)['trades']['entries']
valid_entries_2024 = []
valid_entries_money_quantity_2024 = 0.0
valid_entries_BTC_quantity_2024 = 0.0
for entry in entries:
    if int(entry[0]) >= TIMESTAMP_2024_12:
        valid_entries_2024.append(entry)
        valid_entries_money_quantity_2024 += float(entry[1]) * float(entry[2])
        valid_entries_BTC_quantity_2024 += float(entry[1])

print("Pregunta 1: " + str(math.floor(valid_entries_money_quantity_2024 * 100) / 100))

# 2023 entries

dt = datetime.datetime(2023, 3, 1, 13, 0, 0)
dt = timezone.localize(dt)
last_timestamp = int(dt.timestamp() * 1000)

callNumber = 0

while(last_timestamp > TIMESTAMP_2023_12):
    if callNumber > 4:
        break
    url = f'https://www.buda.com/api/v2/markets/{market_id}/trades?timestamp={last_timestamp}"&"limit=50'
    response = requests.get(url)
    dataAdd = response.json()
    if(last_timestamp == TIMESTAMP_2023_13):
        data = dataAdd
    else:
        data['trades']['entries'] += dataAdd['trades']['entries']
    last_timestamp = int(dataAdd['trades']['last_timestamp'])
    callNumber += 1

json_str = json.dumps(data, indent=4)

entries = json.loads(json_str)['trades']['entries']
valid_entries_2023 = []
valid_entries_money_quantity_2023 = 0.0
valid_entries_BTC_quantity_2023 = 0.0
for entry in entries:
    if int(entry[0]) >= TIMESTAMP_2023_12:
        valid_entries_2023.append(entry)
        valid_entries_money_quantity_2023 += float(entry[1]) * float(entry[2])
        valid_entries_BTC_quantity_2023 += float(entry[1])

percentage_increase = ((valid_entries_BTC_quantity_2024 - valid_entries_BTC_quantity_2023) / valid_entries_BTC_quantity_2023) * 100

print("Pregunta 2: " + str(math.floor(percentage_increase * 100) / 100))

comission = str(math.floor((valid_entries_money_quantity_2024 * 0.008) * 100) / 100 )

print("pregunta 3: " + comission)



