#!/usr/bin/python

"""Generate Assembly code from 3AC"""

import sys
from code import Code, ThreeAddressCode
from registers import Registers
from symbol_table import SymbolTable

three_addr_code = ThreeAddressCode()
assembly_code = Code()
registers = Registers()
input_file = ''

start_main = 0

def convert_tac(ThreeAddressCode):
    """Reads three adress code generated from parser and converts to TAC for codegen;
    generates the three_addr_code along with leaders;
    populates generate symbol table as per three_addr_code"""

    for i in range(ThreeAddressCode.length()):
        three_addr_instr = ThreeAddressCode.code[i]
        three_addr_instr = [str(i+1)] + three_addr_instr
        three_addr_code.add_line(three_addr_instr)


        if len(three_addr_instr) != 5:
            print("Incorrect size for the following instruction: ")
            print(three_addr_instr)
            return -1

        if three_addr_instr[0] == '':
            print("Line number not given in the following instruction: ")
            print(three_addr_instr)
            return -1

        import re
        if re.search(r'\D', three_addr_instr[0]) != None:
            print("Invalid line number given in the following instruction: ")
            print(three_addr_instr)
            return -1

        leader_generating_if_instr = []
        leader_generating_if_instr += ['ifgotoeq']
        leader_generating_if_instr += ['ifgotoneq']
        leader_generating_if_instr += ['ifgotolt']
        leader_generating_if_instr += ['ifgotolteq']
        leader_generating_if_instr += ['ifgotogt']
        leader_generating_if_instr += ['ifgotogteq']

        if three_addr_instr[1] in leader_generating_if_instr:
            three_addr_code.add_leader(three_addr_code.length())

        leader_generating_other_instr = ['label']
        if three_addr_instr[1] in leader_generating_if_instr:
            three_addr_code.add_leader(three_addr_code.length()-1)

        leader_generating_other_instr = []
        leader_generating_other_instr += ['goto']
        leader_generating_other_instr += ['break']
        leader_generating_other_instr += ['continue']
        if three_addr_instr[1] in leader_generating_other_instr:
            three_addr_code.add_leader(three_addr_code.length())

    three_addr_code.leaders = sorted(three_addr_code.leaders, key=int)
    return three_addr_code

def generate_assembly(three_addr_code,var_list,symbol_table):
    """Generate assembly code"""

    # data region to handle global data and constants
    assembly_code.add_line('\t.data')
    assembly_code.add_line('newline:\t.asciiz "\n"')

    #declaring variables from list of variables
    for var in var_list:
        line = '%s:\t.word 0' % var
        assembly_code.add_line(line)

    # functions
    assembly_code.add_line('\t.text')

    global start_main

    translator_error = 0
    for i in range(three_addr_code.length()):
        # if i in three_addr_code.leaders:
        #     assembly_code.add_line('Line_' + str(i + 1) + ':')
        three_addr_instr = three_addr_code.code[i]
        if translator(three_addr_instr,symbol_table) != 0:
            translator_error = 1
            print('Unidentified operator in this Three Address Instruction: ' + ", ".join(three_addr_instr))
            return

    if start_main == 1:
        assembly_code.add_line('li $v0, 10')
        assembly_code.add_line('syscall')

    return assembly_code

