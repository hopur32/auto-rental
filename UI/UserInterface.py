import string
from collections import defaultdict
from datetime import datetime

from asciimatics.event import KeyboardEvent
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import MultiColumnListBox, Text, Frame, Layout, Widget, TextBox, Button, PopUpDialog, DatePicker, CheckBox
from asciimatics.exceptions import ResizeScreenError, StopApplication, NextScene, InvalidFields

from Data.Data import Row


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
    def __init__(self, screen, table, edit_scene,
                 header_text='TableFrame', spacing=2, has_border=True, reverse_sort=False, sort_index=0):
        self.table = table
        self.__screen = screen
        self.__edit_scene = edit_scene
        self.__spacing = spacing
        self.__reverse_sort = reverse_sort
        self.__sort_index = sort_index
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
            self.table.get_column_widths(self.__spacing),
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
            elif event.key_code in [ord("r"), ord("R")]:
                self.__reverse_sort = not self.__reverse_sort
                self._reload_list()
            elif event.key_code == ord("<"):
                self.__sort_index = max(0, self.__sort_index - 1)
                self._reload_list()
            elif event.key_code == ord(">"):
                self.__sort_index = min(self.table.get_num_columns() - 1, self.__sort_index + 1)
                self._reload_list()

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
        def act_on_selection(selection):
            if selection == 0:  # Yes is selected
                self.save()
                self.table.current_row = self.data['row_index']
                # Save the current row number before we delete
                current_row = self.table.current_row
                self.table.del_current_row()
                self._reload_list()
                # Put focus to the row at the index we deleted
                num_rows = len(self.table.get_rows())
                if num_rows != 0:
                    self.__list.value = min(num_rows - 1, current_row)
                else:
                    self.__list.value = None
        popup = PopUpDialog(
            self.__screen,
            "Hey dumbass. Are you sure you want to proceed?",
            ["Yes", "No"],
            has_shadow=True,
            on_close=act_on_selection
        )
        popup.set_theme('monochrome')
        self._scene.add_effect(popup)

    def _sort_list(self):
        self.__list.options = sorted(self.__list.options, key=lambda x: x[0][self.__sort_index],
                                     reverse=self.__reverse_sort)
    def _get_sort_arrow(self):
        if self.__reverse_sort:
            return '▲ '
        else:
            return '▼ '

    def _reload_list(self):
        column_widths = self.table.get_column_widths(self.__spacing)[:]
        column_widths[self.__sort_index] += len(self._get_sort_arrow())
        column_names = self.table.get_column_names()[:]
        column_names[self.__sort_index] = self._get_sort_arrow() + column_names[self.__sort_index]

        list_data = [(row.display(), i)
                     for i, row in enumerate(self.table.get_rows())]

        self.__list.options = list_data
        self._sort_list()
        # Here we are editing private attributes, and must thus be careful.
        # This is not an intended usecase by the module authors.
        self.__list._columns = column_widths
        self.__list._titles = column_names


"""
Arguments:
    screen (Screen): The screen that owns this frame.
    table (Table): The Table() class instance that contains the data to be edited.
    table_scene (str): The name of the scene to go to when exiting this frame.
"""


class EditFrame(Frame):
    def __init__(self, screen, table, table_scene):
        self.table = table
        self.__screen = screen
        self.__table_scene = table_scene

        super().__init__(
            screen, screen.height, screen.width,
            hover_focus=True, can_scroll=True, reduce_cpu=True
        )

        main_layout = Layout([100], fill_frame=True)
        self.add_layout(main_layout)
        for field_type, field_name in zip(
                self.table.get_column_types(), self.table.get_column_names()):
            if field_type == datetime:
                widget = DatePicker(label=field_name, name=field_name)
            elif field_type == bool:
                widget = CheckBox('', label=field_name, name=field_name)
            elif field_type == int:
                widget = Text(
                    label=field_name,
                    name=field_name,
                    validator='^[0-9]*$')
            elif field_type == float:
                widget = Text(
                    label=field_name,
                    name=field_name,
                    validator=r'^[0-9]*\.?[0-9]+$')
            else:
                widget = Text(label=field_name, name=field_name)
            main_layout.add_widget(widget)

        bottom_layout = Layout([1, 1, 1])
        self.add_layout(bottom_layout)
        bottom_layout.add_widget(Button("OK", self._ok), 0)
        bottom_layout.add_widget(Button("Reset", self.reset), 1)
        bottom_layout.add_widget(Button("Cancel", self._cancel), 2)

        self.fix()
        self.set_theme('monochrome')

    # TODO: Change Table() inner representation from list of lists to list of
    #       dicts, so this is not needed anymore.
    def _field_dict_from_row(self, row):
        field_dict = {}
        for field_name, field in zip(
                self.table.get_column_names(), row.am_compatible()):
            field_dict[field_name] = field
        return field_dict

    def reset(self):
        # Do low-level reset
        super().reset()
        # Fill out fields from currently selected row
        row = self.table.get_current_row()
        self.data = self._field_dict_from_row(row)

    def _ok(self):
        try:
            self.save(validate=True)
            row = Row(self.data.values())
            row.set_types(self.table.get_column_types())
            self.table.edit_current_row(row)
            self._cancel()
        except InvalidFields:
            popup = PopUpDialog(
                self.__screen,
                'Error: An invalid value vas entered into form',
                ['OK'],
                has_shadow=True
            )
            popup.set_theme('monochrome')
            self._scene.add_effect(popup)

    def _cancel(self):
        raise NextScene(self.__table_scene)
