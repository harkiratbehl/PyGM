"""Defines classes Code and ThreeAddressCode"""

class Code:
    """Defines a class Code which stores any piece of code line by line"""

    def __init__(self):
        """Initializes empty list named code"""
        self.code = []

    def add_line(self, line):
        """Appends a line to the code"""
        self.code.append(line)

    def print_code(self):
        """Prints the code line by line"""
        for i in range(len(self.code)):
            print(self.code[i])

    def length(self):
        """Returns length of code"""
        return len(self.code)

class ThreeAddressCode(Code):
    """Extends the class code to store 3AC"""

    def __init__(self):
        """Initializes Code as well as empty list for storing leaders in 3AC"""
        Code.__init__(self)
        self.leaders = []

    def add_leader(self, leader):
        """Inserts a leader if not already present in the list"""
        if leader not in self.leaders:
            self.leaders.append(leader)
