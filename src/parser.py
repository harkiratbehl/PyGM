#!/usr/bin/python

# DEFINITIONS

import sys
import ply.lex as lex
import ply.yacc as yacc

from lexer import tokens


#################################################################################
##################################### RULES #####################################
#################################################################################

def p_SourceFile(p):
    '''SourceFile : PackageClause SEMICOLON ImportDeclList TopLevelDeclList 
    '''
    parsed.append(p.slice)
    
def p_ImportDeclList(p):
    '''ImportDeclList : empty 
                | ImportDeclList ImportDecl SEMICOLON
    '''
    parsed.append(p.slice)

def p_TopLevelDeclList(p):
    '''TopLevelDeclList : empty 
                | TopLevelDeclList TopLevelDecl SEMICOLON 
    '''
    parsed.append(p.slice)

def p_PackageClause(p):
    '''PackageClause  : PACKAGE identifier  
    '''
    parsed.append(p.slice)

def p_TopLevelDecl(p):
    '''TopLevelDecl  : Declaration 
                | FunctionDecl 
                | MethodDecl 
    '''
    parsed.append(p.slice)

def p_ImportDecl(p):
    '''ImportDecl : IMPORT ImportSpecTopList 
    '''
    parsed.append(p.slice)

def p_ImportSpecTopList(p):
    '''ImportSpecTopList : ImportSpec 
                | LROUND ImportSpecList RROUND 
    '''
    parsed.append(p.slice)

def p_ImportSpecList(p):
    '''ImportSpecList : empty 
                | ImportSpecList ImportSpec SEMICOLON
    '''
    parsed.append(p.slice)

def p_ImportSpec(p):
    '''ImportSpec :  ImportSpecInit ImportPath 
    '''
    parsed.append(p.slice)

def p_ImportSpecInit(p):
    '''ImportSpecInit : empty
                 | DOT 
                 | identifier 
    '''
    parsed.append(p.slice)

def p_ImportPath(p):
    '''ImportPath : string_lit
    '''
    parsed.append(p.slice)


def p_Block(p):
    '''Block : LCURLY StatementList RCURLY
    '''
    parsed.append(p.slice)

def p_StatementList(p):
    '''StatementList : empty
                 | StatementList Statement SEMICOLON 
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
    '''
    parsed.append(p.slice)

def p_Declaration(p):
    '''Declaration  : ConstDecl 
                 | TypeDecl 
                 | VarDecl 
    '''
    parsed.append(p.slice)

def p_ConstDecl(p):
    '''ConstDecl : CONST ConstSpecTopList
    '''
    parsed.append(p.slice)

def p_ConstSpecTopList(p):
    '''ConstSpecTopList : ConstSpec 
                 | LROUND ConstSpecList RROUND
    '''
    parsed.append(p.slice)

def p_ConstSpecList(p):
    '''ConstSpecList : empty 
                 | ConstSpecList ConstSpec SEMICOLON
    '''
    parsed.append(p.slice)

def p_ConstSpec(p):
    '''ConstSpec : IdentifierList ConstSpecTail 
    '''
    parsed.append(p.slice)

def p_ConstSpecTail(p):
    '''ConstSpecTail : empty 
                 | TypeTop EQ ExpressionList 
    '''
    parsed.append(p.slice)

def p_TypeTop(p):
    '''TypeTop : empty 
                 | Type
    '''
    parsed.append(p.slice)
    
def p_IdentifierList(p):
    '''IdentifierList : identifier IdentifierBotList 
    '''
    parsed.append(p.slice)

def p_IdentifierBotList(p):
    '''IdentifierBotList : empty 
                 | IdentifierBotList COMMA identifier
    '''
    parsed.append(p.slice)

def p_ExpressionList(p):
    '''ExpressionList : Expression ExpressionBotList
    '''
    parsed.append(p.slice)

def p_ExpressionBotList(p):
    '''ExpressionBotList : empty 
                 | ExpressionBotList COMMA Expression
    '''
    parsed.append(p.slice)

