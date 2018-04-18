"""Defines the class SymbolTable"""

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
    """Defines a class for SymbolTable"""

    def __init__(self):
        """Initializes the SymbolTable"""
        self.symbol_table = []
        # self.symbol_table = {
            # 'global': {
                # 'name': 'global',
                # 'type': 'global',
                # 'parent': None,
                # 'identifiers': {}
            # }
        # }
        self.current_scope = 'global'

    def start_scope(self, scope):
        """Starts a scope"""
        self.current_scope = scope

    def end_scope(self, scope):
        """Ends a scope"""
        self.current_scope = self.symbol_table[self.current_scope]['parent']

    def add_scope(self, scope_name, scope_type):
        """Adds a new scope to the SymbolTable"""
        self.symbol_table[scope_name] = {
            'name': scope_name,
            'type': scope_type,
            'parent': self.current_scope,
            'identifiers': {}
        }
        self.start_scope(scope_name)

    def print_symbol_table(self):
        """Prints the symbol table"""
        print 'SYMBOL TABLE'
        for i in range(len(self.symbol_table)):
            print self.symbol_table[i].name

    def add_node(self, node):
        """Adds a node to the SymbolTable"""
        self.symbol_table.append(node)

    def search_node(self,name):
        """Searches for a node in the SymbolTable"""
        for i in range(len(self.symbol_table)):
            if self.symbol_table[i].name == name:
                return 1
        return 0

