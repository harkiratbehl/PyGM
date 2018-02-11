 #converts and adds directly to the asmblycode

def translator(tai):
	if verifyreg(tai[1]==0):
		L=getreg()
		asmblycode.append('')
