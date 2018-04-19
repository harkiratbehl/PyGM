"""Defines the classes SymbolTable and SymbolTableNode"""
import sys
from numpy import ones

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
                'allvars': [],
                'nextuse': dict()
            }
        }
        self.var_list = []
        self.next_use = dict()
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
            'allvars': [],
            'nextuse': dict()
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

    def make_var_list(self):
        for y in self.symbol_table.keys():
            for x in self.symbol_table[y]['allvars']:
                if x.name not in self.var_list:
                    self.var_list += [x.name]
        return self.var_list

    def fill_next_use(self,three_address_code):
        line_count = three_address_code.length()

        # Initializing symbol_table values for each variable
        for var in self.var_list:
            self.next_use[var] = [sys.maxsize * ones(line_count), 0]

        # traversing the three_address_code in reverse order
        for i in range(line_count):
            j = line_count - i - 1
            three_address_instr = three_address_code.code[j]
            var1 = three_address_instr[3]
            var2 = three_address_instr[4]

            for line_no in range(0, j):
                if var1 in self.var_list:
                    self.next_use[var1][0][line_no] = j + 1
                if var2 in self.var_list:
                    self.next_use[var2][0][line_no] = j + 1

    # def add_node(self, node):
        # """Adds a node to the SymbolTable"""
        # self.symbol_table.append(node)

    # def search_node(self,name):
        # """Searches for a node in the SymbolTable"""
        # for i in range(len(self.symbol_table)):
            # if self.symbol_table[i].name == name:
                # return 1
        # return 0

