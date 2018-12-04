from datetime import datetime

class Vehicle():
    def __init__(self, plate, manufacturer, model, year, category):
        self.plate = plate
        self.manufacturer = manufacturer
        self.model = model
        self.year = year
        self.category = category
        self.rental = {}
    def rented(self, date = datetime.now()):
        for i in self.rental.keys():
            if i <= date < self.rental[i]:
                return True
        return False