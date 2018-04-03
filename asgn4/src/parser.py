#!/usr/bin/python
import ply.lex as lex
import ply.yacc as yacc
from lexer import tokens

from code import TreeNode
from code import ThreeAddressCode
import sys
from random import *
import logging

parsed=[]

ThreeAddrCode = ThreeAddressCode()

def temp_gen():
    i = randint(0, sys.maxint)
    return 'temp_' + str(i)

precedence = (
    ('left','IDENTIFIER'),
    ('right','ASSIGN_OP'),
    ('left','COMMA'),
    ('left','LSQUARE'),
    ('left','RSQUARE'),
    ('left','LCURLY'),
    ('left','RCURLY'),
    ('left','DDD'),
    ('left','DOT'),
    ('left','SEMICOLON'),
    ('left','COLON'),
    ('left','SINGLE_QUOTES'),
    ('left','DOUBLE_QUOTES'),
    ('left','DECIMAL_LIT'),
    ('left','OCTAL_LIT'),
    ('left','HEX_LIT'),
    ('left','FLOAT_LIT'),
    ('left','STRING_LIT'),
    ('left','NEWLINE'),
    ('left','BREAK'),
    ('left','CONTINUE'),
    ('left','RETURN'),
    ('left','RROUND'),
    ('left','LROUND'),
    ('left', 'OR_OR'),
    ('left', 'AMP_AMP'),
    ('left', 'EQ_EQ', 'NOT_EQ','LT','LT_EQ','GT','GT_EQ'),
    ('left', 'PLUS', 'MINUS','OR','CARET'),
    ('left', 'STAR', 'DIVIDE','MODULO','AMP','AND_OR','LS','RS'),
)

def p_SourceFile(p):
    '''SourceFile : PACKAGE IDENTIFIER  SEMICOLON ImportDeclList TopLevelDeclList
    '''
    parsed.append(p.slice)

def p_ImportDeclList(p):
    '''ImportDeclList : ImportDecl SEMICOLON ImportDeclList
                | empty
    '''
    parsed.append(p.slice)

def p_TopLevelDeclList(p):
    '''TopLevelDeclList : TopLevelDecl SEMICOLON TopLevelDeclList
                | empty
    '''
    parsed.append(p.slice)

def p_TopLevelDecl(p):
    '''TopLevelDecl  : Declaration
                | FunctionDecl
    '''
    parsed.append(p.slice)

def p_ImportDecl(p):
    '''ImportDecl : IMPORT LROUND ImportSpecList RROUND
                | IMPORT ImportSpec
    '''
    parsed.append(p.slice)

def p_ImportSpecList(p):
    '''ImportSpecList : ImportSpec SEMICOLON ImportSpecList
                | empty
    '''
    parsed.append(p.slice)

def p_ImportSpec(p):
    '''ImportSpec :  DOT string_lit
                | IDENTIFIER string_lit
                | empty string_lit
    '''
    parsed.append(p.slice)

def p_Block(p):
    '''Block : LCURLY StatementList RCURLY
    '''
    parsed.append(p.slice)

def p_StatementList(p):
    '''StatementList : Statement SEMICOLON StatementList
                 | empty
    '''
    parsed.append(p.slice)

def p_Statement(p):
    '''Statement : Declaration
                 | SimpleStmt
                 | ReturnStmt
                 | Block
                 | IfStmt
                 | SwitchStmt
                 | ForStmt
                 | BreakStmt
                 | ContinueStmt
                 | GotoStmt
    '''
    parsed.append(p.slice)

def p_Declaration(p):
    '''Declaration  : ConstDecl
                 | TypeDecl
                 | VarDecl
    '''
    parsed.append(p.slice)

def p_ConstDecl(p):
    '''ConstDecl : CONST LROUND ConstSpecList RROUND
                 | CONST ConstSpec
                 | CONST IDENTIFIER
    '''
    parsed.append(p.slice)

