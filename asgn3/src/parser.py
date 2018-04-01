#!/usr/bin/python
import ply.lex as lex
import sys
import ply.yacc as yacc
from lexer import tokens
import lexer
import logging

non_terminal=[]
output=[]
countg = 0
parsed=[]
final_output=[]

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
                | MethodDecl
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
    parsed.append(p.slice)

def p_IdentifierBotList(p):
    '''IdentifierBotList : COMMA IDENTIFIER
                 | IdentifierBotList COMMA IDENTIFIER
    '''
    parsed.append(p.slice)

def p_ExpressionList(p):
    '''ExpressionList : Expression ExpressionBotList
    '''
    parsed.append(p.slice)

def p_ExpressionBotList(p):
    '''ExpressionBotList : COMMA Expression
                 | COMMA Expression ExpressionBotList
    '''
    parsed.append(p.slice)


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

def p_MethodDecl(p):
    '''MethodDecl : FUNC Receiver IDENTIFIER FunctionDeclTail
    '''
    parsed.append(p.slice)

def p_Receiver(p):
    '''Receiver : Parameters
    '''
    parsed.append(p.slice)

def p_SimpleStmt(p):
    '''SimpleStmt : Expression
                 | Assignment
                 | ShortVarDecl
                 | IncDecStmt
    '''
    parsed.append(p.slice)

# def p_ExpressionStmt(p):
#     '''ExpressionStmt : Expression
#     '''
#     parsed.append(p.slice)

def p_IncDecStmt(p):
    '''IncDecStmt : Expression PLUS_PLUS
    			 | Expression MINUS_MINUS
    '''
    parsed.append(p.slice)


def p_ShortVarDecl(p):
    '''ShortVarDecl : IdentifierList ASSIGN_OP ExpressionList
                 | IdentifierList ASSIGN_OP Expression
                 | IDENTIFIER ASSIGN_OP ExpressionList
                 | IDENTIFIER ASSIGN_OP Expression
    '''
    parsed.append(p.slice)

def p_Assignment(p):
    '''Assignment : Expression assign_op Expression
                 | ExpressionList assign_op Expression
                 | Expression assign_op ExpressionList
                 | ExpressionList assign_op ExpressionList
    '''
    parsed.append(p.slice)

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
    parsed.append(p.slice)

# def p_add_op(p):
#     '''add_op : PLUS
#                  | MINUS
#                  | OR
#                  | CARET
#     '''
#     parsed.append(p.slice)

# def p_mul_op(p):
#     '''mul_op  : STAR
#                  | DIVIDE
#                  | MODULO
#                  | LS
#                  | RS
#                  | AMP
#                  | AND_OR
#     '''
#     parsed.append(p.slice)

# def p_addmul_op(p):
#     '''addmul_op : empty
#                  | add_op
#                  | mul_op
#     '''
#     parsed.append(p.slice)

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
    '''ReturnStmt : RETURN ExpressionListBot
                 | RETURN Expression
    '''
    parsed.append(p.slice)

def p_ExpressionListBot(p):
    '''ExpressionListBot : empty
                 | ExpressionList
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
    parsed.append(p.slice)

def p_UnaryExpr(p):
    '''UnaryExpr : PrimaryExpr
                 | unary_op UnaryExpr
    '''
    parsed.append(p.slice)

# def p_binary_op(p):
#     '''binary_op  : OR_OR
#                  | AMP_AMP
#                  | rel_op
#                  | add_op
#                  | mul_op
#     '''
#     parsed.append(p.slice)

# def p_rel_op(p):
#     '''rel_op : EQ_EQ
#                  | NOT_EQ
#                  | LT
#                  | LT_EQ
#                  | GT
#                  | GT_EQ
#     '''
#     parsed.append(p.slice)

def p_unary_op(p):
    '''unary_op   : PLUS
                 | MINUS
                 | NOT
                 | CARET
                 | STAR
                 | AMP
                 | LT_MINUS
    '''
    parsed.append(p.slice)

def p_PrimaryExpr(p):
    '''PrimaryExpr : Operand
                 | IDENTIFIER
                 | PrimaryExpr Selector
                 | PrimaryExpr Index
                 | PrimaryExpr Arguments
    '''
    parsed.append(p.slice)

def p_Operand(p):
    '''Operand  : Literal
                 | MethodExpr
                 | LROUND Expression RROUND
    '''
    parsed.append(p.slice)

def p_Literal(p):
    '''Literal  : BasicLit
                 | FunctionLit
    '''
    parsed.append(p.slice)

def p_BasicLit(p):
    '''BasicLit : int_lit
                 | float_lit
                 | string_lit
    '''
    parsed.append(p.slice)

def p_int_lit(p):
    '''int_lit : decimal_lit
                 | octal_lit
                 | hex_lit
    '''
    parsed.append(p.slice)

def p_decimal_lit(p):
    '''decimal_lit : DECIMAL_LIT
    '''
    parsed.append(p.slice)

def p_octal_lit(p):
    '''octal_lit  : OCTAL_LIT
    '''
    parsed.append(p.slice)

def p_hex_lit(p):
    '''hex_lit  : HEX_LIT
    '''
    parsed.append(p.slice)

def p_float_lit(p):
    '''float_lit : FLOAT_LIT
    '''
    parsed.append(p.slice)
##########################################
###################################

def p_FunctionLit(p):
    '''FunctionLit : FUNC Function
    '''
    parsed.append(p.slice)

