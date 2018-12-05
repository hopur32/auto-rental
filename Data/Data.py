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
            return types, header, rows
        except:
            return [], [], [[]]
    def append(self, savedata):
        with open("savedata/" + self.path + ".csv", "a+") as csvfile:
            pass
    def overwrite(self, savedata):
        with open("savedata/" + self.path + ".csv", "w") as csvfile:
            pass
    def __str__(self):
        s = " ".join(self.__types)
        s += "\n" + " ".join(self.__col_names)
        for i in self.rows:
            s += "\n"
            s += " ".join(i)
        return s

d = Data("Vehicles")
print(d)