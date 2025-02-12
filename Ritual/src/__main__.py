# prompts the user for several values:
# merchant - just an input string
# items - a list of objects that each map a string to options. Supplied 1-by-1 by the user
# options - a list of strings that go with each item. Each entered item should prompt the user for any number of options, 1-by-1
# If a user inputs 'done' or an empty string for an option, move to the next option
# If a user inputs 'done' or an empty string for an item, stop prompting for items

import apis
import util
import json
import requests

service = 'Ritual'

def prompt_inputs(merchant):
    if not merchant:
        merchant = input("Name of merchant: ")
    print(merchant)

    items = []

    while True:
        empty_cart = len(items) == 0
        item = None
        if(empty_cart):
            item = input("Enter an item: ")
        else:
            item = input("Enter another item, or when finished hit Enter: ")
        if not item:
            if(empty_cart):
                print("No items entered - aborting")
                return
            break
        options = []
        while True:
            option = input(f'Enter an option for the {item}, or when finished hit Enter: ')
            if option == "":
                break
            options.append(option)
        items.append({"item_name": item, "options": options})

    print(items)
    return {"merchant": merchant, "items": items}

def get_merchant_data(merchant_name):
    print(f'Searching {service} merchants: {merchant_name}')
    search_html = apis.lookup_merchant(merchant_name)
    if not search_html:
        return None
    print(f'Done')
    script_json = util.extract_script_from_html(search_html)
    if not script_json:
        return None
    # todo parmaterize
    path = 'props.initialState.catalog.nearbyMerchantsData.data'
    search_results = util.extract_object(script_json, path)
    if not search_results:
        return None

    #todo parameterize
    user_lat = 41.895033
    user_lon = -87.626613

    closest_merchant = util.find_closest_merchant(search_results, merchant_name, user_lat, user_lon)
    # print(closest_merchant)
    return closest_merchant

def get_merchant_menu(merchant_data):
    print(f'Loading {service} merchant: {merchant_data["name"]}')
    merchant_html = apis.get_menu(merchant_data['menuPath'])
    print(f'Done')
    if not merchant_html:
        return None
    script_json = util.extract_script_from_html(merchant_html)
    if not script_json:
        return None
    items_path = 'props.initialState.menu.data.items'
    id_path = 'props.initialState.menu.data.id'
    return {
        "id": util.extract_object(script_json, id_path),
        "items": util.extract_object(script_json, items_path),
        "sub_domain_id": util.extract_object(script_json, 'props.initialState.order.source.subdomainId')
        }

def main (merchant_input="l", items_input=['Turkey Pronto Sandwich']):
    order = prompt_inputs(merchant_input)
    merchant_data = get_merchant_data(order['merchant'])
    menu = get_merchant_menu(merchant_data)
    session = requests.Session()
    for item_input in order['items']:
        # todo llm
        menu_item = util.find_item(menu['items'], item_input['item_name'])
        if not menu_item:
            print(f'Item not found in menu: {item_input["item_name"]}')
            return
        # print(menu_item)
        print(f'Fetching item choices for the {menu_item["title"]}')
        item_choices = apis.get_item_choices(menu['id'], menu_item['id'], menu['sub_domain_id'])
        print(f'Done')
        # print(item_choices)
        item_options = util.get_item_options(item_choices['choices'], item_choices['options'], item_input['options'])
        print(item_options)

        print(f'Adding {menu_item["title"]} to {service} cart')
        response, session = apis.add_item_to_cart(session, merchant_data['id'], menu_item, util.format_option_ids(item_options), menu['sub_domain_id'])
        print(f'Done')
    print(f'Total {service} Price: ${response["financialInfo"]["totalPayableMicro"] / 100000000}')
    return

if __name__ == '__main__':
#     import argparse

#     parser = argparse.ArgumentParser(description='Create a Ritual Order')
#     parser.add_argument('--merchant', metavar='path', required=True,
#                         help='name of the merchant you\'re ordering from')
#     # add a list of string arguments called 'options'
#     parser.add_argument('options', metavar='options', nargs='+\*',
#                         help='options list to include in the order')
#     args = parser.parse_args()
#     main(workspace=args.workspace, schema=args.schema, dem=args.dem)
    main()