def p_ConstSpecList(p):
    '''ConstSpecList : empty
                 | ConstSpecList ConstSpec SEMICOLON
                 | ConstSpecList IDENTIFIER SEMICOLON
    '''
    parsed.append(p.slice)

def p_ConstSpec(p):
    '''ConstSpec : IdentifierList
                 | IdentifierList Type EQ Expression
                 | IDENTIFIER Type EQ Expression
                 | IdentifierList Type EQ ExpressionList
                 | IDENTIFIER Type EQ ExpressionList
                 | IdentifierList IDENTIFIER DOT IDENTIFIER EQ Expression
                 | IDENTIFIER IDENTIFIER DOT IDENTIFIER EQ Expression
                 | IdentifierList IDENTIFIER DOT IDENTIFIER EQ ExpressionList
                 | IDENTIFIER IDENTIFIER DOT IDENTIFIER EQ ExpressionList
                 | IdentifierList IDENTIFIER EQ Expression
                 | IDENTIFIER IDENTIFIER EQ Expression
                 | IdentifierList IDENTIFIER EQ ExpressionList
                 | IDENTIFIER IDENTIFIER EQ ExpressionList
                 | IdentifierList EQ Expression
                 | IDENTIFIER EQ Expression
                 | IdentifierList EQ ExpressionList
                 | IDENTIFIER EQ ExpressionList
    '''
    parsed.append(p.slice)

def p_IdentifierList(p):
    '''IdentifierList : IDENTIFIER IdentifierBotList
    '''
    # p[0] = [{'place': p[1]}] + p[2]
    parsed.append(p.slice)

def p_IdentifierBotList(p):
    '''IdentifierBotList : COMMA IDENTIFIER
                 | IdentifierBotList COMMA IDENTIFIER
    '''
    return
    # if len(p) == 3:
        # p[0] = [{'place': p[2]}]
        # return
    # elif len(p) == 4:
        # p[0] = p[1] + [{'place': p[3]}]
        # return

def p_ExpressionList(p):
    '''ExpressionList : Expression COMMA ExpressionBotList
    '''
    p[0] = TreeNode('ExpressionList', 0, 'INT', 0, p[1].children + p[3].children)
    return

def p_ExpressionBotList(p):
    '''ExpressionBotList : Expression COMMA ExpressionBotList
                        | Expression
    '''
    if len(p) == 2:
        p[0] = TreeNode('ExpressionBotList', 0, 'INT', 0, p[1].children)
        return
    elif len(p) == 4:
        p[0] = TreeNode('ExpressionBotList', 0, 'INT', 0, p[1].children + p[3].children)
        return

def p_TypeDecl(p):
    '''TypeDecl : TYPE TypeSpecTopList
    '''
    parsed.append(p.slice)

def p_TypeSpecTopList(p):
    '''TypeSpecTopList : TypeSpec
                 | LROUND TypeSpecList  RROUND
    '''
    parsed.append(p.slice)

def p_TypeSpecList(p):
    '''TypeSpecList : empty
                 | TypeSpecList TypeSpec SEMICOLON
    '''
    parsed.append(p.slice)

def p_TypeSpec(p):
    '''TypeSpec : AliasDecl
                 | TypeDef
    '''
    parsed.append(p.slice)

def p_AliasDecl(p):
    '''AliasDecl : IDENTIFIER EQ Type
                 | IDENTIFIER EQ IDENTIFIER DOT IDENTIFIER
                 | IDENTIFIER EQ IDENTIFIER
    '''
    parsed.append(p.slice)

def p_TypeDef(p):
    '''TypeDef : IDENTIFIER Type
                 | IDENTIFIER IDENTIFIER
                 | IDENTIFIER IDENTIFIER DOT IDENTIFIER
    '''
    parsed.append(p.slice)

def p_Type(p):
    '''Type :  TypeLit
                 | LROUND IDENTIFIER RROUND
                 | LROUND Type RROUND
                 | LROUND IDENTIFIER DOT IDENTIFIER RROUND
    '''
    parsed.append(p.slice)

