#!/usr/bin/python
import ply.lex as lex
import ply.yacc as yacc
from lexer import tokens

from code import TreeNode
from code import ThreeAddressCode
from symboltable import SymbolTable
from symboltable import symboltable_node
import sys
from random import *
import logging

parsed=[]

ThreeAddrCode = ThreeAddressCode()
SymbolTable = SymbolTable()

def temp_gen():
    i = randint(0, sys.maxint)
    return 'temp_' + str(i)

def label_gen():
    i = randint(0, sys.maxint)
    return 'label_' + str(i)

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
    # TODO: Ignoring package name and Imports for now
    p[0] = p[5]
    p[0].print_node() 
    SymbolTable.print_symbol_table()
    return
    # parsed.append(p.slice)

def p_ImportDeclList(p):
    '''ImportDeclList : ImportDecl SEMICOLON ImportDeclList
                | empty
    '''
    # TODO: Ignoring Imports for now
    p[0]=p[1]
    return
    # parsed.append(p.slice)

def p_TopLevelDeclList(p):
    '''TopLevelDeclList : TopLevelDecl SEMICOLON TopLevelDeclList
                        | empty
    '''
    if len(p) == 4:
        if p[3] != None:
            p[0] = TreeNode('TopLevelDeclList', 0, 'INT', 0, [p[1]] + p[3].children, p[1].TAC)
            p[0].TAC.append_TAC(p[3].TAC)
        else:
            p[0] = TreeNode('TopLevelDeclList', 0, 'INT', 0, [p[1]], p[1].TAC)   
    return

def p_TopLevelDecl(p):
    '''TopLevelDecl  : Declaration
                    | FunctionDecl
    '''
    p[0]=p[1]
    # p[0].print_node()
    return

def p_ImportDecl(p):
    '''ImportDecl : IMPORT LROUND ImportSpecList RROUND
                    | IMPORT ImportSpec
    '''
    # TODO: Ignoring Imports for now
    return
    # parsed.append(p.slice)

def p_ImportSpecList(p):
    '''ImportSpecList : ImportSpec SEMICOLON ImportSpecList
                        | empty
    '''
    # TODO: Ignoring Imports for now
    return
    # parsed.append(p.slice)

def p_ImportSpec(p):
    '''ImportSpec :  DOT string_lit
                    | IDENTIFIER string_lit
                    | empty string_lit
    '''
    # TODO: Ignoring Imports for now
    return
    # parsed.append(p.slice)

def p_Block(p):
    '''Block : LCURLY StatementList RCURLY
    '''
    p[0] = p[2]
    p[0].name = 'Block'
    # p[0].print_node()
    return
    # parsed.append(p.slice)

def p_StatementList(p):
    '''StatementList : Statement SEMICOLON StatementList
                    | empty
    '''
    if len(p) == 4:
        p[0] = TreeNode('StatementList', 0, 'INT', 0, [p[1].data] + p[3].children, p[1].TAC)
        p[0].TAC.append_TAC(p[3].TAC)
    else:
        p[0] = TreeNode('StatementList', 0, 'INT')
    # p[0].print_node()

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
    p[0] = p[1]
    p[0].name = 'Statement'
    

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
    '''IdentifierList : IDENTIFIER COMMA IdentifierBotList
    '''
    p[0] = TreeNode('IdentifierList', 0, 'INT', 0, [p[1]] + p[3].children)
    return

def p_IdentifierBotList(p):
    '''IdentifierBotList : IDENTIFIER COMMA IdentifierBotList
                 | IDENTIFIER
    '''
    if len(p) == 2:
        p[0] = TreeNode('IdentifierBotList', p[1], 'INT')
        return
    elif len(p) == 4:
        p[0] = TreeNode('IdentifierBotList', 0, 'INT', 0, [p[1]] + p[3].children)
        return


def p_ExpressionList(p):
    '''ExpressionList : Expression COMMA ExpressionBotList
    '''
    p[0] = TreeNode('ExpressionList', 0, 'INT', [p[1].isLvalue] + p[3].isLvalue, [p[1]] + p[3].children, p[1].TAC)
    p[0].TAC.append_TAC(p[3].TAC)
    return

def p_ExpressionBotList(p):
    '''ExpressionBotList : Expression COMMA ExpressionBotList
                        | Expression
    '''
    if len(p) == 2:
        p[0] = TreeNode('ExpressionBotList', 0, 'INT', [p[1].isLvalue], [p[1]], p[1].TAC)
        return
    elif len(p) == 4:
        p[0] = TreeNode('ExpressionBotList', 0, 'INT', [p[1].isLvalue] + p[3].isLvalue, [p[1]] + p[3].children, p[1].TAC)
        p[0].TAC.append_TAC(p[3].TAC)
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

    p[0] = p[1]
    p[0].name = 'VarDecl'
    return
    parsed.append(p.slice)

