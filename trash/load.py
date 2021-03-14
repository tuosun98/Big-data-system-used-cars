import requests, json



head = 'https://vpic.nhtsa.dot.gov/api'
tail = '/vehicles/DecodeVinValuesExtended/JTHBZ1BL7JA013785?format=json'
r = requests.get(head + tail)
a = r.json()
