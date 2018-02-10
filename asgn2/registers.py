# class for dealing with registers
# symbol table: used for address descriptors

class registers:
	def __init__(self, Symtb):
		self.freeregs = ['$8','$9','$10','$11','$12','$13','$14','$15','$16','$17','$18','$19','$20','$21','$22','$23']
		# 8 + 8 registers from number 8-15 and 16-23
		self.Symtb = Symtb
		self.regdis = {} #keep track of what is currently in register


	# def getReg(self,var):
		
