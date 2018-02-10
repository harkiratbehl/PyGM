import sys
from sys import argv
from code import *
from registers import *
from symtb import *

#put into TAC
#write nextuse
#write getreg
#write translator

Tac = tac()
asmblycode = code()
symtb = symtb()
# regs = registers()

def read_textfile(inputfile): #generates tac and symtb
	file = open(inputfile,'r')
	for line in file:
		line= line.rstrip('\n')
		tai=line.split(',')
		Tac.addline(tai)
		length=len(tai)
		if tai[1] == 'ifgoto':#might need change
			Tac.leaders.append(len(Tac.code)+1)
			Tac.leaders.append(int(tai[length-1]))

		if tai[1] == 'goto' or tai[1] == 'break' or tai[1] == 'continue':
			Tac.leaders.append(len(Tac.code)+1)
			Tac.leaders.append(int(tai[2]))

	Tac.leaders = sorted(Tac.leaders, key=int)

	symtb.fill_symtb(code)

#def translator(tai): #converts and adds directly to the asmblycode

def gencode(Tac):

	#for block i (basic-blcok local register allocator)
	#make nextuse(symbol table)
	#translate each statement

	#block transition thing
	for i in range(len(Tac.code)):
		instruction = Tac.code[i]
		tai = instruction.split(',')
		# translator(tai)
	# return(code)

if __name__ == '__main__':
	inputfile = argv[1] #the tac text flie
	read_textfile(inputfile)
	Tac.printcode()
	# mipscode = gencode(Tac)
