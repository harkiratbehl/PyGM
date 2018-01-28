# PyGM
Authors - Abhishek Jain, Harkirat Behl, Kunal Kapila 

The Compiler that we are going to create will have the following specification
Source Language: GoLang
Implementation Language: Python
Target LanguageL: MIPS

In order to run the code, you need to follow these steps -

1. cd asgn1
2. make
3. bin/lexer test/test1.go
   In order to run other files, just change the file to test2.go, test3.go ..... etc.

Note:

1. The tool that we used to create the lexer was PLY.
2. We used the following data-structures - 
        a) token_type : It is a dictionary where the key is basically the type of token. It basically stores the                 number of times a particular token has occurred. 
        b) lexeme : It is also a dictionary where the key is again the type of token. It basically stores the list of all lexemes that matches a particular token Regular Expression.



