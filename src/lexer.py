#!/usr/bin/python

import ply.lex as lex
import sys

# The following are the list of kwywords which are reserved in GoLang
reserved_keywords = {
    'break'    : 'BREAK',
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
    'continue' : 'CONTINUE',
    'for'      : 'FOR',
    'import'   : 'IMPORT',
    'return'   : 'RETURN',
    'var'      : 'VAR',
    'true'     : 'TRUE',
    'false'    : 'FALSE'
}

# These are the list of all tokens which we will be going to use in our building of lexer
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

    #'UNICODE_DIGIT','UNICODE_LETTER',
    # 'ESCAPED_CHAR', 'BYTE_VALUE', 'OCTAL_BYTE_VALUE', 'HEX_BYTE_VALUE',
    # 'UNDERSCORE'
    'NEWLINE',
    'IDENTIFIER'
]

# Note: We need to have tokens in such a way that the tokens like '==' should preceede the token '='
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
t_LT_MINUS  = r'(<-)'
t_PLUS_PLUS = r'(\+\+)'
t_MINUS_MINUS = r'(--)'
t_EQ_EQ = r'(==)'
t_NOT_EQ = r'(!=)'
t_NOT = r'!'
t_LT_EQ = r'(<=)'
t_GT_EQ = r'(>=)'
t_ASSIGN_OP = r'(:=)'
t_LSQUARE = r'\['
t_RSQUARE = r'\]'
t_LROUND = r'\('
t_RROUND = r'\)'
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_COMMA = r'\,'
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

DECIMAL_DIGIT = r'[0-9]'
DECIMALS = DECIMAL_DIGIT + DECIMAL_DIGIT + r'*'
EXPONENT = r'(e|E)(\+|-)?' + DECIMALS
OCTAL_DIGIT = r'[0-7]'
HEX_DIGIT = r'[0-9A-Fa-f]'

t_DECIMAL_LIT = r'[1-9]' + DECIMAL_DIGIT + r'*'
t_OCTAL_LIT = r'0' + OCTAL_DIGIT + r'*'
t_HEX_LIT = r'0[x|X]' + HEX_DIGIT + HEX_DIGIT + r'*'
t_FLOAT_LIT = r'(' + DECIMALS + r'\.(' + DECIMALS + r')?(' + EXPONENT + r')?)|(' + DECIMALS + EXPONENT + r')|(\.' + DECIMALS + r'(' + EXPONENT + r')?)'

def t_STRING_LIT(t):
    r'(\"[^(\")]*\")|(\`[^(\`)]*\`)'
    t.value = t.value[1:-1]
    return t

t_ignore = ' \t'

def t_COMMENT(t):
    r'(/\*([^*]|\n|(\*+([^*/]|\n])))*\*+/)|(//.*)'
    pass

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_IDENTIFIER(t):
    r'[a-zA-Z_@][a-zA-Z_0-9]*'
    t.type = reserved_keywords.get(t.value, 'IDENTIFIER')
    return t

def t_error(t):
    print("There is an illegal character '%s' in the input program" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
lexer.input(open(sys.argv[1],'r').read())
token_type_list = {}
lexeme_list = {}

tokens_more_than_once = ['IDENTIFIER']

while 1:
    tokens_generated = lexer.token()
    if not tokens_generated:
        break
    token_name = tokens_generated.value
    token_type = tokens_generated.type

    if token_type not in token_type_list:
        token_type_list[token_type]= 1
        lexeme_list[token_type] = []
        lexeme_list[token_type].append(token_name)
    else:
        if token_name not in lexeme_list[token_type]:
            lexeme_list[token_type].append(token_name)
            token_type_list[token_type] = token_type_list[token_type] + 1
        else:
            if token_type not in tokens_more_than_once:
                token_type_list[token_type] = token_type_list[token_type] + 1

print("Token"+" "*20+"Occurrances"+" "*22+"Lexemes")
print("-"*65)

for data in token_type_list:
    sys.stdout.write("{:25s} {:>4s}".format(data, (str)(token_type_list[data])))
    print("{:>35s}".format(lexeme_list[data][0]))
    for lexlist in lexeme_list[data][1:]:
        sys.stdout.write("{:>65s}\n".format(lexlist))
    print("-"*65)

