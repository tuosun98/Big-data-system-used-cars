import json
import pandas

# merge everything in car_data
# This file is just used to merge files for challenge data
new_json = dict()
for i in range(307):
    with open('car_data/cars_{batch_index}.json'.format(batch_index=i*100)) as f:
        new_json.update(json.load(f))
with open('car_data.json', 'w') as f:
    f.write(json.dumps(new_json, indent=4))

key, value = list(), list()
for i in range(307):
    with open('car_data/key_vin_{batch_index}.json'.format(batch_index=i*100)) as f:
        vindict = json.load(f)
        key += list(vindict.keys())
        value += list(vindict.values())
pandas.DataFrame({'ID': key, 'VIN': value}).to_csv('key_vin.csv')

key, value = list(), list()
for i in range(307):
    with open('car_data/key_position_{batch_index}.json'.format(batch_index=i*100)) as f:
        posdict = json.load(f)
        key += list(posdict.keys())
        value += list(posdict.values())
pandas.DataFrame({'ID': key, 'Position': value}).to_csv('key_pos.csv')

