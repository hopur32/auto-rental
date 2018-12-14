from datetime import datetime

from data.Data import Row, Data

"""
Arguments:

Attributes:
    Public:
        self.current_row
        self.runtime_columns
    Private:
        self.__col_widths
"""


class Table(Data):
    def __init__(self, *args, runtime_columns=[], **kwargs):
        self.current_row = None
        self.runtime_columns = runtime_columns
        super().__init__(*args, **kwargs)
        self._init_column_widths()

    # Overload methods of parent class to update column widths:
    # -------------------------------------------------------------------------
    def set_rows(self, rows):
        super().set_rows(rows)
        self._init_column_widths()

    def set_row(self, row, row_index):
        super().set_row(row, row_index)
        self._init_column_widths()

    def del_row(self, row_index):
        if row_index is not None:
            super().del_row(row_index)
            self._init_column_widths()

    def add_row(self, row):
        super().add_row(row)
        added_row = super().get_row(-1)
        self._update_column_widths(added_row.widths())

    # Methods on current row:
    # --------------------------------------------------------------------------
    def get_current_row(self):
        if self.current_row is None:
            return Row.default_from_types(super().get_column_types())
        else:
            return super().get_row(self.current_row)

    def edit_current_row(self, row):
        if self.current_row is None:
            self.add_row(row)
        else:
            self.set_row(row, self.current_row)

    def del_current_row(self):
        self.del_row(self.current_row)

    # Column widths:
    # --------------------------------------------------------------------------
    """
    Get the widths of the table's columns. This equals the width of the
    largest cell in each column.
    """

    def _init_column_widths(self):
        rows = super().get_rows()
        if len(rows) > 0:
            widths = []
            for i in range(super().get_num_columns()):
                biggest_width = max([row[i].width() for row in rows])
                widths.append(biggest_width)

            self.__col_widths = widths
        # Maybe the column name is larger than every one of the values in the
        # column:
        self._update_column_widths([len(name) for name in super().get_column_names()])

    def _update_column_widths(self, new_row_widths):
        try:
            self.__col_widths = [max(new, old) for new, old in zip(
                new_row_widths, self.__col_widths)]
        except AttributeError:
            # This is the first time we're setting the attribute
            self.__col_widths = new_row_widths

    def get_column_widths(self, spacing=0):
        widths = self.__col_widths
        if len(widths) > 0:
            # Apply spacing to every column except for the last one
            return [w + spacing for w in widths]
        else:
            return []
