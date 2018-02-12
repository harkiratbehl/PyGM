# Defines a class for three object code. Initially the three address code is empty.
# As the text file is read, tai (three address instructions) are added into it.

class code:
    def __init__(self):
        self.code = []

    def nextline(self, line):
        self.code.append(line)

    def printcode(self):
        for i in range(len(self.code)):
            print(self.code[i])

class three_address_code(code):
    def __init__(self):
        self.leaders = [0]
        self.code = []

