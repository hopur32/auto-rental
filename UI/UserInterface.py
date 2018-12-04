import string
from collections import defaultdict

from asciimatics.event import KeyboardEvent
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import MultiColumnListBox, Text, Frame, Layout, Widget, TextBox, Button
from asciimatics.exceptions import ResizeScreenError, StopApplication, NextScene

"""
Attributes:
    Public:
        self.table
    Private:
        self.__spacing
        self.__header
        self.__list
        self.__edit_scene
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


"""
Arguments:
    screen (Screen): The screen that owns this frame.
    table (Table): The Table() class instance that contains the data to be edited.
    table_scene (str): The name of the scene to go to when exiting this frame.
    fields ([ITEM]): List of 
"""
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
        bottom_layout.add_widget(Button("Cancel", self._cancel), 3)

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
        self._cancel()

    def _cancel(self):
        raise NextScene(self.__table_scene)
