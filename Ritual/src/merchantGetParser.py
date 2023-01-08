import json
import os
from RDB.utils.queries import *
from Ritual.src.merchantReader import readMerchant

baseUrl = 'https://store.ritual.co/order'

def parseMerchantGet():
    directory = 'Ritual/data/'
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r', encoding='utf8') as rit_file:
            rit_data = json.load(rit_file)
            for merchant in rit_data['data']:
                # print(merchant['name'])
                # TODO find name in altNames if it don't exist
                insertMerchant(merchant['nameWithoutLocation'], True)
                
                # merchant_items = readMerchant(baseUrl + merchant['menuPath'])


                # for item in merchant['items']:
                #     unit_amount = int(item['price_details']['unit_amount'])
                #     decimal_places = int(item['price_details']['decimal_places'])
                #     price = unit_amount / 10**decimal_places
                # #     print('   ' + item['name'] + ' ' + str(price))
                #     upsertItem(merchant['name'], item['name'], 'dd', price)
            rit_file.close()