# def p_TypeName(p):
#     '''TypeName  : IDENTIFIER DOT IDENTIFIER
#     '''
#     parsed.append(p.slice)

# def p_QualifiedIdent(p):
#     '''QualifiedIdent : IDENTIFIER DOT IDENTIFIER
#     '''
#     parsed.append(p.slice)

def p_TypeLit(p):
    '''TypeLit : ArrayType
                 | StructType
                 | FunctionType
    '''
    parsed.append(p.slice)

def p_ArrayType(p):
    '''ArrayType : LSQUARE ArrayLength RSQUARE Type
                 | LSQUARE ArrayLength RSQUARE IDENTIFIER
                 | LSQUARE ArrayLength RSQUARE IDENTIFIER DOT IDENTIFIER
    '''
    parsed.append(p.slice)

def p_ArrayLength(p):
    '''ArrayLength : Expression
    '''
    parsed.append(p.slice)

def p_StructType(p):
    '''StructType : STRUCT LCURLY FieldDeclList RCURLY
    '''
    parsed.append(p.slice)

def p_FieldDeclList(p):
    '''FieldDeclList : empty
                 | FieldDeclList FieldDecl SEMICOLON
    '''
    parsed.append(p.slice)

def p_FieldDecl(p):
    '''FieldDecl : IdentifierList Type TagTop
                 | IdentifierList IDENTIFIER TagTop
                 | IDENTIFIER IDENTIFIER
                 | IdentifierList IDENTIFIER DOT IDENTIFIER TagTop
                 | STAR IDENTIFIER DOT IDENTIFIER TagTop
                 | IDENTIFIER DOT IDENTIFIER TagTop
                 | STAR IDENTIFIER TagTop
                 | IDENTIFIER TagTop
    '''
    parsed.append(p.slice)

def p_TagTop(p):
    '''TagTop : empty
                 | Tag
    '''
    parsed.append(p.slice)

def p_Tag(p):
    '''Tag : string_lit
    '''
    parsed.append(p.slice)

def p_FunctionType(p):
    '''FunctionType : FUNC Signature
    '''
    parsed.append(p.slice)

# Signature      = Parameters [ Result ] .
# Result         = Parameters | Type .
# Parameters     = "(" [ ParameterList [ "," ] ] ")" .
# ParameterList  = ParameterDecl { "," ParameterDecl } .
# ParameterDecl  = [ IdentifierList ] [ "..." ] Type .

def p_Signature(p):
    '''Signature : Parameters
                 | Parameters Result
    '''
    parsed.append(p.slice)

def p_Result(p):
    '''Result : Parameters
                 | Type
                 | IDENTIFIER
                 | IDENTIFIER DOT IDENTIFIER
    '''
    parsed.append(p.slice)

def p_Parameters(p):
    '''Parameters : LROUND RROUND
                 | LROUND ParameterList RROUND
                 | LROUND ParameterList COMMA RROUND

    '''
    parsed.append(p.slice)

def p_ParameterList(p):
    '''ParameterList  : ParameterDecl
                 | ParameterList COMMA ParameterDecl

    '''
    parsed.append(p.slice)

def p_ParameterDecl(p):
    '''ParameterDecl  : DDD Type
                 | IdentifierList Type
                 | IdentifierList DDD Type
                 | IDENTIFIER Type
                 | IDENTIFIER DDD Type
                 | DDD IDENTIFIER
                 | IdentifierList IDENTIFIER
                 | IdentifierList DDD IDENTIFIER
                 | IDENTIFIER IDENTIFIER
                 | IDENTIFIER DDD IDENTIFIER
                 | DDD IDENTIFIER DOT IDENTIFIER
                 | IdentifierList IDENTIFIER DOT IDENTIFIER
                 | IdentifierList DDD IDENTIFIER DOT IDENTIFIER
                 | IDENTIFIER IDENTIFIER DOT IDENTIFIER
                 | IDENTIFIER DDD IDENTIFIER DOT IDENTIFIER
    '''
    parsed.append(p.slice)

