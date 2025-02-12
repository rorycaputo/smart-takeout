import requests

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'utf-8',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Priority': 'u=0, i'
        # 'Cookie': 'ra_device_id=a16fa42edc5e4a8d95b57dc9d362c44c; ra_entity_id=8907bfaa0d8745e5b7ba97ca916a910e; ra_entity_type=EXTERNAL_USER; ra_session_id=cd7c37b7115c4da28024972f0c2c43a3; ritual_analyticssessionid=ece6f9d37d6d491384744abbe25cde2b; ritual_externalanalyticssessionid=da1d31d0eb1a477fa1a85fa69db0d4cd; ritual_externaluserid=da1d31d0eb1a477fa1a85fa69db0d4cd; rt-lang=en-US'
    }

def lookup_merchant(merchant_name, location='chicago-il', user_lat='+41.894151', user_lon='-87.6359'):
    url = f'https://ritual.co/order/city/{location}'
    params = {'q': merchant_name}
    return call_get_api(url, None, params).text

# todo parametrize
def get_menu(menu_path, location='chicago-il', user_lat='+41.894151', user_lon='-87.6359'):
    url = f'https://store.ritual.co/order/{menu_path}'
    params = {'q': '',
              'on': '1',
              'op': '1',
              'lat': user_lat,
              'lon': user_lon,
              'city': {location}}
    return call_get_api(url, None, params).text

def get_item_choices(menu_id, item_id, sub_domain_id=''):
    url = f'https://athena.ritual.co/v1/menu/{menu_id}/items/{item_id}/choices'
    choices_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': ',en-US;q=0.9',
        'Accept-Encoding': 'utf-8',
        'x-ritual-order-source': 'RITUAL_APP',
        'x-ritual-order-source-subdomain': 'store',
        'x-ritual-order-source-subdomain-id': sub_domain_id,
        'Origin': 'https://store.ritual.co',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://store.ritual.co/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Priority': 'u=0',
        'TE': 'trailers'
    }
    return call_get_api(url, choices_headers).json()

def call_get_api(url, headers=headers, params=None):
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        return response
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return http_err
    except requests.exceptions.ConnectionError as conn_err:
        print(f'Error connecting to the API: {conn_err}')
        return conn_err
    except requests.exceptions.Timeout as timeout_err:
        print(f'Timeout error occurred: {timeout_err}')
        return timeout_err
    except requests.exceptions.RequestException as err:
        print(f'Something went wrong: {err}')
        return err

import requests
import json

def add_item_to_cart(session, merchant_id, cart_item, options, sub_domain_id=''):
    url = f'https://athena.ritual.co/v1/cart/{merchant_id}/item'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': ',en-US;q=0.9',
        'Accept-Encoding': 'utf-8',
        'Content-Type': 'application/json;charset=utf-8',
        'x-ritual-order-source': 'RITUAL_APP',
        'x-ritual-order-source-subdomain': 'store',
        'x-ritual-order-source-subdomain-id': sub_domain_id,
        'Origin': 'https://store.ritual.co',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://store.ritual.co/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Priority': 'u=0',
        'TE': 'trailers'
    }

    data = {
        "menuItemId": cart_item['id'],
        "quantity": 1, # todo
        "note": "",
        # [{"id":"4002005","incrementCount":1},{"id":"3531328","incrementCount":1}]
        "cartItemOptions": options,
        "title": cart_item['title'],
        "priceMicro": cart_item['priceMicro'],
    }

    response = session.post(url, headers=headers, data=json.dumps(data))

    return response.json(), session