def translator(three_addr_instr,symbol_table):
    """Translate Three Address Instruction to Assembly"""
    global start_main

    # parse three_addr_instr
    line_no = int(three_addr_instr[0])
    instr_op = three_addr_instr[1]

    dest = three_addr_instr[2]
    src1 = three_addr_instr[3]
    src2 = three_addr_instr[4]

    if instr_op == 'label':
        assembly_code.add_line(dest + ':')
        return 0

    if instr_op == 'goto':
        assembly_code.add_line('j ' + dest)
        return 0

    if instr_op == 'break':
        assembly_code.add_line('j ' + dest)
        return 0

    if instr_op == 'continue':
        assembly_code.add_line('j ' + dest)
        return 0

    if instr_op == 'func':
        if dest == 'scope_global_main':
            assembly_code.add_line('main:')
            start_main = 1

        if dest != 'main' and start_main == 1:
            assembly_code.add_line('li $v0, 10')
            assembly_code.add_line('syscall')
            start_main = 0

        if dest != 'main':
            assembly_code.add_line('func_' + dest + ':')
            assembly_code.add_line('sub $sp, $sp, 4')
            assembly_code.add_line('sw $fp, ($sp)')
            assembly_code.add_line('sub $sp, $sp, 4')
            assembly_code.add_line('sw $ra, ($sp)')
        return 0

    if instr_op == 'call':
        assembly_code.add_line('jal func_' + dest)
        return 0


    # Using reg_dest
    if dest != '':
        reg_dest = registers.get_register(dest, symbol_table, line_no, assembly_code)

    if instr_op == 'print_int':
        assembly_code.add_line('li $v0, 1')
        assembly_code.add_line('move $a0, ' + reg_dest)
        assembly_code.add_line('syscall')
        assembly_code.add_line('li $v0, 4')
        assembly_code.add_line('la $a0, newline')
        assembly_code.add_line('syscall')
        return 0

    if instr_op == 'scan_int':
        assembly_code.add_line('li $v0, 5')
        assembly_code.add_line('syscall')
        assembly_code.add_line('move ' + reg_dest + ', $v0')
        return 0

    if instr_op == 'return':
        if dest != '':
            assembly_code.add_line('move $v0, ' + reg_dest)

        assembly_code.add_line('lw $ra, ($sp)')
        assembly_code.add_line('addiu $sp, $sp, 4')
        assembly_code.add_line('lw $fp, ($sp)')
        assembly_code.add_line('addiu $sp, $sp, 4')
        assembly_code.add_line('jr $ra')
        return 0

    if instr_op == 'return_value':
        assembly_code.add_line('move ' + reg_dest + ', $v0')
        return 0

    if instr_op == 'get_val_at_add':
        # write src1 to address dest
        assembly_code.add_line('la ' + reg_dest + ', ' + src1)
        return 0


    # Using reg_src1
    if src1 != '':
        reg_src1 = registers.get_register(src1, symbol_table, line_no, assembly_code)

    if instr_op == '+=':
        assembly_code.add_line('add ' + reg_dest + ', ' + reg_dest + ', ' + reg_src1)
        return 0

    if instr_op == '-=':
        assembly_code.add_line('sub ' + reg_dest + ', ' + reg_dest + ', ' + reg_src1)
        return 0

    if instr_op == '*=':
        assembly_code.add_line('mult ' + reg_dest + ', ' + reg_src1)
        assembly_code.add_line('mflo ' + reg_dest)
        return 0

    if instr_op == '/=':
        assembly_code.add_line('div ' + reg_dest + ', ' + reg_src1)
        assembly_code.add_line('mflo ' + reg_dest) # HI
        return 0

    if instr_op == '%=':
        assembly_code.add_line('div ' + reg_dest + ', ' + reg_src1)
        assembly_code.add_line('mfhi ' + reg_dest) # HI
        return 0

    if instr_op == '<<=':
        assembly_code.add_line('sllv ' + reg_dest + ', ' + reg_dest + ', ' + reg_src1)
        return 0

    if instr_op == '>>=':
        assembly_code.add_line('srlv ' + reg_dest + ', ' + reg_dest + ', ' + reg_src1)
        return 0

    if instr_op == '=':
        assembly_code.add_line('move ' + reg_dest + ', ' + reg_src1)
        return 0

    if instr_op == ':=':
        assembly_code.add_line('move ' + reg_dest + ', ' + reg_src1)
        return 0

    if instr_op == 'ifgotoeq':
        assembly_code.add_line('beq ' + reg_dest + ', ' + reg_src1 + ', ' + src2)
        return 0

    if instr_op == 'ifgotoneq':
        assembly_code.add_line('bne ' + reg_dest + ', ' + reg_src1 + ', ' + src2)
        return 0

    if instr_op == 'ifgotolt':
        assembly_code.add_line('blt ' + reg_dest + ', ' + reg_src1 + ', ' + src2)
        return 0

    if instr_op == 'ifgotolteq':
        assembly_code.add_line('ble ' + reg_dest + ', ' + reg_src1 + ', ' + src2)
        return 0

    if instr_op == 'ifgotogt':
        assembly_code.add_line('bgt ' + reg_dest + ', ' + reg_src1 + ', ' + src2)
        return 0

    if instr_op == 'ifgotogteq':
        assembly_code.add_line('bge ' + reg_dest + ', ' + reg_src1 + ', ' + src2)
        return 0

    if instr_op == 'read_add':
        # read from src1 address to dest
        # Similar to * operator or dereferencing
        assembly_code.add_line('lw ' + reg_dest + ', ' + '0(' + reg_src1+ ')')
        return 0

    if instr_op == 'write_add':
        # write src1 to address dest
        assembly_code.add_line('sw ' + reg_dest + ', ' + '0(' + reg_src1+ ')')
        return 0


    # Using reg_src2
    if src2 != '':
        reg_src2 = registers.get_register(src2, symbol_table, line_no, assembly_code)

    if instr_op == '+':
        if src2 != '':
            assembly_code.add_line('add ' + reg_dest + ', ' + reg_src1 + ', ' + reg_src2)
        else:
            assembly_code.add_line('move ' + reg_dest + ', ' + reg_src1)
        return 0

    if instr_op == '-':
        if src2 != '':
            assembly_code.add_line('sub ' + reg_dest + ', ' + reg_src1 + ', ' + reg_src2)
        else:
            src1 = '-' + src1
            reg_src1 = registers.get_register(src1, symbol_table, line_no, assembly_code)
            assembly_code.add_line('move ' + reg_dest + ', ' + reg_src1)
        return 0

    if instr_op == '*':
        assembly_code.add_line('mult ' + reg_src1 + ', ' + reg_src2)
        assembly_code.add_line('mflo ' + reg_dest) # LO 32
        return 0

    if instr_op == '/':
        assembly_code.add_line('div ' + reg_src1 + ', ' + reg_src2)
        assembly_code.add_line('mflo ' + reg_dest) # LO
        return 0

    if instr_op == '%':
        assembly_code.add_line('div ' + reg_src1 + ', ' + reg_src2)
        assembly_code.add_line('mfhi ' + reg_dest) # HI
        return 0

    if instr_op == '&&':
        assembly_code.add_line('and ' + reg_dest + ', ' + reg_src1 + ', ' + reg_src2)
        return 0

    if instr_op == '||':
        assembly_code.add_line('or ' + reg_dest + ', ' + reg_src1 + ', ' + reg_src2)
        return 0

    if instr_op == '^':
        assembly_code.add_line('xor ' + reg_dest + ', ' + reg_src1 + ', ' + reg_src2)
        return 0

    if instr_op == '!=':
        assembly_code.add_line('sne ' + reg_dest + ', ' + reg_src1 + ', ' + reg_src2)
        return 0

    if instr_op == '<=':
        assembly_code.add_line('sle ' + reg_dest + ', ' + reg_src1 + ', ' + reg_src2)
        return 0

    if instr_op == '>=':
        assembly_code.add_line('sge ' + reg_dest + ', ' + reg_src1 + ', ' + reg_src2)
        return 0

    if instr_op == '==':
        assembly_code.add_line('seq ' + reg_dest + ', ' + reg_src1 + ', ' + reg_src2)
        return 0

    if instr_op == '<':
        assembly_code.add_line('slt ' + reg_dest + ', ' + reg_src1 + ', ' + reg_src2)
        return 0

    if instr_op == '>':
        assembly_code.add_line('sgt ' + reg_dest + ', ' + reg_src1 + ', ' + reg_src2)
        return 0

    if instr_op == '!':
        assembly_code.add_line('li ' + reg_src1 + ', 1')
        assembly_code.add_line('xor ' + reg_dest + ', ' + reg_src2 + ', ' + reg_src1)
        return 0

    if instr_op == '<<':
        assembly_code.add_line('sllv ' + reg_dest + ', ' + reg_src1 + ', ' + reg_src2)
        return 0

    if instr_op == '>>':
        assembly_code.add_line('srlv ' + reg_dest + ', ' + reg_src1 + ', ' + reg_src2)
        return 0

    return 1

def codegen():
    """defines a function for codegen"""

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Usage: python /path/to/codegen.py /path/to/3AC.ir')
        sys.exit(1)

    input_file = sys.argv[1] # file containing the three address code

    import os
    if os.path.isfile(input_file) is False:
        print('Input file ' + input_file + ' does not exist')
        sys.exit(1)

    if read_input_file() == 0:
        if generate_assembly() == 0:
            # if start_main == 1:
                # assembly_code.add_line('li $v0, 10')
                # assembly_code.add_line('syscall')
            assembly_code.print_code()
        else:
            print('Unidentified operator in the above line(s)')
