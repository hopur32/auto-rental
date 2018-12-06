from datetime import datetime

DELIM = '|'

class Data():
    'Takes a filename (without file extension) from the savedata folder as input'
    def __init__(self, path):
        self.path = path
        self.__types, self.__col_names, self.rows = self.load()
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
    def append(self, savedata):
        with open("savedata/" + self.path + ".txt", "a+", encoding = "utf-8") as data:
            to_save = [str(i) for i in savedata]
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
            data.write('\n' + DELIM.join(header))
            for i in savedata:
                data.write('\n')
                for j in range(len(i)):
                    if j != 0:
                        data.write(DELIM)
                    if type(i[j]) == datetime:
                        data.write(str(i[j].date()))
                    else:
                        data.write(str(i[j]))
    def get_header(self):
        return self.__col_names
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
    def __str__(self):
        s = " ".join(self.__types)
        s += "\n" + " ".join(self.__col_names)
        for row in self.rows:
            s += "\n"
            s += DELIM.join([str(col) for col in row])
        return s

d = Data("Vehicles")
print(d)
d.overwrite(d.get_header(), d.rows)