from UI.UserInterface import TableFrame, EditFrame
from Domain.Table import Table
from Data.Data import ID
from Domain.PriceFrame import PRICE,PriceFrame
from Domain.GraphFrame import GraphFrame
from Domain.WelcomeFrame import demoWelcome
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError

from datetime import datetime, timedelta

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
    plate = row[2]

    price_p_day = PRICE['Small Car']
    for row in vehicletable.get_rows():
        if plate in row.values():
            if row.values()[-1].lower() in ['medium', 'medium car']:
                price_p_day = PRICE['Medium Car']
            elif row.values()[-1].lower() in ['large', 'large car']:
                price_p_day = PRICE['Large Car']
            elif row.values()[-1].lower() in ['jeep']:
                price_p_day = PRICE['Jeep']
            break
    if has_insurance:
        price_p_day += PRICE['Extra insurance']
    if has_gps:
        price_p_day += PRICE['GPS']

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
        start_date, end_date = order[3].value(), order[4].value()
        if order_plate == my_plate and start_date <= datetime.now() < (end_date + timedelta(days = 1)):
            return 'True'
    return 'False'

vehicletable = Table(
    'Vehicles.txt',
    ['License Plate', 'Manufacturer', 'Model', 'Year', 'Location', 'Category'],
    [str, str, str, int, str, str],
    runtime_columns=[('Occupied', is_taken, [ordertable])]
)

keybinds = {
    'c': 'Customer Table',
    'o': 'Order Table',
    'v': 'Vehicle Table',
    'p': 'Price List',
    'g': 'Statistics'
}

def demo(screen):
    screen.play([
        Scene([TableFrame(screen, customertable, 'customeredit', 'Customers', scene_keybinds=keybinds, footer=keybinds)], -
              1, name='Customer Table'),
        Scene([EditFrame(screen, customertable, 'Customer Table')], -
              1, name='customeredit'),
        Scene([TableFrame(screen, ordertable, 'orderedit', 'Orders', scene_keybinds=keybinds, footer=keybinds)], -1, name='Order Table'),
        Scene([EditFrame(screen, ordertable, 'Order Table')], -1, name='orderedit'),
        Scene([TableFrame(screen, vehicletable, 'vehicleedit', 'Vehicles', scene_keybinds=keybinds, footer=keybinds)], -1, name='Vehicle Table'),
        Scene([EditFrame(screen, vehicletable, 'Vehicle Table')], -1, name='vehicleedit'),
        Scene([PriceFrame(screen, footer=keybinds, scene_keybinds=keybinds)], -1, name='Price List'),
        Scene([GraphFrame(screen, footer=keybinds, scene_keybinds=keybinds)], -1, name='Statistics')
    ], stop_on_resize=True)

while True:
    try:
        Screen.wrapper(demoWelcome)
        break
    except ResizeScreenError:
        pass
while True:
    try:
        Screen.wrapper(demo, catch_interrupt=True)
        exit()
    except ResizeScreenError:
        pass