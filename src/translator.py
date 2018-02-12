# converts and adds directly to the asmblycode

def translator(three_address_instr, symbol_table, regs):
    src1 = three_address_instr[3]
    src2 = three_address_instr[4]
    dest = three_address_instr[2]
    op = three_address_instr[1]
    lineno=three_address_instr[0]
    if op == '+':
        reg1,line1 = regs.getreg(src1,symbol_table,lineno)
        reg2,line2 = regs.getreg(src2,symbol_table,lineno)
        reg3,line3 = regs.getreg(dest,symbol_table,lineno)
        return line1 + '\n' + line2 +'\n'+line3+'\n'+'add '+reg3+', '+reg1+', '+reg2

