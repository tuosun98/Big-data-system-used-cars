import requests, json


key_vin = json.load(open('key_vin.json'))
url = 'https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValuesExtended/{vin}?format=json'
vin_info = dict()

for key in key_vin:
    api_info = requests.get(url.format(vin=key_vin[key])).json()
    vin_info[key] = api_info['Results'][0]

with open('vin_info.json', 'w') as f:
    f.write(json.dumps(vin_info, indent=1))


requests.put('https://dsci551-project-sample-default-rtdb.firebaseio.com/vin_api.json', data=open('vin_info.json'))
