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

end_main = 0

def read_textfile(input_file): #generates tac and leaders and generate symbol table
    inp = open(input_file, 'r')
    for line in inp:
        line = line.rstrip('\n')
        three_add_instr = line.split(',')
        tac.nextline(three_add_instr)
        length = len(three_add_instr)

        if len(three_add_instr) != 5:
            print("Incorrect size for the following instruction: ")
            print(three_add_instr)
            return 1

        if three_add_instr[0] == '':
            print("Line number not given in the following instruction: ")
            print(three_add_instr)
            return 1

        import re
        if re.search(r'\D', three_add_instr[0]) != None:
            print("Invalid line number given in the following instruction: ")
            print(three_add_instr)
            return 1

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
    error = 0
    assembly_code.nextline('\t.data')
    assembly_code.nextline('newline:\t.asciiz "\n"')
    for var in symbol_table.variables:
        line='%s:\t.word 0'%var
        assembly_code.nextline(line)
    assembly_code.nextline('\t.text')
    assembly_code.nextline('main:')

    for i in range(len(tac.code)):
        if i in tac.leaders:
            assembly_code.nextline('Line_' + str(i + 1) + ':')
        three_add_instr = tac.code[i]
        error1 = translator(three_add_instr, symbol_table, regs)
        if error1 == 1:
            error = 1
            print(three_add_instr)

    # return(code)
    return error

def translator(three_address_instr, symbol_table, regs):
    global end_main
    # parse three_address_instr
    lineno = int(three_address_instr[0])
    op = three_address_instr[1]
    dest = three_address_instr[2]
    src1 = three_address_instr[3]
    src2 = three_address_instr[4]
    error = 1

    if op == '+':
        reg1 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src2, symbol_table, lineno, assembly_code)
        reg3 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('add ' + reg3 + ', ' + reg1 + ', ' + reg2)
        error = 0

    if op =='-':
        reg1 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src2, symbol_table, lineno, assembly_code)
        reg3 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('sub ' + reg3 + ', ' + reg1 + ', ' + reg2)
        error = 0

    if op == '*':
        reg1 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src2, symbol_table, lineno, assembly_code)
        reg3 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('mult ' + reg1 + ', ' + reg2)
        assembly_code.nextline('mflo ' + reg3)#LO 32
        error = 0

    if op =='/':
        reg1 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src2, symbol_table, lineno, assembly_code)
        reg3 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('div ' + reg1 + ', ' + reg2)
        assembly_code.nextline('mflo ' + reg3)#LO
        error = 0

    if op =='%':
        reg1 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src2, symbol_table, lineno, assembly_code)
        reg3 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('div ' + reg1 + ', ' + reg2)
        assembly_code.nextline('mfhi ' + reg3)#HI
        error = 0

############## Integer IO

    if op == 'print_int':
        reg1 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('li $v0, 1')
        assembly_code.nextline('move $a0, ' + reg1)
        assembly_code.nextline('syscall')
        assembly_code.nextline('li $v0, 4')
        assembly_code.nextline('la $a0, newline')
        assembly_code.nextline('syscall')
        error = 0

    if op == 'scan_int':
        reg1 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('li $v0, 5')
        assembly_code.nextline('syscall')
        assembly_code.nextline('move ' + reg1 + ', $v0')
        error = 0

