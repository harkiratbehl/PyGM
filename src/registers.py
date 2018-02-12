# Class for dealing with registers
# symbol table: used for address descriptors
# registers are numbered from 0 to 15

import operator

class registers:
    def __init__(self):
        # 8 + 8 registers in MIPS numbered from 8 - 15 and 16 - 23
        self.regs = ['$8', '$9', '$10', '$11', '$12', '$13', '$14', '$15', '$16', '$17', '$18', '$19', '$20', '$21', '$22', '$23']
        self.reg_dis = dict((el, 0) for el in self.regs)

    def print_regdis(self):
        print(self.reg_dis)

    def freereg(self):
        for reg in self.regs:
            # print(self.reg_dis[reg])
            if self.reg_dis[reg] == 0:
                return reg
        return 0

    def getreg(self, three_add_instr, symbol_table):
        if three_add_instr[3] in symbol_table.symbol_table:
            if symbol_table.symbol_table[three_add_instr[3]][1] != 0 and symbol_table.symbol_table[three_add_instr[3]][0][three_add_instr[0]-1] == symbol_table.symbol_table.max_line_number:
                return symbol_table.symbol_table[three_add_instr[3]][1]
        if three_add_instr[4] in symbol_table.symbol_table:
            if symbol_table.symbol_table[[three_add_instr[4]]][1] != 0 and symbol_table.symbol_table[three_add_instr[4]][0][three_add_instr[0]-1] == symbol_table.symbol_table.max_line_number:
                return symbol_table.symbol_table[three_add_instr[4]][1]
        if self.freereg() != 0:
            return self.freereg()
        else:
            # register spilling case
            sorted_x = sorted(self.reg_dis.items(), key=symbol_table.symbol_table[operator.itemgetter(1)][0][three_add_instr[0]-1], reverse=true)
            symbol_table.symbol_table[sorted_x[0][1]][1] = 0
            reg_dis[sorted_x[0][0]] = 0
            return sorted_x[0][0]

    def empty_all_registers(self, symbol_table):
        self.reg_dis = dict((el, 0) for el in self.regs)
        # also empty register name for variables stored in symbol_table.symbol_table
        for var in symbol_table.symbol_table.variables:
            symbol_table.symbol_table[var][1] = 0

