# class for dealing with registers
# symbol table: used for address descriptors

#registers are numbered from 0 to 15

import operator

class registers:
	def __init__(self):

		self.regs = ['$8','$9','$10','$11','$12','$13','$14','$15','$16','$17','$18','$19','$20','$21','$22','$23']
		# 8 + 8 registers from number 8-15 and 16-23
		self.reg_dis = dict((el,0) for el in self.regs)

	def print_regdis(self):
		print(self.reg_dis)

	def getreg(self,tai,symtb):
		if tai[3] in symtb:
			if symtb[tai[3]][1]!=0 and symtb[tai[3]][0][tai[0]-1]==1000:
				return symtb[tai[3]][1]
		if tai[4] in symtb:
			if symtb[[tai[4]]][1]!=0 and symtb[tai[4]][0][tai[0]-1]==1000:
				return symtb[tai[4]][1]
		if freereg != 0:
			return freereg
		#register spilling case
		else:
			sorted_x = sorted(self.reg_dis.items(), key=symtb[operator.itemgetter(1)][0][tai[0]-1], reverse=true)
			return sorted_x[0][0]

	def freereg(self):
		for reg in self.regs:
			if self.reg_dis[reg] != 0:
				return reg
		return 0

	def empty_registers(self,symtb):
		self.reg_dis = dict((el,0) for el in self.regs)
		#####also empty register name of variables
