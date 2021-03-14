import requests, json


key_zip = json.load(open('key_position.json'))
url = 'http://api.zippopotam.us/us/{zipcode}'
zip_info = dict()

for key in key_zip:
    api_info = requests.get(url.format(zipcode=key_zip[key][-5:])).json()
    zip_info[key] = api_info['places'][0]

with open('pos_info.json', 'w') as f:
    f.write(json.dumps(zip_info, indent=1))


requests.put('https://dsci551-project-sample-default-rtdb.firebaseio.com/zipcode_api.json', data=open('pos_info.json'))
