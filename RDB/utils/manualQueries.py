import sqlite3
import json
import queries

con = sqlite3.connect('RDB/SmartTakeout.sqlite')
cursor = con.cursor()

def addAltMerchant(name, alt_names):
    if selectMerchantName(name) is not None:
        queries.addAltNames(name, [alt_names], 'merchant')

def selectMerchantName(name):
    res = cursor.execute('SELECT name FROM main.merchant_names WHERE name = ?;', [name])
    # print(res.fetchall())
    print(res.arraysize)
    name = res.fetchone()
    # print(res.arraysize + ' ' + name)
    print(name)
    con.commit()
    return name[0] if name is not None else name

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
                if alt_name == name:
                    return row[0]
    return None

def combineMerchants(master, duplicates):
    if selectMerchantName(master) is not None:
        for duplicate in duplicates:
            fetched_dup_key = selectMerchantName(duplicate)
            con.commit()
            if fetched_dup_key is not None:
                dup_alt_names = queries.getAltNames(fetched_dup_key, 'merchant')
                if dup_alt_names is not None:
                    queries.addAltNames(master, dup_alt_names, 'merchant')
                queries.addAltNames(master, [fetched_dup_key], 'merchant')
                # delcon = sqlite3.connect('RDB/SmartTakeout.sqlite')
                # delcursor = delcon.cursor()
                con.execute('DELETE FROM main.merchant_names WHERE name = ?;', [fetched_dup_key])
                con.commit()
                con.close()


# print(getKeyFromAltNames("Tamale", 'item', "Al's Beef"))
# selectMerchantName("al's Beef")
combineMerchants('Brown Bag Seafood', ['Brown Bag Seafood Co.'])
# addAltMerchant("Protein Bar & Kitchen", ['Protein Bar'])
# combineMerchants('Protein Bar & Kitchen', ['The Protein Bar and Kitchen'])