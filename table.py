import string
from collections import defaultdict

from asciimatics.event import KeyboardEvent
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import MultiColumnListBox, Text, Frame, Layout, Widget, TextBox, Button
from asciimatics.exceptions import ResizeScreenError, StopApplication, NextScene

# import logging
# logging.basicConfig(filename='/tmp/debug.log',level=logging.DEBUG)

"""
Attributes:
    Public:
        self.current_row
    Private:
        self.__rows
        self.__num_cols
        self.__col_widths
        self.__col_names
"""
class Table():
    def __init__(self, rows, col_names):
        self.__col_names = col_names
        self.set_rows(rows)
        self.current_row = None

    # Row management:
    # --------------------------------------------------------------------------
    """
    Return private attribute self.__rows.
    """
    def get_rows(self):
        return self.__rows

    def get_row(self, row_index):
        return self.__rows[row_index]

    def get_current_row(self):
        if self.current_row == None:
            return [''] * self.__num_cols
        else:
            return self.__rows[self.current_row]

    """
    Validates input and sets self.__rows, self.__num_cols,
    and self.__col_widths().

    Panics:
        Raises valueerror if each row in the list of rows given does not have
        the same length.
    """
    def set_rows(self, rows):
        # First we make sure that each row has the same length
        first_num_cols = len(rows[0])
        for row in rows[1:]:
            if not len(row) == first_num_cols:
                raise ValueError(
                    'Each row in list of rows does not have the same length'
                )

        self.__rows = rows
        self.__num_cols = first_num_cols
        self._init_column_widths()

    def set_row(self, row, row_index):
        self.__rows[row_index] = row
        self._update_column_widths([len(col) for col in row])

    def edit_current_row(self, row):
        if self.current_row == None:
            self.add_row(row)
        else:
            self.set_row(row, self.current_row)

    """
    Delete the row at row_index. Does nothing if row_index == None.
    """
    def del_row(self, row_index):
        if row_index != None:
            del self.__rows[row_index]
            self._init_column_widths()

    """
    Add a row to table.

    Panics:
        This method raises ValueError if number of columns in given row
        does not equal self.__num_cols.
    """
    def add_row(self, row):
        # First we make sure that the number of columns in given row
        # equals self.__num_cols.
        num_given_cols = len(row)
        if not num_given_cols == self.__num_cols:
            raise ValueError(
                'Given row has an invalid number of columns; got {}, expected {}'.format(
                num_given_cols, self.__num_cols
            ))

        self.__rows.append(row)
        self._update_column_widths([len(col) for col in row])

    # Column widths:
    # --------------------------------------------------------------------------
    """
    Get the widths of the table's columns. This equals the width of the
    largest cell in each column.
    """
    def _init_column_widths(self):
        rows = self.__rows[:]
        rows.append(self.__col_names)

        widths = []
        for i in range(self.__num_cols):
            widths_in_col_i = [len(row[i]) for row in rows]
            biggest_width_in_col_i = max(widths_in_col_i)
            widths.append(biggest_width_in_col_i)

        self.__col_widths = widths

    def _update_column_widths(self, new_row_widths):
        self.__col_widths = [max(new, old) for new, old in zip(new_row_widths, self.__col_widths)]

    def get_column_widths(self):
            return self.__col_widths

    # Get other private attributes:
    # --------------------------------------------------------------------------
    def get_column_names(self):
        return self.__col_names

    def get_num_columns(self):
        return self.__num_cols

"""
Attributes:
    Public:
        self.table
    Private:
        self.__spacing

        self.__header
        self.__list
        self.__last_frame
"""
class TableFrame(Frame):
    def __init__(self, screen, table, edit_scene, header_text='TableFrame', spacing=1, has_border=False):
        self.table = table
        self.__edit_scene = edit_scene
        self.__spacing = spacing
        super().__init__(
            screen, screen.height, screen.width, has_border=has_border,
            name=header_text, on_load=self._reload_list
        )
        layout = Layout([1], fill_frame=True)
        # Header
        self.__header = TextBox(1, as_string=True)
        self.__header.disabled = True
        self.__header.custom_colour = "label"
        self.__header.value = header_text
        # List of rows
        self.__list = MultiColumnListBox(
            Widget.FILL_FRAME,
            [w + self.__spacing for w in self.table.get_column_widths()],
            [],
            titles=self.table.get_column_names(),
            name='row_index'
        )

        self.add_layout(layout)
        layout.add_widget(self.__header)
        layout.add_widget(self.__list)
        self.fix()

        # Change colours
        self.set_theme('monochrome')

    def process_event(self, event):
        # Do the key handling for this Frame.
        if isinstance(event, KeyboardEvent):
            if event.key_code in [ord('q'), ord('Q'), Screen.ctrl('c')]:
                raise StopApplication("User quit")
            elif event.key_code in [ord('a'), ord('A')]:
                self._add()
            elif event.key_code in [ord('e'), ord('E')]:
                self._edit()
            elif event.key_code in [ord('d'), ord('D')]:
                self._delete()

        # Now pass on to lower levels for normal handling of the event.
        return super().process_event(event)

    def _add(self):
        self.table.current_row = None
        raise NextScene(self.__edit_scene)

    def _edit(self):
        self.save()
        self.table.current_row = self.data['row_index']
        raise NextScene(self.__edit_scene)

    """
    Delete the selcted row from self.table and redraws the list.
    """
    def _delete(self):
        self.save()
        self.table.del_row(self.data['row_index'])
        self._reload_list()

    def _reload_list(self):
        # prev_value = self.__list.value
        # prev_start_line = self.__list.start_line

        list_data = [(row, i) for i, row in enumerate(self.table.get_rows())]
        column_widths = [w + self.__spacing for w in self.table.get_column_widths()]

        self.__list.options = list_data
        # self.__list.value = prev_value
        # self.__list.start_line = prev_start_line
        # Here we are editing a private attribute, and must thus be careful.
        # This is not an intended usecase by the module authors.
        self.__list._columns = column_widths

class EditFrame(Frame):
    def __init__(self, screen, table, table_scene, field_names):
        self.table = table
        self.__table_scene = table_scene
        self.__field_names = field_names
        self.__num_fields = len(field_names)

        super().__init__(
            screen, screen.height, screen.width,
            hover_focus=True, can_scroll=True, reduce_cpu=True
        )

        main_layout = Layout([100], fill_frame=True)
        self.add_layout(main_layout)
        for field_name in self.__field_names:
            main_layout.add_widget(Text(field_name, field_name))

        bottom_layout = Layout([1, 1, 1, 1])
        self.add_layout(bottom_layout)
        bottom_layout.add_widget(Button("OK", self._ok), 0)
        bottom_layout.add_widget(Button("Cancel", self._ok), 3)

        self.fix()
        self.set_theme('monochrome')

    # TODO: Change Table() inner representation from list of lists to list of
    #       dicts, so this is not needed anymore.
    def _field_dict_from_row(self, row):
        field_dict = {}
        for field_name, field in zip(self.__field_names, row):
            field_dict[field_name] = field
        return field_dict

    def reset(self):
        # Do low-level reset
        super().reset()
        # Fill out fields from currently selected row
        row = self.table.get_current_row()
        self.data = self._field_dict_from_row(row)

    def _ok(self):
        self.save()
        self.table.edit_current_row(list(self.data.values()))
        raise NextScene(self.__table_scene)

    @staticmethod
    def _cancel():
        raise NextScene(self.__table_scene)



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
