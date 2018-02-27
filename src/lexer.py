#!/usr/bin/python
"""Using class Lexer, the input code is tokenized;
prints the stream of lexemes and tokens"""

import sys
import ply.lex as lex

class Lexer():
    """Class Lexer takes input code, uses ply.lex and generates the token stream"""
    def __init__(self):
        """Initializes the following variables:
        code stores the input code
        token_stream is the stream of tokens in code in the order in which they appear
        lexemes is the list of lexemes in the input code
        token_type_list is a list of token types of the tokens in the input code
        semimode is a bool which is set if we intend to insert a semimode after the given token
        """
        self.code = []
        self.token_stream = []
        self.lexemes = {}
        self.token_type_list = {}
        self.semimode = False

    def set_code(self, code):
        """Sets the code to the given input code"""
        self.code = code

    def lex_code(self):
        """Tokenizes the code"""
        def set_semicolon_mode():
            """Sets semimode to true if the next token is a new line"""
            if self.code[lexer.lexpos] == '\n':
                self.semimode = True

        # List of keywords reserved in our version of GoLang
        reserved_keywords = {
            'nil'      : 'NIL',
            'default'  : 'DEFAULT',
            'func'     : 'FUNC',
            'select'   : 'SELECT',
            'case'     : 'CASE',
            'go'       : 'GO',
            'struct'   : 'STRUCT',
            'else'     : 'ELSE',
            'goto'     : 'GOTO',
            'package'  : 'PACKAGE',
            'switch'   : 'SWITCH',
            'const'    : 'CONST',
            'if'       : 'IF',
            'type'     : 'TYPE',
            'for'      : 'FOR',
            'import'   : 'IMPORT',
            'var'      : 'VAR',
            'true'     : 'TRUE',
            'false'    : 'FALSE'
        }

        # List of all tokens (including reserved keywords) in our version of GoLang
        tokens = list(reserved_keywords.values()) + [
            'PLUS',
            'MINUS',
            'STAR',
            'DIVIDE',
            'MODULO',
            'AMP',
            'OR',
            'CARET',
            'LS',
            'RS',
            'AND_OR',
            'PLUS_EQ',
            'MINUS_EQ',
            'STAR_EQ',
            'DIVIDE_EQ',
            'MODULO_EQ',
            'AMP_EQ',
            'OR_EQ',
            'CARET_EQ',
            'LS_EQ',
            'RS_EQ',
            'AND_OR_EQ',
            'AMP_AMP',
            'OR_OR',
            'LT_MINUS',
            'PLUS_PLUS',
            'MINUS_MINUS',
            'EQ_EQ',
            'LT',
            'GT',
            'EQ',
            'NOT',
            'NOT_EQ',
            'LT_EQ',
            'GT_EQ',
            'ASSIGN_OP',
            'LSQUARE',
            'RSQUARE',
            'LROUND',
            'RROUND',
            'LCURLY',
            'RCURLY',
            'COMMA',
            'DDD',
            'DOT',
            'SEMICOLON',
            'COLON',
            'SINGLE_QUOTES',
            'DOUBLE_QUOTES',

            'DECIMAL_LIT',
            'OCTAL_LIT',
            'HEX_LIT',
            'FLOAT_LIT',
            'STRING_LIT',

            # 'UNICODE_DIGIT','UNICODE_LETTER',
            # 'ESCAPED_CHAR', 'BYTE_VALUE', 'OCTAL_BYTE_VALUE', 'HEX_BYTE_VALUE',
            # 'UNDERSCORE'
            'NEWLINE',
            'IDENTIFIER',

            'BREAK',
            'CONTINUE',
            'RETURN'
        ]

        t_ignore = ' \t'

        def t_COMMENT(t):
            r'(/\*([^*]|\n|(\*+([^*/]|\n])))*\*+/)|(//.*)'
            pass

        def t_BREAK(t):
            r'break'
            set_semicolon_mode()
            return t

        def t_CONTINUE(t):
            r'continue'
            set_semicolon_mode()
            return t

        def t_RETURN(t):
            r'return'
            set_semicolon_mode()
            return t

        # Note: We need to have tokens in such a way that
        # tokens like '==' should preceede the token '='
        def t_PLUS_PLUS(t):
            r'(\+\+)'
            set_semicolon_mode()
            return t

        def t_MINUS_MINUS(t):
            r'(--)'
            set_semicolon_mode()
            return t

        t_LS_EQ = r'(<<=)'
        t_RS_EQ = r'(>>=)'
        t_AND_OR_EQ = r'(&\^=)'
        t_LS = r'(<<)'
        t_RS = r'(>>)'
        t_AND_OR = r'&\^'
        t_PLUS_EQ = r'(\+=)'
        t_MINUS_EQ = r'(-=)'
        t_STAR_EQ = r'(\*=)'
        t_DIVIDE_EQ = r'/='
        t_MODULO_EQ = r'(%=)'
        t_AMP_EQ = r'(&=)'
        t_OR_EQ = r'(\|=)'
        t_CARET_EQ = r'(\^=)'
        t_AMP_AMP = r'(&&)'
        t_OR_OR = r'(\|\|)'
        t_LT_MINUS = r'(<-)'
        t_EQ_EQ = r'(==)'
        t_NOT_EQ = r'(!=)'
        t_NOT = r'!'
        t_LT_EQ = r'(<=)'
        t_GT_EQ = r'(>=)'
        t_ASSIGN_OP = r'(:=)'
        t_LSQUARE = r'\['
        t_LROUND = r'\('
        t_LCURLY = r'\{'
        t_COMMA = r'\,'
        t_DDD = r'\.\.\.'
        t_DOT = r'\.'
        t_SEMICOLON = r'\;'
        t_COLON = r'\:'
        t_DOUBLE_QUOTES = r'\"'
        t_SINGLE_QUOTES = r'\''
        t_PLUS = r'\+'
        t_MINUS = r'-'
        t_EQ = r'='
        t_LT = r'<'
        t_GT = r'>'
        t_AMP = r'\&'
        t_STAR = r'\*'
        t_DIVIDE = r'\/'
        t_MODULO = r'\%'
        t_OR = r'\|'
        t_CARET = r'\^'

        def t_HEX_LIT(t):
            r'0[x|X][0-9A-Fa-f]+'
            set_semicolon_mode()
            return t

        def t_FLOAT_LIT(t):
            r'([0-9]+\.([0-9]+)?((e|E)(\+|\-)?[0-9]+)?)|([0-9]+(e|E)(\+|\-)?[0-9]+)|(\.[0-9]+((e|E)(\+|\-)?[0-9]+)?)'
            set_semicolon_mode()
            return t

        def t_OCTAL_LIT(t):
            r'0[0-7]*'
            set_semicolon_mode()
            return t

        def t_DECIMAL_LIT(t):
            r'[1-9][0-9]*'
            set_semicolon_mode()
            return t

        def t_RCURLY(t):
            r'\}'
            set_semicolon_mode()
            return t

        def t_RROUND(t):
            r'\)'
            set_semicolon_mode()
            return t

        def t_RSQUARE(t):
            r'\]'
            set_semicolon_mode()
            return t

        def t_STRING_LIT(t):
            r'(\"[^(\")]*\")|(\`[^(\`)]*\`)'
            t.value = t.value[1:-1]
            set_semicolon_mode()
            return t

        def t_NEWLINE(t):
            r'\n+'
            t.lexer.lineno += len(t.value)
            if self.semimode:
                self.semimode = False
                o = lex.LexToken()
                o.type = 'SEMICOLON'
                o.value = ';'
                o.lineno = t.lexer.lineno
                o.lexpos = t.lexer.lexpos
                return o

        def t_IDENTIFIER(t):
            r'[a-zA-Z_@][a-zA-Z_0-9]*'
            t.type = reserved_keywords.get(t.value, 'IDENTIFIER')
            set_semicolon_mode()
            return t

        def t_error(t):
            print("There is an illegal character '%s' in the input program" % t.value[0])
            t.lexer.skip(1)

        lexer = lex.lex()
        lexer.input(self.code)

        tokens_more_than_once = ['IDENTIFIER']

        while 1:
            tokens_generated = lexer.token()
            self.token_stream.append(tokens_generated)

            if not tokens_generated:
                break
            token_name = tokens_generated.value
            token_type = tokens_generated.type

            if token_type not in self.token_type_list:
                self.token_type_list[token_type] = 1
                self.lexemes[token_type] = [token_name]
            else:
                if token_name not in self.lexemes[token_type]:
                    self.lexemes[token_type].append(token_name)
                    self.token_type_list[token_type] += 1
                else:
                    if token_type not in tokens_more_than_once:
                        self.token_type_list[token_type] += 1

    def print_lexemes(self):
        """Prints the lexemes in a tabular format"""
        print("Token" + " " * 20 + "Occurrances" + " " * 22 + "Lexemes")
        print("-" * 65)

        for data in self.token_type_list:
            sys.stdout.write("{:25s} {:>4s}".format(data, (str)(self.token_type_list[data])))
            print("{:>35s}".format(self.lexemes[data][0]))
            for lexlist in self.lexemes[data][1:]:
                sys.stdout.write("{:>65s}\n".format(lexlist))
            print("-" * 65)

    def print_tokens(self):
        """Prints the token stream in order"""
        for token in self.token_stream:
            print(token)

if __name__ == "__main__":

    cmd_len = len(sys.argv)
    print_op = 0

    if cmd_len != 2 and cmd_len != 3:
        print('Usage: python /path/to/lexer.py /path/to/code.go print_op')
        print('print_op is optional, with default value 0')
        print('If print_op is 0, print Nothing')
        print('If print_op is 1, print lexemes')
        print('If print_op is 2, print token stream')
        print('If print_op is 3, print lexemes and token stream')
        sys.exit(1)

    input_file = sys.argv[1]
    if cmd_len == 2:
        print('Using default value of print_op i.e. 0')

    if cmd_len == 3:
        print_op = int(sys.argv[2])

    import os
    if os.path.isfile(input_file) is False:
        print('Input file ' + input_file + ' does not exist')
        sys.exit(1)

    input_code = open(input_file, 'r').read()
    if input_code[len(input_code)-1] != '\n':
        input_code += '\n'

    lexer_obj = Lexer()
    lexer_obj.set_code(input_code)

    lexer_obj.lex_code()

    if print_op & 1:
        lexer_obj.print_lexemes()
    if print_op & 2:
        lexer_obj.print_tokens()