def p_identifier(p):
    '''identifier : IDENTIFIER
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
    '''AliasDecl : identifier EQ Type
    '''
    parsed.append(p.slice)

def p_TypeDef(p):
    '''TypeDef : identifier Type
    '''
    parsed.append(p.slice)

def p_Type(p):
    '''Type : TypeName
                 | TypeLit
                 | LROUND Type RROUND
    '''
    parsed.append(p.slice)

def p_TypeName(p):
    '''TypeName  : identifier
                 | QualifiedIdent
    '''
    parsed.append(p.slice)

def p_QualifiedIdent(p):
    '''QualifiedIdent : identifier DOT identifier
    '''
    parsed.append(p.slice)

def p_TypeLit(p):
    '''TypeLit : ArrayType
                 | StructType 
                 | FunctionType 
    '''
    parsed.append(p.slice)

def p_ArrayType(p):
    '''ArrayType : LSQUARE ArrayLength RSQUARE ElementType 
    '''
    parsed.append(p.slice)

def p_ArrayLength(p):
    '''ArrayLength : Expression 
    '''
    parsed.append(p.slice)

def p_ElementType(p):
    '''ElementType : Type  
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
    '''FieldDecl : FieldDeclHead TagTop 
    '''
    parsed.append(p.slice)

def p_TagTop(p):
    '''TagTop : empty
                 | Tag
    '''
    parsed.append(p.slice)

def p_FieldDeclHead(p):
    '''FieldDeclHead : IdentifierList Type
                 | EmbeddedField
    '''
    parsed.append(p.slice)

def p_EmbeddedField(p):
    '''EmbeddedField : starTop TypeName
    '''
    parsed.append(p.slice)

def p_starTop(p):
    '''starTop : empty
                 | STAR
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

def p_Signature(p):
    '''Signature : Parameters ResultTop
    '''
    parsed.append(p.slice)


def p_ResultTop(p):
    '''ResultTop : empty 
                 | Result
    '''
    parsed.append(p.slice)

def p_Result(p):
    '''Result : Parameters
                 | Type
    '''
    parsed.append(p.slice)

def p_Parameters(p):
    '''Parameters : LROUND ParameterListTop RROUND
    '''
    parsed.append(p.slice)

def p_ParameterListTop(p):
    '''ParameterListTop : empty
                 | ParameterList commaTop
    '''
    parsed.append(p.slice)

def p_commaTop(p):
    '''commaTop : empty
                 | COMMA
    '''
    parsed.append(p.slice)

def p_ParameterList(p):
    '''ParameterList  : ParameterDecl ParameterDeclList
    '''
    parsed.append(p.slice)

def p_ParameterDeclList(p):
    '''ParameterDeclList : empty
                 | ParameterDeclList COMMA ParameterDecl
    '''
    parsed.append(p.slice)
    
def p_ParameterDecl(p):
    '''ParameterDecl  : ParameterDeclHead tripledotTop Type
    '''
    parsed.append(p.slice)


def p_tripledotTop(p):
    '''tripledotTop : empty
                 | DDD
    '''
    parsed.append(p.slice)

def p_ParameterDeclHead(p):
    '''ParameterDeclHead : empty
                 | IdentifierList 
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
    '''VarSpec : IdentifierList VarSpecTail
    '''
    parsed.append(p.slice)


def p_VarSpecTail(p):
    '''VarSpecTail : Type VarSpecMid
                 | EQ ExpressionList 
    '''
    parsed.append(p.slice)


def p_VarSpecMid(p):
    '''VarSpecMid : empty
                 | EQ ExpressionList
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
    '''FunctionName : identifier
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
    '''MethodDecl : FUNC Receiver MethodName FunctionDeclTail 
    '''
    parsed.append(p.slice)


def p_MethodName(p):
    '''MethodName : identifier 
    '''
    parsed.append(p.slice)

def p_Receiver(p):
    '''Receiver : Parameters
    '''
    parsed.append(p.slice)

def p_SimpleStmt(p):
    '''SimpleStmt : ExpressionStmt
                 | Assignment
                 | ShortVarDecl 
    '''
    parsed.append(p.slice)

