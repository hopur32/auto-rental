from UI.UserInterface import TableFrame, EditFrame
from Domain.Table import Table, Row, Column

from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError

from datetime import datetime

customers = [[3110002920, 'Árni', 'Dagur', True, datetime(2000, 10, 31)],
             [1506995079, 'Viktor', 'Máni', False, datetime.now()]]
customertable = Table(
    customers, [
        'Kennitala', 'First Name', 'Last name', 'Is awesome', 'DOB'])

orders = [['aeo123ao', 'Lamborgini', True, False]]
ordertable = Table(orders, ['ID', 'Model', 'Is awesome', 'GPS'])

PRICES = [
    ['Small cars:', '2.900 ISK', '20.300 ISK', '87.000 ISK', '389.000 ISK'],
    ['Medium cars:', '3.900 ISK', '27.300 ISK', '117.000 ISK', '489.000 ISK'],
    ['Large cars:', '4.900 ISK', '34.300 ISK', '147.000 ISK', '598.000 ISK'],
    ['Jeep:', '5.900 ISK', '41.300 ISK', '177.000 ISK', '998.000 ISK'],
]

PRICES_TABLE = Table(PRICES, ['', '1 day', '1 week', '1 month', '6 months'])


def demo(screen):
    screen.play([
        Scene([TableFrame(screen, PRICES_TABLE, 'pricelist', 'Prices')], -1, name='pricelist'),
        Scene([TableFrame(screen, customertable, 'customeredit', 'Customers')], -
              1, name='customertable'),
        Scene([EditFrame(screen, customertable, 'customertable')], -
              1, name='customeredit'),
        Scene([TableFrame(screen, ordertable, 'orderedit')], -1, name='ordertable'),
        Scene([EditFrame(screen, ordertable, 'ordertable')], -1, name='orderedit')
    ], stop_on_resize=True)


while True:
    try:
        Screen.wrapper(demo, catch_interrupt=True)
        exit()
    except ResizeScreenError:
        pass
