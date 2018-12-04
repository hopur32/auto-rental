from UI.UserInterface import TableFrame, EditFrame
from Domain.Table import Table

from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError

rows = [[str(i)+'dstndtns', str(i+1)+'12312312', str(i+2)+'tsdndtns']
        for i in range(0, 100, 3)]

table = Table(rows, ['one', 'two', 'three'])
def demo(screen):
    screen.play([
        Scene([TableFrame(screen, table, 'edit')], -1, name='table'),
        Scene([EditFrame(screen, table, 'table', table.get_column_names())], -1, name='edit')
    ], stop_on_resize=True)

while True:
    try:
        Screen.wrapper(demo, catch_interrupt=True)
        exit()
    except ResizeScreenError:
        pass