def p_ExpressionStmt(p):
    '''ExpressionStmt : Expression 
    '''
    parsed.append(p.slice)
    
def p_ShortVarDecl(p):
    '''ShortVarDecl : IdentifierList ASSIGN_OP ExpressionList
    '''
    parsed.append(p.slice)

def p_Assignment(p):
    '''Assignment : ExpressionList assign_op ExpressionList 
    '''
    parsed.append(p.slice)

def p_assign_op(p):
    '''assign_op : addmul_op EQ
    '''
    parsed.append(p.slice)

def p_addmul_op(p):
    '''addmul_op : empty
                 | add_op
                 | mul_op  
    '''
    parsed.append(p.slice)

def p_IfStmt(p):
    '''IfStmt : IF SimpleStmtBot Expression Block elseBot 
    '''
    parsed.append(p.slice)

def p_SimpleStmtBot(p):
    '''SimpleStmtBot : empty
                 | SimpleStmt SEMICOLON 
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
    '''ExprSwitchStmt : SWITCH SimpleStmtBot ExpressionBot LCURLY ExprCaseClauseList RCURLY 
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
    '''
    parsed.append(p.slice)

def p_ExpressionListBot(p):
    '''ExpressionListBot : empty
                 | ExpressionList
    '''
    parsed.append(p.slice)

def p_Expression(p):
    '''Expression : UnaryExpr
                 | Expression binary_op Expression
    '''
    parsed.append(p.slice)

def p_UnaryExpr(p):
    '''UnaryExpr : PrimaryExpr
                 | unary_op UnaryExpr
    '''
    parsed.append(p.slice)

def p_binary_op(p):
    '''binary_op  : OR_OR
                 | AMP_AMP 
                 | rel_op 
                 | add_op 
                 | mul_op 
    '''
    parsed.append(p.slice)
    
def p_rel_op(p):
    '''rel_op : EQ_EQ 
                 | NOT_EQ 
                 | LT 
                 | LT_EQ 
                 | GT 
                 | GT_EQ 
    '''
    parsed.append(p.slice)

def p_add_op(p):
    '''add_op : PLUS 
                 | MINUS 
                 | OR 
                 | CARET
    '''
    parsed.append(p.slice)

def p_mul_op(p):
    '''mul_op  : STAR 
                 | DIVIDE 
                 | MODULO 
                 | LS 
                 | RS 
                 | AMP 
                 | AND_OR
    '''
    parsed.append(p.slice)

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
                 | PrimaryExpr Selector 
                 | PrimaryExpr Index 
                 | PrimaryExpr Arguments
    '''
    parsed.append(p.slice)

def p_Operand(p):
    '''Operand  : Literal
                 | OperandName 
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
def p_OperandName(p):
    '''OperandName : identifier 
    '''
    parsed.append(p.slice)

def p_FunctionLit(p):
    '''FunctionLit : FUNC Function
    '''
    parsed.append(p.slice)

def p_MethodExpr(p):
    '''MethodExpr : ReceiverType DOT MethodName
    '''
    parsed.append(p.slice)

def p_ReceiverType(p):
    '''ReceiverType  : TypeName
                 | LROUND STAR TypeName RROUND 
                 | LROUND ReceiverType RROUND
    '''
    parsed.append(p.slice)

def p_Selector(p):
    '''Selector : DOT identifier
    '''
    parsed.append(p.slice)

def p_Index(p):
    '''Index : LSQUARE Expression RSQUARE 
    '''
    parsed.append(p.slice)

def p_Arguments(p):
    '''Arguments : LROUND ArgumentsHead RROUND
    '''
    parsed.append(p.slice)

def p_ArgumentsHead(p):
    '''ArgumentsHead : empty
                 | ArgumentsHeadMid tripledotTop commaTop 
    '''
    parsed.append(p.slice)

def p_ArgumentsHeadMid(p):
    '''ArgumentsHeadMid : ExpressionList
                 | Type COMMA ExpressionList 
                 | Type
    '''
    parsed.append(p.slice)

def p_newline(p):
    '''newline : NEWLINE
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


# SUBROUTINES