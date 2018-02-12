# converts and adds directly to the asmblycode

def translator(three_address_instr, symbol_table, regs):
    ans = []
    src1 = three_address_instr[3]
    src2 = three_address_instr[4]
    print(src1)
    print(src2)
    print(type(symbol_table.symbol_table))
    reg_resultant = regs.getreg(three_address_instr, symbol_table)
    print(reg_resultant)
    if src1 in symbol_table.symbol_table:
        if symbol_table.symbol_table[src1][1] != 0 and symbol_table.symbol_table[src1][1] != reg_resultant:
            ans += ["move " + reg_resultant + " " + symbol_table.symbol_table[src1][1]]
    else:
        ans += ["li " + reg_resultant + src1]

    constant = 0
    if src2 in symbol_table.symbol_table:
        temp = symbol_table.symbol_table[src2][1]
    else:
        constant = 1
        temp = src2
    op = three_address_instr[1]
    if op == '+':
        if constant == 1:
            ans += ["addi " + reg_resultant + " " + reg_resultant + " " + temp]
        else:
            ans += ["add " + reg_resultant + " " + reg_resultant + " " + temp]

    return ans

