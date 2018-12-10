from UI.UserInterface import TableFrame, EditFrame
from Domain.Table import Table

from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError

from datetime import datetime

customers = [[3110002920, 'Árni', 'Dagur', True, datetime(2000, 10, 31)],
             [1506995079, 'Viktor', 'Máni', False, datetime.now()]]
customertable = Table(
    'customers',
    ['Kennitala', 'First Name', 'Last name', 'Is awesome', 'DOB'],
    [int, str, str, bool, datetime]
)

#  orders = [['aeo123ao', 'Lamborgini', True, False]]
#  ordertable = Table('ord', ['ID', 'Model', 'Is awesome', 'GPS'])


def demo(screen):
    screen.play([
        Scene([TableFrame(screen, customertable, 'customeredit')], -
              1, name='customertable'),
        Scene([EditFrame(screen, customertable, 'customertable')], -
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
