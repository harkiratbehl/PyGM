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

Authors:
* [Abhishek Jain](https://github.com/Abhi13027)
* [Harkirat Behl](https://github.com/harkiratbehl)
* [Kunal Kapila](https://github.com/kunalkap)
