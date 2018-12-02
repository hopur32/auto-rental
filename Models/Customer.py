from datetime import datetime

class Customer():
    def __init__(self, name, email, phone, creditcard, expiration, age, signup = datetime.now()):
        self.name = name
        self.email = email
        self.phone = phone
        self.creditcard = creditcard
        self.expiration = expiration
        self.age = age
        self.signup = self.signup.date()