class symboltable_node:
    """Defines a class Code which stores any piece of code line by line"""

    def __init__(self):
        """Initializes empty list named code"""
        self.name = ''
        self.type = ''

    # def add_line(self, line):
    #     """Appends a line to the code"""
    #     self.code.append(line)

    # def print_code(self):
    #     """Prints the code line by line"""
    #     for i in range(len(self.code)):
    #         print(self.code[i])

    # def length(self):
    #     """Returns length of code"""
    #     return len(self.code)

class SymbolTable:
    """Defines a class for p which stores the element for the Node"""

    def __init__(self):
        """Initializes class TreeNode"""

        self.symbol_table = []

    def print_symbol_table(self):
        """Prints the symbol table"""
        print '\nSYMBOL TABLE'
        for i in range(len(self.symbol_table)):
            print self.symbol_table[i].name

    def add_node(self, symboltable_node):
        self.symbol_table.append(symboltable_node)

    def search_node(self,name):
        for i in range(len(self.symbol_table)):
            if self.symbol_table[i].name == name:
                return 1
        return 0


