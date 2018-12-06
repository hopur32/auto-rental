from datetime import datetime

DELIM = '|'

class Data():
    'Takes a filename (without file extension) from the savedata folder as input'
    def __init__(self, path):
        self.path = path
        self.__types, self.__col_names, self.__rows = self.load()
    def load(self):
        try:
            with open("savedata/" + self.path + ".txt", "r", encoding = "utf-8") as data:
                types = data.readline().strip().split(DELIM)
                header = data.readline().strip().split(DELIM)
                rows = data.readlines()
                for i in range(len(rows)):
                    rows[i] = rows[i].strip().split(DELIM)
                rows = self.typify(types, rows)
            return types, header, rows
        except:
            return [], [], [[]]
    def append(self, newdata):
        with open("savedata/" + self.path + ".txt", "a", encoding = "utf-8") as data:
            to_save = []
            self.__rows.append(newdata)
            for value in newdata:
                if type(value) == datetime:
                    to_save.append(str(value.date()))
                else:
                    to_save.append(str(value))
            data.write(DELIM.join(to_save) + "\n")
    def overwrite(self, header, savedata):
        with open("savedata/" + self.path + ".txt", "w", encoding = 'utf-8') as data:
            for i in range(len(savedata[0])):
                if i != 0:
                    data.write(DELIM)
                if type(savedata[0][i]) == datetime:
                    data.write('date')
                elif type(savedata[0][i]) == str:
                    data.write('str')
                elif type(savedata[0][i]) == int:
                    data.write('int')
            data.write('\n' + DELIM.join(header) + '\n')
            for i in savedata:
                for j in range(len(i)):
                    if j != 0:
                        data.write(DELIM)
                    if type(i[j]) == datetime:
                        data.write(str(i[j].date()))
                    else:
                        data.write(str(i[j]))
                data.write('\n')
    def typify(self, types, values):
        "Convert a list of lists of values into the correct types"
        for i in range(len(values)):
            for j in range(len(types)):
                if types[j] == "int":
                    values[i][j] = int(values[i][j])
                elif types[j] == "str":
                    pass
                elif types[j] == "date":
                    year, month, day = [int(k) for k in values[i][j].split('-')]
                    values[i][j] = datetime(year, month, day)
        return values
    def get_col_names(self):
        return self.__col_names
    def get_rows(self):
        return self.__rows
    def remove_row(self, index):
        self.__rows.pop(index)
        self.overwrite(self.__col_names, self.__rows)