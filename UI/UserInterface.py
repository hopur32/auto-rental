from Business.Management import Management
import os
import ctypes

class UserInterface():
    def __init__(self):
        self.manage = Management()
        os.system('color 1f')
        ctypes.windll.kernel32.SetConsoleTitleW("Auto-Rental")
    def UI_loop(self):
        command = ""
        clear = lambda: os.system('cls')
        while command.lower() != 'q':
            clear()
            print("\t1 - Rent out a car")
            print("\t2 - Return a car")
            print("\tC - Customers")
            print("\tV - Vehicles")
            print("\tO - Orders")
            print("\tP - Price list")
            print("\tQ - Quit the program")
            command = input()