def p_VarDecl(p):
    '''VarDecl : VAR VarSpecTopList
    '''
    parsed.append(p.slice)

def p_VarSpecTopList(p):
    '''VarSpecTopList : VarSpec
                 | LROUND VarSpecList RROUND
    '''
    parsed.append(p.slice)

def p_VarSpecList(p):
    '''VarSpecList : empty
                 | VarSpecList VarSpec SEMICOLON
    '''
    parsed.append(p.slice)

def p_VarSpec(p):
    '''VarSpec : IdentifierList Type VarSpecMid
                | IDENTIFIER Type VarSpecMid
                | IdentifierList IDENTIFIER VarSpecMid
                | IDENTIFIER IDENTIFIER VarSpecMid
                | IdentifierList IDENTIFIER DOT IDENTIFIER VarSpecMid
                | IDENTIFIER IDENTIFIER DOT IDENTIFIER VarSpecMid
                | IdentifierList EQ ExpressionList
                | IDENTIFIER EQ ExpressionList
                | IdentifierList EQ Expression
                | IDENTIFIER EQ Expression
    '''
    parsed.append(p.slice)

def p_VarSpecMid(p):
    '''VarSpecMid : empty
                 | EQ ExpressionList
                 | EQ Expression
    '''
    parsed.append(p.slice)

def p_FunctionDecl(p):
    '''FunctionDecl : FUNC FunctionName FunctionDeclTail
    '''
    parsed.append(p.slice)

def p_FunctionDeclTail(p):
    '''FunctionDeclTail : Function
                 | Signature
    '''
    parsed.append(p.slice)

def p_FunctionName(p):
    '''FunctionName : IDENTIFIER
    '''
    parsed.append(p.slice)

def p_Function(p):
    '''Function : Signature FunctionBody
    '''
    parsed.append(p.slice)

def p_FunctionBody(p):
    '''FunctionBody : Block
    '''
    parsed.append(p.slice)

def p_SimpleStmt(p):
    '''SimpleStmt : Expression
                 | Assignment
                 | ShortVarDecl
                 | IncDecStmt
    '''
    p[0] = p[1]
    p[0].name = 'SimpleStmt'
    return
    # parsed.append(p.slice)

# def p_ExpressionStmt(p):
#     '''ExpressionStmt : Expression
#     '''
#     parsed.append(p.slice)

def p_IncDecStmt(p):
    '''IncDecStmt : Expression PLUS_PLUS
                | Expression MINUS_MINUS
    '''
    one_val = TreeNode('decimal_lit', 1, 'INT', 0, [])
    if p[1].isLvalue == 1:
        if p[2] == '++':
            ThreeAddrCode.add_line([ThreeAddrCode.length() + 1, '+', p[1].data, p[1].data, one_val.data])
        else:
            ThreeAddrCode.add_line([ThreeAddrCode.length() + 1, '-', p[1].data, p[1].data, one_val.data])
    else:
        print "*** Error: Lvalue required! ***"
    p[0] = p[1]
    p[0].name = 'IncDecStmt'
    return
    # parsed.append(p.slice)

def p_ShortVarDecl(p):
    '''ShortVarDecl : ExpressionList ASSIGN_OP ExpressionList
                 | Expression ASSIGN_OP Expression
    '''
    # TODO: Add in symbol table
    p[0] = TreeNode('ShortVarDecl', 0, 'INT', 0, [])
    if p[1].name == 'ExpressionList':
        l1 = len(p[1].children)
        l2 = len(p[3].children)
        if l1 == l2:
            for i in range(l1):
                ThreeAddrCode.add_line([ThreeAddrCode.length() + 1, p[2], p[1].children[i].data, p[3].children[i].data, ''])
        else:
            print "*** Error: Assignment mismatch:", l1, "identifier(s) but", l2, "value(s)! ***"
    elif p[1].name == 'Expression':
        ThreeAddrCode.add_line([ThreeAddrCode.length() + 1, p[2], p[1].data, p[3].data, ''])
    return

