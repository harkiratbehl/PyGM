"""Defines the classes SymbolTable and SymbolTableNode"""

class SymbolTableNode:
    """Defines a class SymbolTableNode which stores the nodes in the SymbolTable"""

    def __init__(self, name, type_name):
        """Initializes the Node"""
        self.name = name
        self.type_name = type_name

    def print_node(self):
        print self.name, self.type_name

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
                'functions': [],
                'allvars': []
            }
        }
        self.current_scope = 'global'

    def start_scope(self, scope):
        """Starts a scope"""
        self.current_scope = scope

    def end_scope(self):
        """Ends a scope"""
        self.current_scope = self.symbol_table[self.current_scope]['parent']

    def add_scope(self, scope_name):
        """Adds a new scope to the SymbolTable"""
        self.symbol_table[scope_name] = {
            'name': scope_name,
            'type': scope_name,
            'parent': self.current_scope,
            'identifiers': [],
            'functions': [],
            'allvars': []
        }
        self.start_scope(scope_name)

    def add_identifier(self, TreeNode):
        for node in self.symbol_table[self.current_scope]['identifiers']:
            if TreeNode.data == node.name:
                return True
        newNode = SymbolTableNode(TreeNode.data, TreeNode.input_type)
        self.symbol_table[self.current_scope]['identifiers'] += [newNode]
        return True

    def add_var(self, TreeNode):
        for node in self.symbol_table[self.current_scope]['allvars']:
            if TreeNode.name == node.name:
                return True
        # newNode = SymbolTableNode(TreeNode.name, TreeNode.type_name)
        self.symbol_table[self.current_scope]['allvars'] += [TreeNode]
        return True

    def search_identifier(self, name):
        scope = self.current_scope
        while scope != None:
            for node in self.symbol_table[scope]['identifiers']:
                if name == node.name:
                    return scope + '_' + name
            scope = self.symbol_table[scope]['parent']
        return False

    def print_symbol_table(self):
        """Prints the symbol table"""
        print ''
        print 'SYMBOL TABLE'
        for y in self.symbol_table.keys():
            print "scope", y, self.symbol_table[y]['parent']
            for x in self.symbol_table[y]['identifiers']:
                x.print_node()
            for x in self.symbol_table[y]['allvars']:
                x.print_node()

    # def add_node(self, node):
        # """Adds a node to the SymbolTable"""
        # self.symbol_table.append(node)

    # def search_node(self,name):
        # """Searches for a node in the SymbolTable"""
        # for i in range(len(self.symbol_table)):
            # if self.symbol_table[i].name == name:
                # return 1
        # return 0