def p_VarSpecTopList(p):
    '''VarSpecTopList : VarSpec
                 | LROUND VarSpecList RROUND
    '''

    if len(p) == 2:
        p[0] = p[1]
        p[0].name = 'VarSpecTopList'
    else:
        p[0] = p[2]
        ####TODO
    return


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

    # if len(p) == 4:
    #     if p[2].type == 'IDENTIFIER':
    #         #TODO
    #     else if p[2].type == 'EQ':
    #         #TODO
    #     else:
    #         if p[1].type == 'IDENTIFIER':

    #         else:
    #             #TODO
    # else:
    #     #TODO 
    parsed.append(p.slice)

def p_VarSpecMid(p):
    '''VarSpecMid : empty
                 | EQ ExpressionList
                 | EQ Expression
    '''
    parsed.append(p.slice)

def p_FunctionDecl(p):
    '''FunctionDecl : FUNC FunctionName Signature
                | FUNC FunctionName Signature FunctionBody
    '''
    p[0] = TreeNode('FunctionDecl', 0, 'INT')
    p[0].TAC.add_line(['func', p[2].data, '', ''])
    p[0].TAC.append_TAC(p[4].TAC)
    # p[0].print_node()
    return
    # p[2].print_node()
    # p[4].print_node()
    # parsed.append(p.slice)

def p_FunctionName(p):
    '''FunctionName : IDENTIFIER
    '''
    p[0] = TreeNode('FunctionName', p[1], 'INT')
    return

def p_FunctionBody(p):
    '''FunctionBody : Block
    '''
    p[0] = p[1]
    p[0].name = 'FunctionBody'
    return

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
    one_val = TreeNode('decimal_lit', 1, 'INT')
    p[0] = p[1]
    if p[1].isLvalue == 1:
        if p[2] == '++':
            p[0].TAC.add_line(['+', p[1].data, p[1].data, one_val.data])
        else:
            p[0].TAC.add_line(['-', p[1].data, p[1].data, one_val.data])
    else:
        print "*** Error: Lvalue required! ***"
    p[0].name = 'IncDecStmt'
    return

def p_ShortVarDecl(p):
    '''ShortVarDecl : ExpressionList ASSIGN_OP ExpressionList
                 | Expression ASSIGN_OP Expression
    '''
    # TODO: Add in symbol table
    p[0] = TreeNode('ShortVarDecl', 0, 'INT')
    if p[1].name == 'ExpressionList':
        l1 = len(p[1].children)
        l2 = len(p[3].children)
        if l1 == l2:
            for i in range(l1):
                if p[1].children[i].isLvalue == 0:
                    print "*** Error: Cannot assign to constant ***"   
                else: 
                    if SymbolTable.search_node(p[1].children[i].data) == 0:
                        node = symboltable_node()
                        node.name = p[1].children[i].data
                        node.type = 'INT'
                        SymbolTable.add_node(node)
                    p[0].TAC.add_line([p[2], p[1].children[i].data, p[3].children[i].data, ''])
        else:
            print "*** Error: Assignment mismatch:", l1, "identifier(s) but", l2, "value(s)! ***"

    elif p[1].name == 'Expression':
        if p[1].isLvalue == 0:
            print "*** Error: Cannot declare and assign to constant ***"
            return            
        else:
            p[0].TAC.append_TAC(p[3].TAC)
            p[0].TAC.append_TAC(p[1].TAC)
            p[0].TAC.add_line([p[2], p[1].data, p[3].data, ''])
            if SymbolTable.search_node(p[1].data) == 0:
                node = symboltable_node()
                node.name = p[1].data
                node.type = 'INT'
                SymbolTable.add_node(node)
            return


