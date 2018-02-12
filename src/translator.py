# converts and adds directly to the asmblycode

def translator(three_address_instr):
    if verifyreg(three_address_instr[1] == 0):
        L = getreg()
        asmblycode.append('')
