import string
from collections import defaultdict

from asciimatics.event import KeyboardEvent
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import MultiColumnListBox, Text, Frame, Layout, Widget, TextBox
from asciimatics.exceptions import ResizeScreenError, StopApplication

"""
Attributes:
    Public:
    Private:
        self.__spacing
        self.__rows
        self.__num_cols
        self.__col_widths
        self.__col_names

        self.__header
        self.__list
        self.__last_frame
"""
class TableFrame(Frame):
    def __init__(self, screen, rows, col_names=None, header_text='TableFrame', spacing=1, has_border=False):
        if col_names == None:
            self.__col_names = [str(i+1) for i in range(len(rows[0]))]
        else:
            self.__col_names = col_names
        self.set_rows(rows)
        self.__spacing = spacing

        # Asciimatics stuff:
        # ----------------------------------------------------------------------
        super().__init__(
            screen, screen.height, screen.width, has_border=has_border, name=header_text
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
            self.get_column_widths(spacing=self.__spacing),
            [],
            titles=self.__col_names,
            name='Table'
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
            if event.key_code in [ord('q'), ord('Q'), Screen.ctrl("c")]:
                raise StopApplication("User quit")

            # Force a refresh for improved responsiveness
            self.__last_frame = 0

        # Now pass on to lower levels for normal handling of the event.
        return super().process_event(event)

    def _update(self, frame_num):
        if frame_num - self.__last_frame >= self.frame_update_count or self.__last_frame == 0:
            self.__last_frame = frame_num

            prev_value = self.__list.value
            prev_start_line = self.__list.start_line

            list_data = [(row, i+1) for i, row in enumerate(self.get_rows())]
            column_widths = self.get_column_widths(spacing=self.__spacing)

            self.__list.options = list_data
            self.__list.value = prev_value
            self.__list.start_line = prev_start_line
            # Here we are editing a private attribute, and must thus be careful.
            # This is not an intended usecase by the module authors.
            self.__list._columns = column_widths

        super()._update(frame_num)

    @property
    def frame_update_count(self):
        return 40

    # Row management:
    # --------------------------------------------------------------------------
    """
    Return private attribute self.__rows.
    """
    def get_rows(self):
        return self.__rows

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
        self.__col_widths = self._init_column_widths()

        # Force a refresh for improved responsiveness
        self.__last_frame = 0

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
        self.__num_cols += 1

        # Update self.__col_widths.
        new_row_lengths = [len(col) for col in row]
        self.__col_widths = [max(new, old) for new, old in zip(new_row_lengths, self.__col_widths)]

        # Force a refresh for improved responsiveness
        self.__last_frame = 0

    # Column widths:
    # --------------------------------------------------------------------------
    """
    Get the widths of the table's columns. This equals the width of the
    largest cell in each column.
    """
    def _init_column_widths(self):
        widths = []
        rows = self.__rows[:]
        if self.__col_names:
            rows.append(self.__col_names)
        for i in range(self.__num_cols):
            widths_in_col_i = [len(row[i]) for row in rows]
            biggest_width_in_col_i = max(widths_in_col_i)
            widths.append(biggest_width_in_col_i)
        return widths

    def get_column_widths(self, spacing=None):
        if spacing:
            return [col_width + spacing for col_width in self.__col_widths]
        else:
            return self.__col_widths

rows = [[str(i)+'dstndtns', str(i+1)+'12312312', str(i+2)+'tsdndtns']
        for i in range(0, 100, 3)]

def demo(screen):
    screen.play([Scene([TableFrame(screen, rows, col_names=['one', 'two', 'three', 'four', 'five'])], -1)], stop_on_resize=True)

while True:
    try:
        Screen.wrapper(demo, catch_interrupt=True)
        exit()
    except ResizeScreenError:
        pass
