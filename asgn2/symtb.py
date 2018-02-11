import sys
from collections import OrderedDict
import numpy as np

#added nextuse
#added address descriptor

class symtb:
	def __init__(self):
		self.symtb = {}#OrderedDict()
		self.nextuse = []
		self.variables=[]

	def get_variables(self,Tac):
		#variables = return_variables()
		self.variables = ['t1','a','t2','b','t3','t4','t5','t6']

	def fill_symtb(self,Tac):
		self.get_variables(Tac)
		numoflines=len(Tac.code)
		#constructing fields for each variable
		for var in self.variables:
			self.symtb[var] = [1000*np.ones(numoflines),0] #second element is the name of the regiser


		#going back from last line of block
		for i in range(numoflines):
			j=numoflines-i-1
			tai = Tac.code[j]
			if tai[3] in self.symtb:
				for r in range(0,j):
					self.symtb[tai[3]][0][r] = j+1
			if tai[4] in self.symtb:
				for r in range(0,j):
					self.symtb[tai[4]][0][r] = j+1

		print(self.symtb)
