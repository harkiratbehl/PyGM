"""Defines the class SymbolTable"""

import sys
from numpy import ones
from lexer import Lexer

class SymbolTable:
    """Defines the Symbol Table"""

    def __init__(self):
        """Initializes member variables"""

        self.symbol_table = dict() # OrderedDict()

        self.next_use = []
        self.variables = []
        self.max_line_no = sys.maxsize

    def print_symbol_table(self):
        """Prints the symbol table"""
        print(self.symbol_table)

    def set_variables(self, three_address_code):
        """Gets identifiers from lexer and sets them as variables
        Hardcoded since we don't have the parser"""

        input_code = ''
        for line in three_address_code:
            input_code += ','.join(line) + '\n'

        lexer_obj = Lexer()
        lexer_obj.set_code(input_code)

        lexer_obj.lex_code()
        self.variables = lexer_obj.lexemes['IDENTIFIER']

    def fill_symbol_table(self, three_address_code):
        """Populates the symbol table"""
        self.set_variables(three_address_code.code)
        line_count = three_address_code.length()

        # Initializing symbol_table values for each variable
        for var in self.variables:
            self.symbol_table[var] = [self.max_line_no * ones(line_count), 0]

        # traversing the three_address_code in reverse order
        for i in range(line_count):
            j = line_count - i - 1
            three_address_instr = three_address_code.code[j]

            var1 = three_address_instr[3]
            var2 = three_address_instr[4]

            for line_no in range(0, j):
                if var1 in self.symbol_table:
                    self.symbol_table[var1][0][line_no] = j + 1
                if var2 in self.symbol_table:
                    self.symbol_table[var2][0][line_no] = j + 1