def p_Assignment(p):
    '''Assignment : ExpressionList assign_op ExpressionList
                | Expression assign_op Expression
    '''
    p[0] = TreeNode('Assignment', 0, 'INT', 0, [])
    if p[1].name == 'ExpressionList':
        l1 = len(p[1].children)
        l2 = len(p[3].children)
        if l1 == l2:
            for i in range(l1):
                ThreeAddrCode.add_line([ThreeAddrCode.length() + 1, p[2].data, p[1].children[i].data, p[3].children[i].data, ''])
        else:
            print "*** Error: Assignment mismatch:", l1, "identifier(s) but", l2, "value(s)! ***"
    elif p[1].name == 'Expression':
        ThreeAddrCode.add_line([ThreeAddrCode.length() + 1, p[2].data, p[1].data, p[3].data, ''])
    return

def p_assign_op(p):
    '''assign_op : EQ
                 | PLUS_EQ
                 | MINUS_EQ
                 | OR_EQ
                 | CARET_EQ
                 | STAR_EQ
                 | DIVIDE_EQ
                 | MODULO_EQ
                 | LS_EQ
                 | RS_EQ
                 | AMP_EQ
                 | AND_OR_EQ
    '''
    p[0] = TreeNode('assign_op', p[1], 'OPERATOR', 0, [])
    return

def p_IfStmt(p):
    '''IfStmt : IF Expression Block elseBot
                 | IF SimpleStmt SEMICOLON  Expression Block elseBot
    '''
    parsed.append(p.slice)

def p_elseBot(p):
    '''elseBot : empty
                 | ELSE elseTail
    '''
    parsed.append(p.slice)

def p_elseTail(p):
    '''elseTail : IfStmt
                 | Block
    '''
    parsed.append(p.slice)

def p_SwitchStmt(p):
    '''SwitchStmt : ExprSwitchStmt
    '''
    parsed.append(p.slice)

def p_ExprSwitchStmt(p):
    '''ExprSwitchStmt : SWITCH SimpleStmt SEMICOLON  ExpressionBot LCURLY ExprCaseClauseList RCURLY
                 | SWITCH ExpressionBot LCURLY ExprCaseClauseList RCURLY
    '''
    parsed.append(p.slice)

def p_ExprCaseClauseList(p):
    '''ExprCaseClauseList : empty
                 | ExprCaseClauseList ExprCaseClause
    '''
    parsed.append(p.slice)

def p_ExprCaseClause(p):
    '''ExprCaseClause : ExprSwitchCase COLON StatementList
    '''
    parsed.append(p.slice)

def p_ExprSwitchCase(p):
    '''ExprSwitchCase : CASE ExpressionList
                 | DEFAULT
                 | CASE Expression
    '''
    parsed.append(p.slice)

def p_ForStmt(p):
    '''ForStmt : FOR ExpressionBot Block
    '''
    parsed.append(p.slice)

def p_ExpressionBot(p):
    '''ExpressionBot : empty
                 | Expression
    '''
    parsed.append(p.slice)

def p_ReturnStmt(p):
    '''ReturnStmt : RETURN
                 | RETURN Expression
                 | RETURN ExpressionList
    '''
    parsed.append(p.slice)

def p_BreakStmt(p):
    '''BreakStmt : BREAK IDENTIFIER
    '''
    parsed.append(p.slice)

def p_ContinueStmt(p):
    '''ContinueStmt : CONTINUE IDENTIFIER
    '''
    parsed.append(p.slice)

def p_GotoStmt(p):
    '''GotoStmt : GOTO IDENTIFIER
    '''
    parsed.append(p.slice)

