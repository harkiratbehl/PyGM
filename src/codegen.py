#!/usr/bin/python

import sys
from sys import argv
from code import *
from registers import *
from symbol_table import *
# from translator import *

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
        if three_add_instr[1] == 'ifgotoeq' or three_add_instr[1] == 'ifgotoneq' or three_add_instr[1] == 'ifgotolt' or three_add_instr[1] == 'ifgotogt' or three_add_instr[1] == 'ifgotolteq' or three_add_instr[1] == 'ifgotolteq':
            # might need change
            tac.leaders.append(len(tac.code))
            tac.leaders.append(int(three_add_instr[4])-1)

        if three_add_instr[1] == 'goto' or three_add_instr[1] == 'break' or three_add_instr[1] == 'continue':
            tac.leaders.append(len(tac.code))
            tac.leaders.append(int(three_add_instr[2])-1)

        # if three_add_instr[1] == 'for':
        #     tac.leaders.append(len(tac.code)+1)

    tac.leaders = sorted(tac.leaders, key=int)
    # print(tac.code)
    symbol_table.fill_symbol_table(tac)

def assmcodegen(tac):
    # data region to handle global data and constants
    assembly_code.nextline('\t.data')
    for var in symbol_table.variables:
        line='%s:\t.word 0'%var
        assembly_code.nextline(line)
    assembly_code.nextline('\t.text')
    assembly_code.nextline('main:')

    for i in range(len(tac.code)):
        if i in tac.leaders:
            assembly_code.nextline('Line_' + str(i + 1) + ':')
        three_add_instr = tac.code[i]
        translator(three_add_instr, symbol_table, regs)

    assembly_code.nextline('li $v0, 10')
    assembly_code.nextline('syscall')

    # return(code)
    assembly_code.printcode()

def translator(three_address_instr, symbol_table, regs):

    # parse three_address_instr
    lineno = int(three_address_instr[0])
    op = three_address_instr[1]
    dest = three_address_instr[2]
    src1 = three_address_instr[3]
    src2 = three_address_instr[4]

    if op == '+':
        reg1 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src2, symbol_table, lineno, assembly_code)
        reg3 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('add ' + reg3 + ', ' + reg1 + ', ' + reg2)

    if op =='-':
        reg1 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src2, symbol_table, lineno, assembly_code)
        reg3 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('sub ' + reg3 + ', ' + reg1 + ', ' + reg2)

    if op == '*':
        reg1 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src2, symbol_table, lineno, assembly_code)
        reg3 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('mult ' + reg1 + ', ' + reg2)
        assembly_code.nextline('mflo ' + reg3)#LO 32

    if op =='/':
        reg1 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src2, symbol_table, lineno, assembly_code)
        reg3 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('div ' + reg1 + ', ' + reg2)
        assembly_code.nextline('mflo ' + reg3)#LO

    if op =='%':
        reg1 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src2, symbol_table, lineno, assembly_code)
        reg3 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('div ' + reg1 + ', ' + reg2)
        assembly_code.nextline('mfhi ' + reg3)#HI

    if op == 'print_int':
        reg1 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('li $v0, 1')
        assembly_code.nextline('move $a0, ' + reg1)
        assembly_code.nextline('syscall')

    if op == 'scan_int':
        reg1 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('li $v0, 5')
        assembly_code.nextline('syscall')
        assembly_code.nextline('move ' + reg1 + ', $v0')
        

################ UNARY OPERATORS
    if op == '=':
        #in case of this also it will take a register for the destination variable and it will be initialized to its value in the data declaration
        reg1 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('li ' + reg1 + ', ' + src1)

    if op == '+=':
        #in case of this also it will take a register for the destination variable and it will be initialized to its value in the data declaration
        reg1 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('add ' + reg2 + ', ' + reg2 + ', ' + reg1)

    if op == '-=':
        #in case of this also it will take a register for the destination variable and it will be initialized to its value in the data declaration
        reg1 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('sub ' + reg2 + ', ' + reg2 + ', ' + reg1)


    if op == '*=':
        #in case of this also it will take a register for the destination variable and it will be initialized to its value in the data declaration
        reg1 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        aassembly_code.nextline('mult ' + reg2 + ', ' + reg1)
        assembly_code.nextline('mflo ' + reg2)


    if op == '/=':
        #in case of this also it will take a register for the destination variable and it will be initialized to its value in the data declaration
        reg1 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('add ' + reg2 + ', ' + reg2 + ', ' + reg1)





    if op == 'ifgotoeq':
        reg1 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        target = 'Line_' + str(src2)
        assembly_code.nextline('beq ' + reg1 + ', ' + reg2 + ', ' + target)

    if op == 'ifgotoneq':
        reg1 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        target = 'Line_' + str(src2)
        assembly_code.nextline('bne ' + reg1 + ', ' + reg2 + ', ' + target)

    if op == 'ifgotolt':
        reg1 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        target = 'Line_' + str(src2)
        assembly_code.nextline('blt ' + reg1 + ', ' + reg2 + ', ' + target)

    if op == 'ifgotolteq':
        reg1 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        target = 'Line_' + str(src2)
        assembly_code.nextline('ble ' + reg1 + ', ' + reg2 + ', ' + target)

    if op == 'ifgotogt':
        reg1 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        target = 'Line_' + str(src2)
        assembly_code.nextline('bgt ' + reg1 + ', ' + reg2 + ', ' + target)

    if op == 'ifgotogteq':
        reg1 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        target = 'Line_' + str(src2)
        assembly_code.nextline('bge ' + reg1 + ', ' + reg2 + ', ' + target)

    if op == 'goto':
        target = 'Line_' + str(dest)
        assembly_code.nextline('j ' + target)


####################.  LOOPS

    if op == 'break':
        target = 'Line_' + str(dest)
        assembly_code.nextline('j ' + target)

    if op == 'continue':
        target = 'Line_' + str(dest)
        assembly_code.nextline('j ' + target)

    # if op == 'for':
    #this is the format of tac for for loop
        # L: if (i>=9) goto END_FOR
        # i=i+1
        # goto L:
        # END_FOR:


if __name__ == '__main__':
    input_file = argv[1] # file conthree_add_instrning three address code

    read_textfile(input_file)
    assmcodegen(tac)

    # tac.printcode()
    # mipscode = codegen(tac)

