import sys
from sys import argv
from code import *
from registers import *
from symtb import *
from translator import *

#put into TAC
#write nextuse
#write getreg
#write translator

Tac = tac()
asmblycode = code()
symtb = symtb()
# regs = registers()

def read_textfile(inputfile): #generates tac and leaders and generate symbol table
	file = open(inputfile,'r')
	for line in file:
		line= line.rstrip('\n')
		tai=line.split(',')
		Tac.nextline(tai)
		length=len(tai)
		if tai[1] == 'ifgoto':#might need change
			Tac.leaders.append(len(Tac.code)+1)
			Tac.leaders.append(int(tai[length-1]))

		if tai[1] == 'goto' or tai[1] == 'break' or tai[1] == 'continue':
			Tac.leaders.append(len(Tac.code)+1)
			Tac.leaders.append(int(tai[2]))

	Tac.leaders = sorted(Tac.leaders, key=int)

	print(Tac.code)
	symtb.fill_symtb(Tac)
	regs = registers()
	regs.print_regdis()

def assmcodegen(Tac):

	#data region to handle global data and constants
	asmblycode.nextline('.data')
	for var in symtb.variables:
		line='%s:\t.space 150'%var
		asmblycode.nextline(line)
	asmblycode.nextline('.text')
	asmblycode.nextline('main:')


	for i in range(len(Tac.code)):
		tai = Tac.code[i]
		#translator(tai)

	#return(code)
	asmblycode.printcode()

if __name__ == '__main__':
	inputfile = argv[1] #the tac text file
	read_textfile(inputfile)
	assmcodegen(Tac)

	# Tac.printcode()
	# mipscode = codegen(Tac)