def p_Assignment(p):
    '''Assignment : ExpressionList assign_op ExpressionList
                | Expression assign_op Expression
    '''
    p[0] = TreeNode('Assignment', 0, 'INT')
    if p[1].name == 'ExpressionList':
        l1 = len(p[1].children)
        l2 = len(p[3].children)
        if l1 == l2:
            for i in range(l1):
                if p[1].children[i].isLvalue == 0:
                    print "*** Error: Cannot assign to constant ***"   
                else: 
                    if SymbolTable.search_node(p[1].children[i].data) == 0:
                        node = symboltable_node()
                        node.name = p[1].children[i].data
                        node.type = 'INT'
                        SymbolTable.add_node(node)
        
                    if SymbolTable.search_node(p[3].children[i].data) == 0 and p[3].children[i].isLvalue ==1:
                        node = symboltable_node()
                        node.name = p[3].children[i].data
                        node.type = 'INT'
                        SymbolTable.add_node(node)
                    p[0].TAC.add_line([p[2].data, p[1].children[i].data, p[3].children[i].data, ''])
        else:
            print "*** Error: Assignment mismatch:", l1, "identifier(s) but", l2, "value(s)! ***"

    elif p[1].name == 'Expression':
        # p[0] = TreeNode('Assignment', 0, 'INT', 0, p[1].children + p[3].children, p[1].TAC.append_TAC(p[3].TAC))
        if p[1].isLvalue == 0:
            print "*** Error: Cannot assign to constant ***"
            return            
        else:
            p[0].TAC.append_TAC(p[3].TAC)
            p[0].TAC.append_TAC(p[1].TAC)
            p[0].TAC.add_line([p[2].data, p[1].data, p[3].data, ''])
            if SymbolTable.search_node(p[1].data) == 0:# and p[1].children[i].isLvalue ==1:
                node = symboltable_node()
                node.name = p[1].data
                node.type = 'INT'
                SymbolTable.add_node(node)
            if SymbolTable.search_node(p[3].data) == 0 and p[3].isLvalue ==1:
                node = symboltable_node()
                node.name = p[3].data
                node.type = 'INT'
                SymbolTable.add_node(node)
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
    p[0] = TreeNode('assign_op', p[1], 'OPERATOR')
    return

def p_IfStmt(p):
    '''IfStmt : IF Expression Block
            | IF Expression Block ELSE elseTail
    '''
    if len(p) == 4:
        l1 = label_gen()
        p[0] = TreeNode('IfStmt', 0, 'INT')
        p[0].TAC.append_TAC(p[2].TAC)
        p[0].TAC.add_line(['ifgotoeq', p[2].data, 0, l1])
        p[0].TAC.append_TAC(p[3].TAC)
        p[0].TAC.add_line([l1])
    if len(p) == 6:
        l1 = label_gen()
        l2 = label_gen()
        p[0] = TreeNode('IfStmt', 0, 'INT')
        p[0].TAC.append_TAC(p[2].TAC)
        p[0].TAC.add_line(['ifgotoeq', p[2].data, 0, l1])
        p[0].TAC.append_TAC(p[3].TAC)
        p[0].TAC.add_line(['goto', l2])
        p[0].TAC.add_line([l1])
        p[0].TAC.append_TAC(p[5].TAC)
        p[0].TAC.add_line([l2])
    # p[0].print_node()
    return

def p_elseTail(p):
    '''elseTail : IfStmt
                 | Block
    '''
    p[0] = p[1]
    p[0].name = 'elseTail'
    return

def p_SwitchStmt(p):
    '''SwitchStmt : ExprSwitchStmt
    '''
    p[0] = TreeNode('SwitchStmt', 0, 'INT', 0, [], p[1].TAC)
    return

def p_ExprSwitchStmt(p):
    '''ExprSwitchStmt : SWITCH SimpleStmt SEMICOLON LCURLY ExprCaseClauseList RCURLY
                 | SWITCH SimpleStmt SEMICOLON Expression LCURLY ExprCaseClauseList RCURLY
                 | SWITCH LCURLY ExprCaseClauseList RCURLY
                 | SWITCH Expression LCURLY ExprCaseClauseList RCURLY
    '''
    if len(p) == 6:
        l1 = label_gen()
        l2 = label_gen()
        p[0] = TreeNode('ExprSwitchStmt', 0, 'INT')
        p[0].TAC.append_TAC(p[2].TAC)
        t1= temp_gen()
        p[0].TAC.add_line(['=', t1 , p[2].data, ''])
        p[0].TAC.append_TAC(p[4].data)
        for i in range(len(p[4].children)):
            p[0].TAC.add_line(['ifgotoeq', t1, p[4].children[i][0], p[4].children[i][1]])
        for i in range(p[4].TAC.length()):
            if i in p[4].TAC.leaders[1:]:
                p[0].TAC.add_line(['goto', l2, '', ''])
            p[0].TAC.add_line(p[4].TAC.code[i])
        p[0].TAC.add_line([l2])
    return

