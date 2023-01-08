import sqlite3
import json

appDict = {'dd': 'dd',
            'rit': 'rit'}

con = sqlite3.connect('RDB/SmartTakeout.sqlite')
cursor = con.cursor()

def sanitizeInput(input):
    out = input.replace('\'', '\\\'')
    return out

def getKeyFromAltNames(name, source, merchant_name=None):
    if source == 'merchant':
        res = cursor.execute('SELECT * FROM main.merchant_names;')
    elif source == 'item':
        res = cursor.execute('SELECT name, alt_names FROM main.items WHERE merchant_name = ?;', [merchant_name])
    else:
        return None
    for row in res.fetchall():
        if row[1] is not None:
            for alt_name in json.loads(row[1]):
                if alt_name.lower() == name.lower():
                    return row[0]
    return None

# def getNameRecord(name, source, merchant_name=None):
#     if source == 'merchant':
#         res = cursor.execute('SELECT name, alt_names FROM main.merchant_names WHERE name = ?;', [name])
#     elif source == 'item':
#         res = cursor.execute('SELECT name, alt_names FROM main.items WHERE merchant_name = ?, name = ?;', [merchant_name, name])
#     else:
#         res = None
#     if res is not None:
#         return res.fetchone()
#     else:
#         return None

def getAltNames(name, source, merchant_name=None):
    if source == 'merchant':
        res = cursor.execute('SELECT alt_names FROM main.merchant_names WHERE name = ?;', [name])
    elif source == 'item':
        res = cursor.execute('SELECT alt_names FROM main.items WHERE merchant_name = ?, name = ?;', [merchant_name, name])
    else:
        res = None
    if res is not None:
        alt_names_json = res.fetchone()[0]
        return json.loads(alt_names_json) if alt_names_json is not None else alt_names_json
    else:
        return None

def addAltNames(name, alt_names, source, merchant_name=None):
    cur_alt_names = getAltNames(name, source, merchant_name)
    if cur_alt_names is not None:
        new_names = []
        for alt_name in alt_names:
            if alt_name not in cur_alt_names:
                new_names.append(alt_name)
        cur_alt_names.extend(new_names)
        alt_names = cur_alt_names
    json_alt_names = json.dumps(alt_names)
    if source == 'merchant':
        cursor.execute('UPDATE main.merchant_names SET alt_names = ? WHERE (name = ?);', [json_alt_names, name])
    elif source == 'item':
        cursor.execute('UPDATE main.items SET alt_names = ? WHERE merchant_name = ?, name = ?;', [json_alt_names, merchant_name, name])
    con.commit()

def insertMerchant(name, ritual=False):
    alt_names_to_add = None
    if ritual==True and name.split(' (')[0] != name:
        alt_names_to_add = [name]
        name = name.split(' (')[0]
    res = cursor.execute('SELECT name FROM main.merchant_names WHERE name = ?;', [name])
    row = res.fetchone()
    if row is None:
        key_name = getKeyFromAltNames(name, 'merchant')
        # Name not in DB
        if key_name is None:
            if alt_names_to_add is not None:
                cursor.execute('INSERT INTO main.merchant_names (name, alt_names)'
                        'VALUES (?, ?)'
                        'ON CONFLICT(name)'
                        'DO NOTHING;', [name, json.dumps(alt_names_to_add)])
                con.commit()
                return name
            cursor.execute('INSERT INTO main.merchant_names (name)'
                    'VALUES (?)'
                    'ON CONFLICT(name)'
                    'DO NOTHING;', [name])
            con.commit()
            return name
        # Name in alt names
        else:
            if alt_names_to_add is not None:
                addAltNames(key_name, alt_names_to_add, 'merchant')
            con.commit()
            return key_name
    # Name is already a key
    else:
        retrieved_name = row[0]
        if alt_names_to_add is not None:
            addAltNames(retrieved_name, alt_names_to_add, 'merchant')
        con.commit()
        return retrieved_name

def upsertItem(merchant_name, name, app, price):
    # merchant_name = sanitizeInput(merchant_name)
    # name = sanitizeInput(name)
    appName = appDict[app]
    # priceStr = str(price)
    cursor.execute('INSERT INTO main.items (merchant_name, name, ' + appName + '_price_listed, ' + appName + '_price_actual)'
                   'VALUES (?, ?, ?, ?)'
                   'ON CONFLICT(merchant_name, name)'
                   'DO UPDATE SET ' + appName + '_price_listed=?, ' + appName + '_price_actual=?;',
                   (merchant_name, name, price, price, price, price))
    con.commit()

# insertMerchant('Avli River North')
# upsertItem('Avli River North', 'Greek Salad', 'dd', 16.0)