def p_Expression(p):
    '''Expression : UnaryExpr
                 | Expression OR_OR Expression
                 | Expression AMP_AMP Expression
                 | Expression EQ_EQ Expression
                 | Expression NOT_EQ Expression
                 | Expression LT Expression
                 | Expression LT_EQ Expression
                 | Expression GT Expression
                 | Expression GT_EQ Expression
                 | Expression PLUS Expression
                 | Expression MINUS Expression
                 | Expression OR Expression
                 | Expression CARET Expression
                 | Expression STAR Expression
                 | Expression DIVIDE Expression
                 | Expression MODULO Expression
                 | Expression LS Expression
                 | Expression RS Expression
                 | Expression AMP Expression
                 | Expression AND_OR Expression
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = TreeNode('IDENTIFIER', temp_gen(), 'INT', 1, [])
        ThreeAddrCode.add_line([ThreeAddrCode.length() + 1, p[2], p[0].data, p[1].data, p[3].data])
    p[0].name = 'Expression'
    p[0].children = [p[0]]
    return

def p_UnaryExpr(p):
    '''UnaryExpr : PrimaryExpr
                 | unary_op UnaryExpr
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = TreeNode('IDENTIFIER', temp_gen(), 'INT', 1, [])
        ThreeAddrCode.add_line([ThreeAddrCode.length() + 1, p[1].data, p[0].data, p[2].data])
    p[0].name = 'UnaryExpr'
    return

def p_unary_op(p):
    '''unary_op : PLUS
                 | MINUS
                 | NOT
                 | CARET
                 | STAR
                 | AMP
                 | LT_MINUS
    '''
    p[0] = TreeNode('unary_op', p[1], 'OPERATOR', 0, [])
    return

def p_PrimaryExpr(p):
    '''PrimaryExpr : Operand
                 | IDENTIFIER
                 | PrimaryExpr Selector
                 | PrimaryExpr Index
                 | PrimaryExpr Arguments
    '''
    # print p.slice
    if len(p) == 2:
        if p.slice[1].type == 'IDENTIFIER':
            p[0] = TreeNode('IDENTIFIER', p[1], 'INT', 1, [])
        elif p[1].name == 'Operand':
            p[0] = p[1]
    elif len(p) == 3:
        p[0]
        # TODO
    p[0].name = 'PrimaryExpr'
    return

