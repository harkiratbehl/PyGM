import sys
from collections import OrderedDict
import numpy as np
from lexer import *

class symbol_table:
    def __init__(self):
        self.symbol_table = dict() # OrderedDict()
        self.next_use = []
        self.variables = []
        self.max_line_no = 1000000

    def print_symbol_table(self):
        print(self.symbol_table)

    def get_variables(self, three_address_code):
        # use lexer to get identifiers from three_address_code
        # hardcoded for testing
        code=''
        # print(three_address_code.code)
        for l in three_address_code.code:
            l = ",".join(l)
            code=code+l+'\n'
        lexr=lexer_pygm(code)
        lexr.lext()
        self.variables = lexr.identifiers

    def fill_symbol_table(self, three_address_code):
        self.get_variables(three_address_code)
        line_count = len(three_address_code.code)

        # constructing fields for each variable
        # second element is the name of the regiser for the variable
        for var in self.variables:
            self.symbol_table[var] = [self.max_line_no * np.ones(line_count), 0]

        # going back from last line of block
        for i in range(line_count):
            j = line_count - i - 1
            three_address_instr = three_address_code.code[j]
            if three_address_instr[3] in self.symbol_table:
                for r in range(0, j):
                    self.symbol_table[three_address_instr[3]][0][r] = j+1
            if three_address_instr[4] in self.symbol_table:
                for r in range(0, j):
                    self.symbol_table[three_address_instr[4]][0][r] = j+1

