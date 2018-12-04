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
            return [''] * self.__num_cols
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
        self.__col_types = [type(col) for col in first_row]
        for row in rows[1:]:
            self._assert_valid_row(row)
        self.__rows = rows
        self._init_column_widths()

    def _assert_valid_row(self, row):
        if len(row) != self.__num_cols:
            raise ValueError(
                'Each row in list of rows does not have the same length'
            )
        row_col_types = [type(col) for col in row]
        if row_col_types != self.__col_types:
            raise TypeError(
                'Each column does not have the same type in every row'
            )

    def set_row(self, row, row_index):
        self._assert_valid_row(row)
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
        self._assert_valid_row(row)
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