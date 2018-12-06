from datetime import datetime

# import logging
# logging.basicConfig(filename='/tmp/debug.log',level=logging.DEBUG)

class Column():
    def __init__(self, value):
        self.set_value(value)

    def value(self):
        return self.__value

    def set_value(self, value):
        self.__value = value

    def type(self):
        return type(self.__value)

    def set_type(self, type_constructor):
        if not type_constructor == self.type():
            self.__value = type_constructor(self.__value)

    def am_compatible(self):
        if self.type() in (bool, datetime):
            return self.value()
        else:
            return str(self.value())

    def display(self):
        if self.type() == datetime:
            string = self.__value.date()
        else:
            string = self.__value
        return str(string)

    def width(self):
        return len(self.display())

    def __len__(self):
        return self.width()

    def __str__(self):
        return self.display()

    def __repr__(self):
        return 'Col({})'.format(self.value().__repr__())


class Row():
    def __init__(self, columns):
        self.set_columns(columns)

    def columns(self):
        return self.__columns

    def set_columns(self, columns):
        new_columns = []
        for column in columns:
            if not isinstance(column, Column):
                column = Column(column)
            new_columns.append(column)
        self.__columns = new_columns

    def values(self):
        return [col.value() for col in self.columns()]

    def am_compatible(self):
        return [col.am_compatible() for col in self.columns()]

    def display(self):
        return [col.display() for col in self.columns()]

    def widths(self):
        return [col.width() for col in self.columns()]

    def types(self):
        return [col.type() for col in self.columns()]

    def set_types(self, types):
        for col, t in zip(self.__columns, types):
            col.set_type(t)

    def __len__(self):
        return len(self.columns())

    def __repr__(self):
        return 'Row({})'.format(self.columns())

    def __getitem__(self, key):
        return self.__columns[key]

    def __setitem__(self, key, value):
        self.__columns[key] = value

    def __delitem__(self, key):
        del self.__columns[key]

    @classmethod
    def default_from_types(cls, types):
        columns = []
        for col_type in types:
            if col_type == datetime:
                column = datetime.now()
            else:
                column = col_type()
            columns.append(column)
        return cls(columns)
"""
Arguments:

Attributes:
    Public:
        self.current_row
    Private:
        self.__rows
        self.__num_cols
        self.__col_widths
        self.__col_names
        self.__col_types
"""
class Table():
    def __init__(self, rows, columns):
        self.__col_names = columns
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
            return Row.default_from_types(self.__col_types)
        else:
            return self.__rows[self.current_row]

    """
    Validates input and sets self.__rows, self.__num_cols,
    and self.__col_widths().

    Panics:
        Raises valueerror if each row in the list of rows given does not have
        the same length.
        Raises typeerror if each column does not have the same type in every
        row.
    """
    def set_rows(self, rows):
        first_row = rows[0]
        self.__num_cols = len(first_row)
        self.__col_types = first_row.types()
        for row in rows[1:]:
            self._assert_valid_row(row)
        self.__rows = rows
        self._init_column_widths()

    def _assert_valid_row(self, row):
        if len(row) != self.__num_cols:
            raise ValueError(
                'Each row in list of rows does not have the same length'
            )
        if row.types() != self.__col_types:
            raise TypeError(
                'Each column does not have the same type in every row'
            )

    def set_row(self, row, row_index):
        self._assert_valid_row(row)
        self.__rows[row_index] = row
        self._update_column_widths(row.widths())

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

    def del_current_row(self):
        self.del_row(self.current_row)

    """
    Add a row to table.

    Panics:
        This method raises ValueError if number of columns in given row
        does not equal self.__num_cols.
    """
    def add_row(self, row):
        self._assert_valid_row(row)
        self.__rows.append(row)
        self._update_column_widths(row.widths())

    # Column widths:
    # --------------------------------------------------------------------------
    """
    Get the widths of the table's columns. This equals the width of the
    largest cell in each column.
    """
    def _init_column_widths(self):
        rows = self.__rows
        widths = []
        for i in range(self.__num_cols):
            biggest_width = max([row[i].width() for row in rows])
            widths.append(biggest_width)

        self.__col_widths = widths
        # Maybe the column name is larger than every one of the values in the column:
        self._update_column_widths([len(name) for name in self.get_column_names()])

    def _update_column_widths(self, new_row_widths):
        self.__col_widths = [max(new, old) for new, old in zip(new_row_widths, self.__col_widths)]

    def get_column_widths(self, spacing=0):
        widths = self.__col_widths
        # Apply spacing to every column except for the last one
        return [w + spacing for w in widths[:-1]] + [widths[-1]]

    # Get other private attributes:
    # --------------------------------------------------------------------------
    def get_column_names(self):
        return self.__col_names

    def get_column_types(self):
        return self.__col_types

    def get_num_columns(self):
        return self.__num_cols
