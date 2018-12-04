import csv

class Data():
    'Takes a filename (without file extension) from the savedata folder as input'
    def __init__(self, path):
        self.path = path
    def load(self):
        try:
            with open("savedata/" + self.path + ".csv", "r") as data:
                pass
        except:
            return []
    def append(self, savedata):
        with open("savedata/" + self.path + ".csv", "a+"):
            pass
    def overwrite(self, savedata):
         with open("savedata/" + self.path + ".csv", "w"):
             pass