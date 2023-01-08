import requests
from bs4 import BeautifulSoup
from Ritual.src.merchantReader import readMerchant
from RDB.utils.queries import *

coords = {'home': 'lat=41.8937619&lon=-87.6353731'}

def fetchMerchantMenus():
    response = requests.get('https://ritual.co/order/city/chicago-il?' + coords['home'])
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.content, "html.parser")
    merchant_links = soup.select('a[class*="MerchantCard__LinkContainer-"]')
    # print(merchant_links[0].select('h3[class*="MerchantCard__Name"]')[0].text)
    for link in merchant_links:
        merchant_name = link.select('h3[class*="MerchantCard__Name"]')[0].text
        # print(merchant_name + ' ' + link.get('href'))
        print(insertMerchant(merchant_name, True))
        # readMerchant(link.get('href'))