def p_MethodExpr(p):
    '''MethodExpr : ReceiverType DOT IDENTIFIER   %prec IDENTIFIER
                 | IDENTIFIER DOT IDENTIFIER        %prec IDENTIFIER
                 | IDENTIFIER DOT IDENTIFIER DOT IDENTIFIER
    '''
    parsed.append(p.slice)

def p_ReceiverType(p):
    '''ReceiverType  : LROUND STAR IDENTIFIER DOT IDENTIFIER RROUND
                 | LROUND STAR IDENTIFIER RROUND
                 | LROUND ReceiverType RROUND
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
        print str(sys.argv[1])+" ::You missed something at the end"
    else:
        print str(sys.argv[1])+" :: Syntax error in line no " +  str(p.lineno)


def p_empty(p):
    'empty :'
    pass

def p_string_lit(p):
    '''string_lit : STRING_LIT
    '''
    parsed.append(p.slice)



#########

# The function rightderivation has been taken from an open source github repo

#########


def rightderivation(prefx,sufx):
    global final_output
    global countg
    lcount=countg
    count=0
    last=[]
    for i in range(1,len(output[lcount])):
        if not (output[lcount][i] in non_terminal):
            count+=1
        else:
            last.append(i)
    pre=" "
    for i in range(1,len(output[lcount])):
        if(last != [] and i==last[-1]):
            pre=pre+" <u> "+str(valuate(lcount,i))  +" </u> "
        else:
            pre=pre+str(valuate(lcount,i)) +  " "
    if(count==len(output[lcount])-1):
        countg+=1
        return pre
    del last[-1]
    final_output.append(computestr(prefx)+" " + pre+" " +sufx)
    suf=" "
    for x in range(len(output[lcount])-1,0,-1):
        if not (output[lcount][x] in non_terminal):
            suf = valuate(lcount,x)+suf
            continue
        las =-1
        if(num_of_non_terminals_in_line(countg+1)==0 and last==[]):
            for i in range(len(prefx)-1,-1,-1):
                if prefx[i] in non_terminal:
                    las=i
                    break
            pre=" "
            for i in range(len(prefx)):
                if(i==las):
                    pre=pre+" <u> "+str(prefx[i])  +" </u> "
                elif prefx[i] in non_terminal:
                    pre=pre+str(prefx[i]) +  " "
                else:
                    pre=pre+str(prefx[i].value)+  " "
            flag=0
        else:
            pre=computestr(prefx)
            flag=1

        for i in range(1,x):
            if(flag ==1 and last != [] and i==last[-1] ):
                pre=pre+" <u> "+str(valuate(lcount,i))  +" </u> "
            else:
                pre=pre+str(valuate(lcount,i))+" "
        countg+=1
        suf = str(rightderivation(prefx+output[lcount][1:x],suf+sufx)) +" " + suf
        countg-=1
        final_output.append(pre+" " +suf+" " +sufx)
        if (last != []):
            del last[-1]
    countg+=1
    return suf

def computestr(lis):
    stri=" "
    for i in range(len(lis)):
        if lis[i] in non_terminal:
            stri=stri+str(lis[i]) +  " "
        else:
            stri=stri+str(lis[i].value)+  " "
    return stri

def valuate(line,x):
    if output[line][x] in non_terminal:
        return output[line][x]
    else:
        return output[line][x].value

def num_of_non_terminals_in_line(line):
    non_terminal_count = 0
    for i in range(1, len(output[line])):
        if output[line][i] in non_terminal:
            non_terminal_count += 1
    return non_terminal_count

def trim_html(output):
    i = 0
    while i < len(output) - 1:
        if (similar(output[i], output[i+1])):
            del output[i+1]
        else:
            i += 1
    return output

def reduce(xs):
    i = 0
    x1 = ""
    while i < len(xs):
        if xs[i] == ' ':
            i += 1
        elif (i+3) <= len(xs) and xs[i:i+3] == '<u>':
            i += 3
        elif (i+4) <= len(xs) and xs[i:i+4] == '</u>':
            i += 4
        else:
            x1 += xs[i]
            i += 1
    return x1

def similar(xs, ys):
    return reduce(xs) == reduce(ys)

yacc.yacc()

filename = sys.argv[1]

inp = open(filename, 'r')
inp = inp.read()
inp += "\n"

yacc.parse(inp)

# print parsed
html_filename = filename[filename.rfind('/')+1:filename.rfind('.')] + ".html"

for i in range(len(parsed)):
    non_terminal.append(parsed[i][0])

for i in range(len(parsed) - 1, -1, -1):
    output.append(parsed[i])

# print output
for i in range(len(output)):
    print output[i]

import sys
sys.stdout = open(html_filename, 'w')

print "<html> <head> <title> CS335A - PyGM </title> </head> <uody>"
print "<h1> PyGM - GoLang to MIPS Compiler in Python </h1>"
print "<h4> Rightmost derivation </h4>"
print "<u style = color:blue> "+ str(output[0][0])+"</u> "+ "</br>"

rightderivation([], "")
final_output = trim_html(final_output)

for line in final_output:
    i = 0
    to_print = ""
    while i < len(line):
        if (i+3) <= len(line) and line[i:i+3] == '<u>':
            to_print += "<u style = font-size:18px> "
            i += 3
        else:
            to_print += line[i]
            i += 1
    print to_print + "</br>"
print "</body></html>"
