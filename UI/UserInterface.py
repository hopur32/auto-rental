from Business.Management import Management

class UserInterface():
    def __init__(self):
        self.manage = Management()
    def UI_loop(self):
        command = ""
        while command.lower() != 'q':
            command = input()