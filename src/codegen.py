#!/usr/bin/python

import sys
from sys import argv
from code import *
from registers import *
from symbol_table import *
from translator import *

# put into TAC
# write nextuse
# write getreg
# write translator

tac = three_address_code()
assembly_code = code()
symbol_table = symbol_table()
regs = registers()

def read_textfile(input_file): #generates tac and leaders and generate symbol table
    inp = open(input_file, 'r')
    for line in inp:
        line = line.rstrip('\n')
        three_add_instr = line.split(',')
        tac.nextline(three_add_instr)
        length = len(three_add_instr)
        if three_add_instr[1] == 'ifgoto': # might need change
            tac.leaders.append(len(tac.code)+1)
            tac.leaders.append(int(three_add_instr[length-1]))

        if three_add_instr[1] == 'goto' or three_add_instr[1] == 'break' or three_add_instr[1] == 'continue':
            tac.leaders.append(len(tac.code) + 1)
            tac.leaders.append(int(three_add_instr[2]))

    tac.leaders = sorted(tac.leaders, key=int)

    print(tac.code)

    symbol_table.fill_symbol_table(tac)
    symbol_table.print_symbol_table()

    # regs = registers()
    regs.print_regdis()

def assmcodegen(tac):
    # data region to handle global data and constants
    assembly_code.nextline('.data')
    for var in symbol_table.variables:
        line='%s:\t.space 150'%var
        assembly_code.nextline(line)
    assembly_code.nextline('.text')
    assembly_code.nextline('main:')

    for i in range(len(tac.code)):
        three_add_instr = tac.code[i]
        translator(three_add_instr, symbol_table, regs)

    # return(code)
    assembly_code.printcode()

if __name__ == '__main__':
    input_file = argv[1] # file conthree_add_instrning three address code
    print(input_file)

    read_textfile(input_file)
    assmcodegen(tac)

    # tac.printcode()
    # mipscode = codegen(tac)
