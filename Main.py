from UI.UserInterface import TableFrame, EditFrame
from Domain.Table import Table

from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError

from datetime import datetime

customers = [[3110002920, 'Árni', 'Dagur', True, datetime(2000, 10, 31)],
             [1506995079, 'Viktor', 'Máni', False, datetime.now()]]
customertable = Table(
    'Customers.txt',
    ['Kennitala', 'First Name', 'Last name', 'Is awesome', 'DOB'],
    [int, str, str, bool, datetime]
)
vehicletable = Table(
    'Vehicles.txt',
    ['Number of seats', 'Fuel consumption', 'Model', 'Year', 'Airbags'],
    [int, float, str, datetime, bool]
)

#  orders = [['aeo123ao', 'Lamborgini', True, False]]
#  ordertable = Table('ord', ['ID', 'Model', 'Is awesome', 'GPS'])

# PRICES = [
#     ['Small cars:', '2.900 ISK', '20.300 ISK', '87.000 ISK', '389.000 ISK'],
#     ['Medium cars:', '3.900 ISK', '27.300 ISK', '117.000 ISK', '489.000 ISK'],
#     ['Large cars:', '4.900 ISK', '34.300 ISK', '147.000 ISK', '598.000 ISK'],
#     ['Jeep:', '5.900 ISK', '41.300 ISK', '177.000 ISK', '998.000 ISK'],
# ]
# PRICE_LIST= [
# ['Small Car', '2900 ISK', '20300 ISK', '87000 ISK', '527800 ISK']
# ['Medium car', '3900 ISK', '27300 ISK', '117000 ISK', '709800 ISK']
# ['Large car', '4900 ISK', '34300 ISK', '147000 ISK', '891800 ISK']
# ['Jeep', '5900 ISK', '41300 ISK', '177000 ISK', '1073800 ISK']
# ['Basic insurance', '0 ISK', '0 ISK', '0 ISK', '0 ISK']
# ['silver insurance', '250 ISK', '1750 ISK', '7500 ISK', '45500 ISK']
# ['Gold insurance', '450 ISK', '3150 ISK', '13500 ISK', '81900 ISK'] ]

PRICE = {'Small Car':2900, 'Medium car': 3900, 'Large car': 4900, 'Jeep': 5900,
'Basic insurance': 0, 'silver insurance': 250, 'Gold insurance': 450}
PRICE_LIST= [[key, '{} ISK'.format(value ), '{} ISK'.format(value*7 ), '{} ISK'.format(value*30 ), 
'{} ISK'.format(value*182)] for key, value in PRICE.items()]

#PRICES_TABLE = Table(PRICE_LIST, ['', '1 day', '1 week', '1 month', '6 months'])


def demo(screen):
    screen.play([
        #Scene([TableFrame(screen, PRICES_TABLE, 'pricelist', 'Prices')], -1, name='pricelist'),
        Scene([TableFrame(screen, vehicletable, 'customeredit', 'Customers')], -
              1, name='customertable'),
        Scene([EditFrame(screen, vehicletable, 'customertable')], -
              1, name='customeredit'),
        #  Scene([TableFrame(screen, ordertable, 'orderedit')], -1, name='ordertable'),
        #  Scene([EditFrame(screen, ordertable, 'ordertable')], -1, name='orderedit')
    ], stop_on_resize=True)


while True:
    try:
        Screen.wrapper(demo, catch_interrupt=True)
        exit()
    except ResizeScreenError:
        pass
