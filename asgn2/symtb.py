import sys
sys.path.insert(0,r'/Users/harkiratbehl/acads/sem10/CS335/PyGM/src')
from collections import OrderedDict
import lexer

variables=[]

class symtb:
	def __init__(self):
		self.symtb = OrderedDict()
		self.nextuse = []

	def get_variables(self,code):
		variables = return_variables()

	def fill_symtb(self,code):
		self.get_variables(code)
		numoflines=len(code)
		#constructing fields for each variable
		for var in variables:
			self.symtb[var] = np.zeros(numoflines)
		#going back from last line of block
		for i in range(len(code)):
			j=numoflines-i-1
			tai = code[j]
			if tai[2] in self.symtb:
				self.symtb[tai[2]][j] = 1
			if tai[3] in self.symtb:
				self.symtb[tai[3]][j] = 1