################ UNARY OPERATORS

    if op == '+=':
        #in case of this also it will take a register for the destination variable and it will be initialized to its value in the data declaration
        reg1 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('add ' + reg2 + ', ' + reg2 + ', ' + reg1)
        error = 0

    if op == '-=':
        #in case of this also it will take a register for the destination variable and it will be initialized to its value in the data declaration
        reg1 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('sub ' + reg2 + ', ' + reg2 + ', ' + reg1)
        error = 0

    if op == '*=':
        #in case of this also it will take a register for the destination variable and it will be initialized to its value in the data declaration
        reg1 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('mult ' + reg2 + ', ' + reg1)
        assembly_code.nextline('mflo ' + reg2)
        error = 0

    if op == '/=':
        #in case of this also it will take a register for the destination variable and it will be initialized to its value in the data declaration
        reg1 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('div ' + reg2 + ', ' + reg1)
        assembly_code.nextline('mflo ' + reg2)#HI
        error = 0

    if op == '%=':
        #in case of this also it will take a register for the destination variable and it will be initialized to its value in the data declaration
        reg1 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('div ' + reg2 + ', ' + reg1)
        assembly_code.nextline('mfhi ' + reg2)#HI
        error = 0

    if op == '<<=':
        #in case of this also it will take a register for the destination variable and it will be initialized to its value in the data declaration
        reg1 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('sllv ' + reg2 + ', ' + reg2 + ', ' + reg1)
        error = 0

    if op == '>>=':
        #in case of this also it will take a register for the destination variable and it will be initialized to its value in the data declaration
        reg1 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('srlv ' + reg2 + ', ' + reg2 + ', ' + reg1)
        error = 0

    if op == '<<=':
        #in case of this also it will take a register for the destination variable and it will be initialized to its value in the data declaration
        reg1 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('sllv ' + reg2 + ', ' + reg2 + ', ' + reg1)
        error = 0

    if op == '>>=':
        #in case of this also it will take a register for the destination variable and it will be initialized to its value in the data declaration
        reg1 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('srlv ' + reg2 + ', ' + reg2 + ', ' + reg1)
        error = 0

############## LOGICAL

    # and $t1, $t2, $t3    # $t1 = $t2 & $t3 (bitwise and)
    # or  $t1, $t2, $t3    # $t1 = $t2 | $t3 (bitwise or)

    # # set if equal:
    # seq $t1, $t2, $t3    # $t1 = $t2 == $t3 ? 1 : 0

    # # set if less than:
    # slt $t1, $t2, $t3    # $t1 = $t2 < $t3 ? 1 : 0

    # # set if less than or equal:
    # sle $t1, $t2, $t3    # $t1 = $t2 <= $t3 ? 1 : 0

    if op == '&&':
        reg1 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src2, symbol_table, lineno, assembly_code)
        reg3 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('and ' + reg3 + ', ' + reg1 + ', ' + reg2)
        error = 0

    #A
    if op == '||':
        reg1 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src2, symbol_table, lineno, assembly_code)
        reg3 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('or ' + reg3 + ', ' + reg1 + ', ' + reg2)
        error = 0

    if op == '^': ####
        reg1 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src2, symbol_table, lineno, assembly_code)
        reg3 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('xor ' + reg3 + ', ' + reg1 + ', ' + reg2)
        error = 0

    if op == '!=':
        reg1 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src2, symbol_table, lineno, assembly_code)
        reg3 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('sne ' + reg3 + ', ' + reg1 + ', ' + reg2)
        error = 0

    if op == '<=':
        reg1 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src2, symbol_table, lineno, assembly_code)
        reg3 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('sle ' + reg3 + ', ' + reg1 + ', ' + reg2)
        error = 0

    if op == '>=':
        reg1 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src2, symbol_table, lineno, assembly_code)
        reg3 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('sge ' + reg3 + ', ' + reg1 + ', ' + reg2)
        error = 0

    if op == '==':
        reg1 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src2, symbol_table, lineno, assembly_code)
        reg3 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('seq ' + reg3 + ', ' + reg1 + ', ' + reg2)
        error = 0

    if op == '<':
        reg1 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src2, symbol_table, lineno, assembly_code)
        reg3 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('slt ' + reg3 + ', ' + reg1 + ', ' + reg2)
        error = 0

    if op == '>':
        reg1 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src2, symbol_table, lineno, assembly_code)
        reg3 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('sgt ' + reg3 + ', ' + reg1 + ', ' + reg2)
        error = 0

    if op == '=':
        #in case of this also it will take a register for the destination variable and it will be initialized to its value in the data declaration
        reg1 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        assembly_code.nextline('move ' + reg1 + ', ' + reg2)
        error = 0

    if op == ':=':
        #in case of this also it will take a register for the destination variable and it will be initialized to its value in the data declaration
        reg1 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        assembly_code.nextline('move ' + reg1 + ', ' + reg2)
        error = 0

    if op == '!': #####
        reg1 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src2, symbol_table, lineno, assembly_code)
        reg3 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('li ' + reg1 + ', 1')
        assembly_code.nextline('xor ' + reg3 + ', ' + reg2 + ', ' + reg1)
        error = 0

    if op == '<<':
        reg1 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src2, symbol_table, lineno, assembly_code)
        reg3 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('sllv ' + reg3 + ', ' + reg1 + ', ' + reg2)
        error = 0

    if op == '>>':
        reg1 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src2, symbol_table, lineno, assembly_code)
        reg3 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('srlv ' + reg3 + ', ' + reg1 + ', ' + reg2)
        error = 0

