from UI.UserInterface import TableFrame, EditFrame
from Domain.Table import Table

from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError

from datetime import datetime
rows = [['3110002920', 'Árni', 'Dagur', True, datetime(2000, 10, 31)],
        ['1506995079', 'Viktor', 'Máni', False, datetime.now()]]

table = Table(rows, ['Kennitala', 'First Name', 'Last name', 'Is awesome', 'DOB'])
def demo(screen):
    screen.play([
        Scene([TableFrame(screen, table, 'edit')], -1, name='table'),
        Scene([EditFrame(screen, table, 'table')], -1, name='edit')
    ], stop_on_resize=True)

while True:
    try:
        Screen.wrapper(demo, catch_interrupt=True)
        exit()
    except ResizeScreenError:
        pass

