"""Defines the classes SymbolTable and SymbolTableNode"""

class SymbolTableNode:
    """Defines a class SymbolTableNode which stores the nodes in the SymbolTable"""

    def __init__(self, name, type_name):
        """Initializes the Node"""
        self.name = name
        self.type_name = type_name

class SymbolTable:
    """Defines a class for SymbolTable"""

    def __init__(self):
        """Initializes the SymbolTable"""
        self.symbol_table = {
            'global': {
                'name': 'global',
                'type': 'global',
                'parent': None,
                'identifiers': [],
                'functions': []
            }
        }
        self.current_scope = 'global'

    def start_scope(self, scope):
        """Starts a scope"""
        self.current_scope = scope

    def end_scope(self, scope):
        """Ends a scope"""
        self.current_scope = self.symbol_table[self.current_scope]['parent']

    def add_scope(self, scope_name):
        """Adds a new scope to the SymbolTable"""
        self.symbol_table[scope_name] = {
            'name': scope_name,
            'type': scope_name,
            'parent': self.current_scope,
            'identifiers': []
        }
        self.start_scope(scope_name)

    def add_identifier(self, TreeNode):
        newNode = SymbolTableNode(TreeNode.data, TreeNode.input_type)
        self.symbol_table[self.current_scope]['identifiers'] += [newNode]
        return True

    def search_identifier(self, name):
        return True

    # def print_symbol_table(self):
        # """Prints the symbol table"""
        # print 'SYMBOL TABLE'
        # for i in range(len(self.symbol_table)):
            # print self.symbol_table[i].name

    # def add_node(self, node):
        # """Adds a node to the SymbolTable"""
        # self.symbol_table.append(node)

    # def search_node(self,name):
        # """Searches for a node in the SymbolTable"""
        # for i in range(len(self.symbol_table)):
            # if self.symbol_table[i].name == name:
                # return 1
        # return 0

