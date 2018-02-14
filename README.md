# PyGM

This is a to-be compiler for GoLang with Python as the implementation language and MIPS as the target language.

In order to run the lexer, follow these steps:
	1. cd asgn1
	2. make
	3. bin/lexer test/test1.go

In order to generate tokens for other input files, just replace the file being passed to the lexer.

Note:
* The lexer was created using PLY (Python Lex-Yacc).
* The following variables were used to create the lexer:
   * token_type_list : It is a dictionary where the key is the type of token. It stores the number of times that particular token occurred.
   * lexeme : It is a dictionary where the key is the type of token. It stores the list of all unique lexemes that match a particular RegEx.

---------------------------------------------------------------------------------------------------------------------------

In order to run the Assembly Code Generator, follow these steps:
	1. cd asgn2
	2. make
	3. bin/codegen test/test01.ir

In order to generate assembly code for other input files, just replace the file being passed to the code generator.

Note:
* The src folder consists of the following files:
	* code.py: It defines the data structure of the code and also for the derived class of it which is the 3AC.
	* codegen.py: It takes 3AC as input file, which then parses it to find the leaders. The leaders are then added into a list. This is followed by the creation of the symbol table and the generation of the assembly code. In this file, we have dealt with translation of each operator individually.
	* lexer.py: This file is the same from the previous assignment, except for the fact that we have defined it as class so ti can be used in subsequent assignments.
	* registers.py: It contains the list of all the registers which are available to us in MIPS. It has "reg_dis" dictionary which maps the registers to variables. The functions such as getnextuse and getemptyreg are implemented using the algorithm discussed in the class. It also contains some auxillary functions for different purposes. "last_use" is used for storing the line number where this register was last used, this is crucial since we don't want to empty the register which is being used in the same line.
	* symbol_table.py: It defines the symbol table, and maintains the list of variables as dictionary. It containes the get_variables function which used the keywords generated by the lexer as varibales. We have populated the symbol table as per the algorithm which was discussed in the class.

* The general format of the ThreeAddressCode is as follows:
	* LineNo, Operand, destination, Source1, Source2 (without spaces)
	* We have taken an implicit assumption that the 3AC will have 5 arguments. So, if let say one of them is not present, we define the entity to be empty. Eg: 1,print_int,aa,,

Authors:
* [Abhishek Jain](https://github.com/Abhi13027)
* [Harkirat Behl](https://github.com/harkiratbehl)
* [Kunal Kapila](https://github.com/kunalkap)
