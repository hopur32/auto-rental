from UI.UserInterface import TableFrame, EditFrame
from Domain.Table import Table
from Data.Data import ID

from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError

from datetime import datetime

customertable = Table(
    'Customers.txt',
    ['Kennitala', 'First Name', 'Last name', 'Phone Nr.', 'Email', 'DOB', 'Credit Card', 'Expiration Date', 'Nationality'],
    [str, str, str, str, str, datetime, str, datetime, str]
)

def calc_price(row):
    row = row.values()
    start, end = row[3], row[4]
    days = (end - start).days + 1
    has_insurance, has_gps = row[5], row[6]

    price_p_day = 3000
    if has_insurance:
        price_p_day += 1000
    if has_gps:
        price_p_day += 350

    return str(price_p_day * days)
ordertable = Table(
    'Orders.txt',
    ['Order ID', 'Customer', 'Vehicle', 'Start Date', 'End Date', 'Extra Insurance', 'GPS'],
    [ID, str, str, datetime, datetime, bool, bool],
    runtime_columns=[('Price', calc_price, [])]
)

def is_taken(row, order_table):
    order_table.update_cache()
    my_plate = row.display()[0]
    for order in order_table.get_rows():
        order_plate = order.display()[2]
        if order_plate == my_plate:
            return 'True'
    return 'False'
vehicletable = Table(
    'Vehicles.txt',
    ['License Plate', 'Manufacturer', 'Model', 'Year', 'Location', 'Category'],
    [str, str, str, int, str, str],
    runtime_columns=[('Occupied', is_taken, [ordertable])]
)

keybinds = {
    'c': 'customertable',
    'o': 'ordertable',
    'v': 'vehicletable'
}

def demo(screen):
    screen.play([
        Scene([TableFrame(screen, customertable, 'customeredit', 'Customers', scene_keybinds=keybinds)], -
              1, name='customertable'),
        Scene([EditFrame(screen, ordertable, 'customertable')], -
              1, name='customeredit'),
        Scene([TableFrame(screen, ordertable, 'orderedit', 'Orders', scene_keybinds=keybinds)], -1, name='ordertable'),
        Scene([EditFrame(screen, ordertable, 'ordertable')], -1, name='orderedit'),
        Scene([TableFrame(screen, vehicletable, 'vehicleedit', 'Vehicles', scene_keybinds=keybinds)], -1, name='vehicletable'),
        Scene([EditFrame(screen, vehicletable, 'vehicletable')], -1, name='vehicleedit')
    ], stop_on_resize=True)


while True:
    try:
        Screen.wrapper(demo, catch_interrupt=True)
        exit()
    except ResizeScreenError:
        pass