def p_Operand(p):
    '''Operand  : Literal
                 | LROUND Expression RROUND
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]
    p[0].name = 'Operand'
    return

def p_Literal(p):
    '''Literal  : BasicLit
                 | FunctionLit
    '''
    if p[1].name == 'BasicLit':
        p[0] = p[1]
    elif p[1].name == 'FunctionLit':
        p[0]
        # TODO: FunctionLit
    p[0].name = 'Literal'
    return

def p_BasicLit(p):
    '''BasicLit : int_lit
                 | float_lit
                 | string_lit
    '''
    p[0] = p[1]
    p[0].name = 'BasicLit'
    return

def p_int_lit(p):
    '''int_lit : decimal_lit
                 | octal_lit
                 | hex_lit
    '''
    p[0] = p[1]
    p[0].name = 'int_lit'
    return

def p_decimal_lit(p):
    '''decimal_lit : DECIMAL_LIT
    '''
    p[0] = TreeNode('decimal_lit', p[1], 'INT', 0, [])
    return

def p_octal_lit(p):
    '''octal_lit : OCTAL_LIT
    '''
    p[0] = TreeNode('octal_lit', p[1], 'OCT', 0, [])
    return

def p_hex_lit(p):
    '''hex_lit  : HEX_LIT
    '''
    p[0] = TreeNode('hex_lit', p[1], 'HEX', 0, [])
    return

def p_float_lit(p):
    '''float_lit : FLOAT_LIT
    '''
    p[0] = TreeNode('float_lit', p[1], 'FLOAT', 0, [])
    return

def p_FunctionLit(p):
    '''FunctionLit : FUNC Function
    '''
    parsed.append(p.slice)

def p_Selector(p):
    '''Selector : DOT IDENTIFIER
    '''
    parsed.append(p.slice)

def p_Index(p):
    '''Index : LSQUARE Expression RSQUARE
    '''
    parsed.append(p.slice)

def p_Arguments(p):
    '''Arguments : LROUND RROUND
                 | LROUND ExpressionList DDD RROUND
                 | LROUND Expression DDD RROUND
                 | LROUND ExpressionList RROUND
                 | LROUND Expression RROUND
                 | LROUND Type DDD RROUND
                 | LROUND Type RROUND
                 | LROUND Type COMMA ExpressionList  DDD RROUND
                 | LROUND Type COMMA ExpressionList  RROUND
                 | LROUND Type COMMA Expression DDD RROUND
                 | LROUND Type COMMA Expression RROUND
                 | LROUND IDENTIFIER DDD RROUND
                 | LROUND IDENTIFIER RROUND %prec LROUND
                 | LROUND IDENTIFIER COMMA ExpressionList  DDD RROUND
                 | LROUND IDENTIFIER COMMA ExpressionList  RROUND
                 | LROUND IDENTIFIER COMMA Expression DDD RROUND
                 | LROUND IDENTIFIER COMMA Expression RROUND
                 | LROUND IDENTIFIER DOT IDENTIFIER DDD RROUND
                 | LROUND IDENTIFIER DOT IDENTIFIER RROUND
                 | LROUND IDENTIFIER DOT IDENTIFIER COMMA ExpressionList  DDD RROUND
                 | LROUND IDENTIFIER DOT IDENTIFIER COMMA ExpressionList  RROUND
                 | LROUND IDENTIFIER DOT IDENTIFIER COMMA Expression DDD RROUND
                 | LROUND IDENTIFIER DOT IDENTIFIER COMMA Expression RROUND
                 | LROUND ExpressionList DDD COMMA RROUND
                 | LROUND Expression DDD COMMA RROUND
                 | LROUND ExpressionList COMMA RROUND
                 | LROUND Expression COMMA RROUND
                 | LROUND Type DDD COMMA RROUND
                 | LROUND Type COMMA RROUND
                 | LROUND Type COMMA ExpressionList  DDD COMMA RROUND
                 | LROUND Type COMMA ExpressionList  COMMA RROUND
                 | LROUND Type COMMA Expression DDD COMMA RROUND
                 | LROUND Type COMMA Expression COMMA RROUND
                 | LROUND IDENTIFIER DDD COMMA RROUND
                 | LROUND IDENTIFIER COMMA RROUND
                 | LROUND IDENTIFIER COMMA ExpressionList  DDD COMMA RROUND
                 | LROUND IDENTIFIER COMMA ExpressionList  COMMA RROUND
                 | LROUND IDENTIFIER COMMA Expression DDD COMMA RROUND
                 | LROUND IDENTIFIER COMMA Expression COMMA RROUND
                 | LROUND IDENTIFIER DOT IDENTIFIER DDD COMMA RROUND
                 | LROUND IDENTIFIER DOT IDENTIFIER COMMA RROUND
                 | LROUND IDENTIFIER DOT IDENTIFIER COMMA ExpressionList  DDD COMMA RROUND
                 | LROUND IDENTIFIER DOT IDENTIFIER COMMA ExpressionList  COMMA RROUND
                 | LROUND IDENTIFIER DOT IDENTIFIER COMMA Expression DDD COMMA RROUND
                 | LROUND IDENTIFIER DOT IDENTIFIER COMMA Expression COMMA RROUND
    '''
    parsed.append(p.slice)

def p_error(p):
    if p == None:
        print str(sys.argv[1]) + " :: You missed something at the end"
    else:
        print str(sys.argv[1]) + " :: Syntax error in line no " +  str(p.lineno)

def p_empty(p):
    'empty :'
    pass

def p_string_lit(p):
    '''string_lit : STRING_LIT
    '''
    p[0] = TreeNode('string_lit', p[1], 'STRING', 0, [])
    return

logging.basicConfig(
    level = logging.DEBUG,
    filename = "parselog.txt",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)

log = logging.getLogger()

yacc.yacc(debug=True, debuglog=log)
filename = sys.argv[1]

inp = open(filename, 'r')
inp = inp.read()
inp += "\n"

yacc.parse(inp, debug=log)

ThreeAddrCode.print_code()

