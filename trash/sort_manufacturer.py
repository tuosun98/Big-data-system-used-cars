import json
import pandas as pd

first_header, mode = True, 'w'
i = 1
while True:
    try:
        with open('manufacturer/manu_{index}.json'.format(index=i)) as f:
            a = json.load(f)
            df = pd.DataFrame(a['Results'])
            df.to_csv('manufacturer.csv', header=first_header, index=False, mode=mode)
            first_header, mode = False, 'a'
            i += 1
    except FileNotFoundError:
        break