######################### Conditionals
# Note: We haven't handled switch case here
# We will take care of it while parsing

    if op == 'ifgotoeq':
        reg1 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        target = 'Line_' + str(src2)
        assembly_code.nextline('beq ' + reg1 + ', ' + reg2 + ', ' + target)
        error = 0

    if op == 'ifgotoneq':
        reg1 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        target = 'Line_' + str(src2)
        assembly_code.nextline('bne ' + reg1 + ', ' + reg2 + ', ' + target)
        error = 0

    if op == 'ifgotolt':
        reg1 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        target = 'Line_' + str(src2)
        assembly_code.nextline('blt ' + reg1 + ', ' + reg2 + ', ' + target)
        error = 0

    if op == 'ifgotolteq':
        reg1 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        target = 'Line_' + str(src2)
        assembly_code.nextline('ble ' + reg1 + ', ' + reg2 + ', ' + target)
        error = 0

    if op == 'ifgotogt':
        reg1 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        target = 'Line_' + str(src2)
        assembly_code.nextline('bgt ' + reg1 + ', ' + reg2 + ', ' + target)
        error = 0

    if op == 'ifgotogteq':
        reg1 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        reg2 = regs.getreg(src1, symbol_table, lineno, assembly_code)
        target = 'Line_' + str(src2)
        assembly_code.nextline('bge ' + reg1 + ', ' + reg2 + ', ' + target)
        error = 0

    if op == 'goto':
        target = 'Line_' + str(dest)
        assembly_code.nextline('j ' + target)
        error = 0

####################  Loops

    if op == 'break':
        target = 'Line_' + str(dest)
        assembly_code.nextline('j ' + target)
        error = 0

    if op == 'continue':
        target = 'Line_' + str(dest)
        assembly_code.nextline('j ' + target)
        error = 0

    if op == 'for':
        error = 0
    #this is the format of tac for for loop
        # L: if (i>=9) goto END_FOR
        # i=i+1
        # goto L:
        # END_FOR:

#################### FUNCTIONS

    if op == 'return':
        if dest != '':
            reg1 = regs.getreg(dest, symbol_table, lineno, assembly_code)
            assembly_code.nextline('move $v0, ' + reg1)

        assembly_code.nextline('lw $ra, ($sp)')
        assembly_code.nextline('addiu $sp, $sp, 4')
        assembly_code.nextline('lw $fp, ($sp)')
        assembly_code.nextline('addiu $sp, $sp, 4')
        assembly_code.nextline('jr $ra')
        error = 0

    if op == 'return_value':
        reg1 = regs.getreg(dest, symbol_table, lineno, assembly_code)
        assembly_code.nextline('move ' + reg1 + ', $v0')
        error = 0

    if op == 'func':
        if end_main == 0:
            assembly_code.nextline('li $v0, 10')
            assembly_code.nextline('syscall')
            end_main = 1

        assembly_code.nextline('func_' + dest + ':')
        assembly_code.nextline('sub $sp, $sp, 4')
        assembly_code.nextline('sw $fp, ($sp)')
        assembly_code.nextline('sub $sp, $sp, 4')
        assembly_code.nextline('sw $ra, ($sp)')

        error = 0

    if op == 'call':
        assembly_code.nextline('jal func_' + dest)
        error = 0

    return error

if __name__ == '__main__':

    if len(argv) != 2:
        print('Usage: python /path/to/codegen.py /path/to/3AC.ir')
        sys.exit(1)

    input_file = argv[1] # file containing the three address code

    import os
    if os.path.isfile(input_file) == False:
        print('Input file ' + input_file + ' does not exist')
        sys.exit(1)

    errora = read_textfile(input_file)
    if errora != 1:
        error = assmcodegen(tac)
        if error == 0:
            if end_main == 0:
                assembly_code.nextline('li $v0, 10')
                assembly_code.nextline('syscall')
            assembly_code.printcode()
        else:
            print('Unidentified operator in the above line(s)')

