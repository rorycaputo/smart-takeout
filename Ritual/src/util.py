import json
import math
from lxml import html

def extract_script_from_html(input_html):
    tree = html.fromstring(input_html)
    # with open('output1.html', 'w') as f:
    #     f.write(html.tostring(tree, encoding='unicode'))
    script_tag = tree.xpath('//script[@id="__NEXT_DATA__"]')
    if script_tag:
        data = script_tag[0].text
        try:
            json_data = json.loads(data)
            return json_data
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return None
    else:
        print("Script tag with id '__NEXT_DATA__' not found")
        return None
    
def extract_object(json_input, path):
    try:
        path_parts = path.split('.')
        current_data = json_input
        for part in path_parts:
            current_data = current_data[part]
        return current_data
    except KeyError as e:
        print(f'Key not found in JSON: {e}')
        return None
    
def find_closest_merchant(merchant_list, merchant_name, user_lat, user_lon):
    closest_merchant = None
    closest_distance = float('inf')

    merchant_names =  [item['nameWithoutLocation'] for item in merchant_list]

    for merchant in merchant_list:
        # todo llm
        if merchant['nameWithoutLocation'].casefold() == merchant_name.casefold():
            merchant_lat = merchant['location']['latitude']
            merchant_lon = merchant['location']['longitude']

            distance = math.sqrt((merchant_lat - user_lat) ** 2 + (merchant_lon - user_lon) ** 2)

            if distance < closest_distance:
                closest_distance = distance
                closest_merchant = merchant

    if closest_merchant:
        # return closest_merchant['id']
        return closest_merchant
    else:
        return None
    
def find_item(menu_items, item_name):
    for item in menu_items.items():
        if item[1]['title'] == item_name:
            return item[1]
    return None

# def get_lowest_price_ids(choices, options, preferred_titles):
#     result = {}
#     for choice_id, choice in choices.items():
#         min_selectable = choice['minSelectable']
#         option_ids = choice['optionIds']
#         preferred_option_ids = [option_id for option_id in option_ids if options[option_id]['title'] in preferred_titles]
#         if len(preferred_option_ids) < min_selectable:
#             additional_option_ids = [option_id for option_id in option_ids if option_id not in preferred_option_ids]
#             prices = [(option_id, options[option_id]['priceMicro']) for option_id in additional_option_ids]
#             prices.sort(key=lambda x: x[1])
#             additional_option_ids = [option_id for option_id, _ in prices]
#             preferred_option_ids += additional_option_ids[:min_selectable - len(preferred_option_ids)]
#         result[choice_id] = preferred_option_ids[:min_selectable]
#     return result

def get_item_options(choices, options, preferred_titles):
    result = {}
    for choice_id, choice in choices.items():
        min_selectable = choice['minSelectable']
        max_selectable = choice['maxSelectable']
        option_ids = choice['optionIds']
        preferred_option_ids = [option_id for option_id in option_ids if options[option_id]['title'] in preferred_titles]
        preferred_option_ids = preferred_option_ids[:max_selectable] if max_selectable > 0 else preferred_option_ids # limit to maxSelectable
        remaining_option_ids = [option_id for option_id in option_ids if option_id not in preferred_option_ids]
        prices = [(option_id, options[option_id]['priceMicro']) for option_id in remaining_option_ids]
        prices.sort(key=lambda x: x[1])
        additional_option_ids = [option_id for option_id, _ in prices]
        result[choice_id] = preferred_option_ids + additional_option_ids[:max(0, min_selectable - len(preferred_option_ids))]
    return result

def format_option_ids(option_choices_list_obj):
    result = []
    for option_list in option_choices_list_obj.values():
        for id in option_list:
            result.append({"id": id, "incrementCount": 1})
    return result