# Class for dealing with registers
# symbol table: used for address descriptors
# registers are numbered from 0 to 15

from operator import itemgetter

class registers:
    def __init__(self):
        # 8 + 8 registers in MIPS numbered from 8 - 15 and 16 - 23
        self.regs = ['$8', '$9', '$10', '$11', '$12', '$13', '$14', '$15', '$16', '$17', '$18', '$19', '$20', '$21', '$22', '$23']
        self.reg_dis = dict((el, 0) for el in self.regs)
        self.nextuse = dict((el, 0) for el in self.regs)

    def print_regdis(self):
        print(self.reg_dis)

    def getnextuse(self,lineno,symbol_table):       #returns register with maximum next use
        max=0
        reg=''
        for key in self.reg_dis:
            a= symbol_table.symbol_table[self.reg_dis[key]][0][lineno-1]
            if a>max:
                max=a
                reg = key
        return reg

    def freereg(self):              #checks if any register is free and returns it
        for reg in self.regs:
            # print(self.reg_dis[reg])
            if self.reg_dis[reg] == 0:
                return reg
        for reg in self.regs:
            if self.reg_dis[reg] == 1:#for registers used for constants
                return reg
        return 0

    def getemptyreg(self,lineno,symbol_table,assembly_code):
        if self.freereg() != 0:
            return self.freereg()
        else:
            # register spilling case

            reg = self.getnextuse(lineno,symbol_table)
            symbol_table.symbol_table[self.reg_dis[reg]][1] = 0
            line1='la $a0, '+ self.reg_dis[reg]
            assembly_code.nextline(line1)
            line2='sw ' + reg+ ' 0($a0)'
            assembly_code.nextline(line2)
            self.reg_dis[reg] = 0


            # putting back the value of spilled register data variable into its address
            # la $a0, globalVariable #get address
            # li $a1, 11 #new value
            # sw $a1 0($a0) #save new value

            return reg



    def getreg(self, var, symbol_table,lineno,assembly_code):
        if var in symbol_table.symbol_table:
            if symbol_table.symbol_table[var][1] != 0:
                return symbol_table.symbol_table[var][1]
            else:
                arf = self.getemptyreg(lineno,symbol_table,assembly_code)
                symbol_table.symbol_table[var][1] = arf
                self.reg_dis[arf]=var
                line = 'lw ' + arf + ', ' + var
                assembly_code.nextline(line)
                return arf
        else:               #assigning registr for constant
            arf = self.getemptyreg(lineno,symbol_table,assembly_code)
            self.reg_dis[arf]=1
            line = 'li ' + arf + ', ' + var
            assembly_code.nextline(line)
            return arf

    def empty_all_registers(self, symbol_table):
        self.reg_dis = dict((el, 0) for el in self.regs)
        # also empty register name for variables stored in symbol_table.symbol_table
        for var in symbol_table.symbol_table.variables:
            symbol_table.symbol_table[var][1] = 0

