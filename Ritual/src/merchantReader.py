import requests
from bs4 import BeautifulSoup



def readMerchant(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.content, "html.parser")

    items = soup.select('div[class*="MenuItem__FlexColumn"]')
    item_dict = {}
    for item in items:
        item_name = item.select('p[class*="MenuItem__Title"]')[0].text
        item_price = float(item.select('span[class*="ItemPrice__RegularText"]')[0].text[1:])
        item_dict[item_name] = item_price

    return item_dict