def p_ExprCaseClauseList(p):
    '''ExprCaseClauseList : empty
                 | ExprCaseClauseList ExprCaseClause
    '''
    TAC1 = ThreeAddressCode()
    TAC2 = ThreeAddressCode()
    if len(p) == 3:
        TAC1 = p[1].data
        TAC2 = p[2].data
        p[0] = TreeNode('ExprCaseClauseList', TAC1, 'INT', 0, p[1].children + p[2].children, p[1].TAC)
        p[0].TAC.add_leader(p[0].TAC.length())
        p[0].TAC.append_TAC(p[2].TAC)
        p[0].data.append_TAC(TAC2)

    else:
        p[0] = TreeNode('ExprCaseClauseList', TAC1, 'INT')

    return
    # parsed.append(p.slice)

def p_ExprCaseClause(p):
    '''ExprCaseClause : ExprSwitchCase COLON StatementList
    '''
    l1 = label_gen()
    p[0] = TreeNode('ExprCaseClause', 0, 'INT')
    # p[0].TAC.append_TAC(p[1].TAC)
    p[0].TAC.add_line([l1])
    # p[0].TAC.add_line(['ifgotoneq', p[1].children, p[1].children, l1])
    p[0].TAC.append_TAC(p[3].TAC)
    p[0].children = [[p[1].data,l1]]
    p[0].data = p[1].TAC
    return
    # parsed.append(p.slice)

def p_ExprSwitchCase(p):
    '''ExprSwitchCase : CASE ExpressionList
                 | DEFAULT
                 | CASE Expression
    '''
    p[0] = TreeNode('ExprSwitchCase', 0, 'INT')
    if len(p) == 3:
        p[0].data = p[2].data
        p[0].TAC = p[2].TAC

    parsed.append(p.slice)

def p_ForStmt(p):
    '''ForStmt : FOR Expression Block
                 | FOR Block
    '''
    p[0] = TreeNode('ForStmt', 0, 'INT')
    if len(p) == 4:
        l1 = label_gen()
        l2 = label_gen()
        p[0].TAC.add_line([l1])
        p[0].TAC.append_TAC(p[2].TAC)
        p[0].TAC.add_line(['ifgotoeq', p[2].data, 0, l2])
        p[0].TAC.append_TAC(p[3].TAC)
        p[0].TAC.add_line(['goto', l1])
        p[0].TAC.add_line([l2])

    if len(p) == 3:
        l1 = label_gen()
        # l2 = label_gen()
        p[0].TAC.add_line([l1])
        p[0].TAC.append_TAC(p[2].TAC)
        p[0].TAC.add_line(['goto', l1])
        # p[0].TAC.add_line([l2])
    return






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
        p[0].TAC.add_line([p[2], p[0].data, p[1].data, p[3].data])
    p[0].name = 'Expression'
    return

def p_UnaryExpr(p):
    '''UnaryExpr : PrimaryExpr
                 | unary_op UnaryExpr
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = TreeNode('IDENTIFIER', temp_gen(), 'INT', 1)
        p[0].TAC.add_line([p[1].data, p[0].data, p[2].data])
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
    p[0] = TreeNode('unary_op', p[1], 'OPERATOR')
    return

def p_PrimaryExpr(p):
    '''PrimaryExpr : Operand
                 | IDENTIFIER
                 | PrimaryExpr Selector
                 | PrimaryExpr Index
                 | PrimaryExpr Arguments
    '''
    if len(p) == 2:
        if p.slice[1].type == 'IDENTIFIER':
            p[0] = TreeNode('IDENTIFIER', p[1], 'INT', 1, [])
        elif p[1].name == 'Operand':
            p[0] = p[1]
    elif len(p) == 3:
        if p[2].name == 'Arguments':
            p[0] = p[1]
            p[0].TAC.add_line(['call', p[1].data, '', ''])
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
    p[0] = TreeNode('decimal_lit', p[1], 'INT')
    return

def p_octal_lit(p):
    '''octal_lit : OCTAL_LIT
    '''
    p[0] = TreeNode('octal_lit', p[1], 'OCT')
    return

def p_hex_lit(p):
    '''hex_lit  : HEX_LIT
    '''
    p[0] = TreeNode('hex_lit', p[1], 'HEX')
    return

def p_float_lit(p):
    '''float_lit : FLOAT_LIT
    '''
    p[0] = TreeNode('float_lit', p[1], 'FLOAT')
    return

def p_FunctionLit(p):
    '''FunctionLit : FUNC Signature FunctionBody
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
    if len(p) == 3:
        p[0] = TreeNode('Arguments', 0, 'INT')
    return

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
    p[0] = TreeNode('string_lit', p[1], 'STRING')
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

# ThreeAddrCode.print_code()

