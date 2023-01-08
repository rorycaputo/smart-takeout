import json
import os
from RDB.utils.queries import *

def parseBffExplore():
    directory = 'DoorDash/data/bffExplore'
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r', encoding='utf8') as dd_file:
            dd_data = json.load(dd_file)
            for merchant in dd_data['display_modules'][0]['data']['content']:
                # print(merchant['name'])
                # TODO find name in altNames if it don't exist
                insertMerchant(merchant['name'])
                for item in merchant['items']:
                    unit_amount = int(item['price_details']['unit_amount'])
                    decimal_places = int(item['price_details']['decimal_places'])
                    price = unit_amount / 10**decimal_places
                #     print('   ' + item['name'] + ' ' + str(price))
                    upsertItem(merchant['name'], item['name'], 'dd', price)
            dd_file.close()
