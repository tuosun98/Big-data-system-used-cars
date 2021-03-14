import requests, json

def get_manufacturer(start=0, step=1):
    head = 'https://vpic.nhtsa.dot.gov/api'
    tail = '/vehicles/GetAllManufacturers?format=json&page='
    num = start+1
    while True:
        try:
            r = requests.get(head+tail+str(num))
        except requests.exceptions.ProxyError:
            continue

        a = r.json()
        if a['Count'] == 0:
            print(num)
            break
        with open('manufacturer/manu_{num}.json'.format(num=num), 'w') as f:
            f.write(json.dumps(a, indent=1))
        print(num)
        num += step