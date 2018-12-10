PRICE = {'Small Car':2900, 'Medium car': 3900, 'Large car': 4900, 'Jeep': 5900,
'Basic insurance': 0, 'silver insurance': 250, 'Gold insurance': 450}
PRICE_LIST= [[key, '{} ISK'.format(value ), '{} ISK'.format(value*7 ), '{} ISK'.format(value*30 ), 
'{} ISK'.format(value*182)] for key, value in PRICE.items()]

for Item in PRICE_LIST:
    print(Item)