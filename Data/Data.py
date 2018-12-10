from datetime import datetime
from pathlib import Path

from metadata import DATA_DIR

import logging
#logging.basicConfig(filename='/tmp/debug.log', level=logging.DEBUG)

class Column():
    def __init__(self, value):
        self.set_value(value)

    def value(self):
        return self.__value

    def set_value(self, value):
        self.__value = value

    def type(self):
        return type(self.__value)

    def type_name(self):
        return type(self.__value).__name__

    def constructable(self):
        if self.type() == datetime:
            d = self.__value
            return ','.join([str(i) for i in [d.year, d.month, d.day,
                              d.hour, d.minute, d.second, d.microsecond]])
        else:
            return str(self.__value)

    def set_type(self, type_constructor):
        logging.info('Setting type: self.__value = {}, type_constructor = {}'.format(
            self.__value, type_constructor))
        if type_constructor != self.type():
            if type_constructor == datetime:
                self.__value = datetime(*[int(i) for i in self.__value.split(',')])
            else:
                logging.debug('Not datetime')
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

    def constructable(self):
        return [col.constructable() for col in self.columns()]

    def types(self):
        return [col.type() for col in self.columns()]

    def type_names(self):
        return [col.type_name() for col in self.columns()]

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
    Private:
        self.__file_path
        self.__rows
        self.__num_cols
        self.__col_names
        self.__col_types
"""
class Data():
    def __init__(self, filename, column_names, types, file_directory=DATA_DIR, delimiter='|'):
        self.__file_path = Path(file_directory + '/' + filename)
        # Maybe change to list of tuples instead of two seperate lists, so
        # this check doesn't have to be done.
        self.__col_names = column_names
        self.__col_types = types
        if not len(self.__col_names) == len(self.__col_types):
            raise ValueError('Column names and column types do not have the same number of elements.')
        self.__num_cols = len(types)
        self.__delim = delimiter
        self.update_cache()

    """
    Updates file with contents of self.__file_path. If file does not exist,
    make self.__rows an empty list.
    """
    def update_cache(self):
        try:
            with open(self.__file_path, "r", encoding="utf-8") as f:
                type_names = f.readline().strip().split(self.__delim)
                col_names = f.readline().strip().split(self.__delim)
                if col_names != self.__col_names:
                    raise ValueError('File has invalid column names')
                elif type_names != [t.__name__ for t in self.__col_types]:
                    raise ValueError('File has invalid column types')

                logging.debug('{}'.format(type_names))
                logging.debug(col_names)

                rows = []
                for line in f.readlines():
                    row = Row(line.split(self.__delim))
                    row.set_types(self.__col_types)
                    rows.append(row)
                self.set_rows(rows)
        except FileNotFoundError:
            self.__rows = []

    def update_file(self):
        with open(self.__file_path, "w+", encoding='utf-8') as f:
            lines = []
            lines.append(self.__delim.join([t.__name__ for t in self.__col_types]) + '\n')
            lines.append(self.__delim.join(self.__col_names) + '\n')
            for row in self.get_rows():
                lines.append(self.__delim.join(row.constructable()) + '\n')

            # Write the lines to file
            f.writelines(lines)

    def _append_row_to_file(self, row):
        with open(self.__file_path, 'a', encoding='utf-8') as f:
            line = self.__delim.join(row.constructable())
            f.write(line + '\n')

    # Row management:
    # --------------------------------------------------------------------------
    """
    Return private attribute self.__rows.
    """
    def get_rows(self):
        return self.__rows

    def get_row(self, row_index):
        return self.__rows[row_index]

    """
    Validates input and overwrites self.__rows, self.__num_cols.

    Panics:
        Raises valueerror if each row in the list of rows given does not have
        the same length.
        Raises typeerror if each column does not have the same type in every
        row.
    """
    def set_rows(self, rows):
        rows = [Row(row) if not isinstance(row, Row) else row for row in rows]

        first_row = rows[0]
        self.__num_cols = len(first_row)
        self.__col_types = first_row.types()

        for row in rows[1:]:
            self._assert_valid_row(row)
        self.__rows = rows

    """
    Validates input and overwrites the row at index `row_index`` in self.__rows.
    """
    def set_row(self, row, row_index):
        if not isinstance(row, Row):
            row = Row(row)
        self._assert_valid_row(row)
        self.__rows[row_index] = row
        self.update_file()

    """
    Raises valueerror if each row in the list of rows given does not have
    the same length.
    Raises typeerror if each column does not have the same type in every
    row.
    """
    def _assert_valid_row(self, row):
        if len(row) != self.__num_cols:
            raise ValueError(
                'Each row in list of rows does not have the same length'
            )
        if row.types() != self.__col_types:
            raise TypeError(
                'Each column does not have the same type in every row'
            )

    """
    Delete the row at row_index. Does nothing if row_index == None.
    """
    def del_row(self, row_index):
        del self.__rows[row_index]
        self.update_file()

    """
    Add a row to table.

    Panics:
        This method raises ValueError if number of columns in given row
        does not equal self.__num_cols.
    """
    def add_row(self, row):
        if not isinstance(row, Row):
            row = Row(row)
        self._assert_valid_row(row)
        self.__rows.append(row)
        # self._append_row_to_file(row)
        self.update_file()

    # Get other private attributes:
    # --------------------------------------------------------------------------
    def get_column_names(self):
        return self.__col_names

    def get_column_types(self):
        return self.__col_types

    def get_num_columns(self):
        return self.__num_cols

DELIM = '|'
