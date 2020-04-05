#Toncho Tonchev  3168  cse53168    
#Christos Katsios  3002  cse53002

import sys
import os
line = 1
token = ''
word = ''
char = ''
f = open('testFile.txt','r')

keywords = {
    'program' : 'program_token',
    'declare' : 'declare_token',
    'if' : 'if_token',
    'else' : 'else_token',
    'while' : 'while_token',
    'doublewhile' : 'doublewhile_token',
    'loop' : 'loop_token',
    'exit' : 'exit_token',
    'forcase' : 'forcase_token',
    'incase' : 'incase_token',
    'when' : 'when_token',
    'default' : 'default_token',
    'not' : 'not_token',
    'and' : 'and_token',
    'or' : 'or_token',
    'function' : 'function_token',
    'procedure' : 'procedure_token',
    'call' : 'call_token',
    'return' : 'return_token',
    'in' : 'in_token',
    'inout' : 'inout_token',
    'input' : 'input_token',
    'print' : 'print_token',
    'then' : 'then_token'         }


symbols = ['+', '-', '*', '/', '<', '>', '=', '<=', '>=', '<>', ':=' , ';', ',', ':', '(', ')', '[', ']' , '/*', '*/', '//' ]

def lex():

    global line,token,char,word
    next = True
    state = 0
    word = ''
    comments = ''

    while next:
        char = f.read(1)


        if state == 0:
            if char.isspace():
                if(char == '\n'):
                    line += 1
                state = 0
                char = ''
            elif char.isalpha():
                state = 1
                token = 'id_token'
            elif char.isdigit():
                state = 2
                token = 'number_token'
            elif char == '>':
                state = 3
                token = 'greaterThan_token'
            elif char == '<':
                state = 4
                token = 'lessThan_token'
            elif char == ':':
                state = 5
                token = 'colon_token'
            elif char == '/':
                state = 6
                token = 'div_token'
            elif char == '+':
                next = False
                token = 'plus_token'
            elif char == '-':
                next = False
                token = 'minus_token'
            elif char == '*':
                next = False
                token = 'multiply_token'
            elif char == '=':
                next = False
                token = 'equal_token'
            elif char == ',':
                next = False
                token = 'comma_token'
            elif char == ';':
                next = False
                token = 'semicolon_token'
            elif char == ')':
                next = False
                token = 'rightParentheses_token'
            elif char == ']':
                next = False
                token = 'rightBracket_token'
            elif char == '}':
                next = False
                token = 'rightCurly_token'
            elif char == '(':
                next = False
                token = 'leftParentheses_token'
            elif char == '[':
                next = False
                token = 'leftBracket_token'
            elif char == '{':
                next = False
                token = 'leftCurly_token'
            elif not char:
                print("---------- End Of File ---------- lines : ",line)
                break
            else:
                print("SyntaxError : Unknown character:' %c ' \nLine %d :  "%( char, line))
                exit(1)
            word+=char
        elif state == 1:
            if(not char):
                next = False
            elif (not char.isalpha() and not char.isdigit()):
                    f.seek(f.tell() - 1)
                    next = False
            else:
                word+=char
        elif state == 2:
            if not char.isdigit():
                if char == '.':
                    print("Only Integers.")
                    exit(1)
                elif char.isalpha():
                    print("SyntaxError : Variables names cannot be started with number:%s.\nLine %d : "%(word+char ,line) )
                    exit(1)
                else:
                    next = False
                    f.seek(f.tell() - 1)
            else:
                word += char
                if(int(word) > 32767):
                    print("SyntaxError : Minimal does not support number bigger than 32767.\nLine ",line)
                    exit(1)
        elif state == 3:
            if char == '=':
                next = False
                token = 'greaterOrEqual_token'
                word += char
            elif (char.isalpha() or char.isdigit()):
                f.seek(f.tell() - 1)
                next = False
            else:
                print("SyntaxError : Unknown character:' %c ' \nLine %d :  "%( char, line))
                exit(1)
        elif state == 4:
            if char == '=':
                next = False
                token = 'lessOrEqual_token'
                word += char
            elif char == '>':
                next = False
                token = 'different_token'
                word += char
            elif (char.isalpha() or char.isdigit()):
                f.seek(f.tell() - 1)
                next = False
            else:
                print("SyntaxError : Unknown character:' %c ' \nLine %d :  "%( char, line))
                exit(1)
        elif state == 5:
            if char == '=':
                next = False
                token = 'assignment_token'
                word += char
            elif(char.isalpha() or char.isdigit()):
                f.seek(f.tell() - 1)
                next = False
        elif state == 6:
            if (char.isdigit() or char.isalpha()):
                next = False
                f.seek(f.tell() - 1)
            elif char == '/':
                token = 'commentLine_token'
                comments = ''
                while char != '\n':
                    char = f.read(1)
                    comments += char
                line += 1
                if('//' in comments or '/*' in comments or '*/' in comments):
                    print("Cant use '//' or '/*' or '*/' inside of comments.\nLine:",line-1)
                    exit(1)
                lex()
                return
            elif char =='*':
                token = 'commentBlock_token'
                comments ='' 
                startComment = line
                line += 1
                while ('*/' not in comments):
                    char = f.read(1)
                    comments += char
                    if char == '\n':
                        line += 1
                    if char =='' and '*/' not in comments:
                        print ("The commentsBlock never be closed in line :\nStart Comments from line:", startComment)
                        exit(1)
                if('//' in comments or '/*' in comments):
                    print("Cant use '//' or '/*' inside of comments.\nLine:",line-1)
                    exit(1)
                lex()
                return   
    #end While
    if word in keywords:
        token = keywords.get(word)
    print("word:",word)
    print("token:",token)
    print ("\n")
    return token,word



# ----------------------------------------------------------------------------------



# Syntaktikos Analutis
def program():
    global token,word,line
    if(token == 'program_token'):
        token,word = lex()
        if(token == 'id_token'):
            token,word = lex()
            if (token == 'leftCurly_token'):
                token,word = lex()
                block()
                if(token == 'rightCurly_token'):
                    print("successful compile program.")
                else:
                    print("SyntaxError :  '}' was expected in line : " , line)
                    exit(1)
            else:
                print("SyntaxError :  '{' was expected in line : " , line)
                exit(1)
        else:
            print("SyntaxError : Invalid name.\n line : " , line)
            exit(1)
    else:
        print("SyntaxError : Not found the word 'program' was expected in line : " , line)
        exit(1)



def block():
    declarations()
    subprograms()
    statements()



def declarations():
    global token,word,line
    while(token == 'declare_token'):
        token,word = lex()
        varlist()
        if(token == 'semicolon_token'):
            token,word = lex()
        else:
            print("SyntaxError :  ';' was expected in line : " , line)
            exit(1)

        

def subprograms():
    global token,word,line
    while(token == 'function_token' or token == 'procedure_token'):
        token,word = lex()
        subprogram()



def statements():
    global token,word,line
    if(token == 'leftCurly_token'):
        token,word == lex()
        statement()
        while (token == 'semicolon_token'):
            token,word == lex()
            statement()
        if(token == 'rightCurly_token'):
            token,word = lex()
        else:
            print("SyntaxError :  '}' was expected in line : " , line)
            exit(1)
    else:
        statement()  



def varlist():
    global token,word,line
    if(token == 'id_token'):
        token ,word = lex()
        while(token == 'comma_token'):
            token,word = lex()
            if(token == 'id_token' ):
                token,word = lex()
            else:
                print("SyntaxError :  'id' was expected in line : " , line)
                exit(1)



def subprogram():
    global token,word,line
    if(token == 'id_token'):
        token,word = lex()
        funcbody()
    else:
        print("SyntaxError :  'Wring function/procedure' name in line : " , line)
        exit(1)



def funcbody():
    global token,word,line
    formalpars()
    if(token == 'leftCurly_token'):
        token,word = lex() 
        block()
        if(token == 'rightCurly_token'):
            token,word = lex()
        else:
            print("SyntaxError :  '}' was expected in line : " , line)
            exit(1)
    else:
        print("SyntaxError :  '{' was expected in line : " , line)
        exit(1)



def formalpars():
    global token,word,line
    if(token == 'leftParentheses_token'):
        token,word = lex()
        formalparlist()
        if(token == 'rightParentheses_token'):
            token,word = lex()
        else:
            print("SyntaxError :  ')' was expected in line : " , line)
            exit(1)
    else:
        print("SyntaxError :  '(' was expected in line : " , line)
        exit(1)



def formalparlist():
    global token,word,line
    formalparitem()
    while(token == 'comma_token'):
        token,word = lex()
        formalparitem()


def formalparitem():
    global token,word,line
    if(token == 'in_token' or token == 'inout_token'):
        token,word = lex()
        if(token == 'id_token'):
            token,word = lex()
        else:
            print("SyntaxError : parameters was expected in line : " , line)
            exit(1)
    else:
        print("SyntaxError :  undeclere function/procedure parameters in line : " , line)
        exit(1)



def statement():
    global token,word,line
    if (token == 'id_token'):
        token,word = lex()
        assignment_stat()
    elif (token == 'if_token'):
        token,word = lex()
        if_stat()
    elif (token == 'while_token'):
        token,word = lex()
        while_stat()
    elif (token == 'doublewhile_token'):
        token,word = lex()
        doublewhile_stat()
    elif (token == 'loop_token'):
        token,word = lex()
        loop_stat()
    elif (token == 'exit_token'):
        token,word = lex()
        exit_stat()
    elif (token == 'forcase_token'):
        token,word = lex()
        forcase_stat()
    elif (token == 'incase_token'):
        token,word = lex()
        incase_stat()
    elif (token == 'call_token'):
        token,word = lex()
        call_stat()
    elif (token == 'return_token'):
        token,word = lex()
        return_stat()
    elif (token == 'input_token'):
        token,word = lex()
        input_stat()
    elif (token == 'print_token'):
        token,word = lex()
        print_stat()   



def assignment_stat():
    global token,word,line
    if(token == 'assignment_token'):
        token,word = lex()
        expression()
    else:
        print("SyntaxError :  expected  ':=' in line : " , line)
        exit(1)



def if_stat():
    global token,word,line
    if(token == 'leftParentheses_token'):
        token,word = lex()
        condition()
        if(token == 'rightParentheses_token'):
            token,word = lex()
            if(token == 'then_token'):
                token,word = lex()
                statements()
                elsepart()
            else:
                print("SyntaxError :  expected 'then' in line : " , line)
                exit(1)
        else:
            print("SyntaxError :  expected '(' in line : " , line)
            exit(1)
    else:
        print("SyntaxError :  expected  '(' in line : " , line)
        exit(1)



def elsepart():
    global token,word,line
    if( token == 'else_token'):
        token,word = lex()
        statements()
    return



def while_stat():
    global token,word,line
    if(token == 'leftParentheses_token'):
        token,word = lex()
        condition()
        if(token == 'rightParentheses_token'):
            token,word = lex()
            statements()
        else:
            print("SyntaxError :  expected  ')' in line : " , line)
            exit(1)
    else:
        print("SyntaxError :  expected  '(' in line : " , line)
        exit(1)



def doublewhile_stat():
    global token,word,line
    if(token == 'leftParentheses_token'):
        token,word = lex()
        condition()
        if(token == 'rightParentheses_token'):
            token,word = lex()
            statements()
            if(token == 'else_token'):
                token,word = lex()
                statements()
            else:
                print("SyntaxError :  expected  'else' in line : " , line)
                exit(1)
        else:
            print("SyntaxError :  expected  ')' in line : " , line)
            exit(1)
    else:
        print("SyntaxError :  expected  '(' in line : " , line)
        exit(1)
    return



def loop_stat():
    global token,word,line
    statements()



def exit_stat():
    global token,word,line



def forcase_stat():
    global token,word,line
    while(token == 'when_token'):
        token,word = lex()
        if(token == 'leftParentheses_token'):
            token,word = lex()
            condition()
            if(token == 'rightParentheses_token'):
                token,word = lex()
                if(token == 'colon_token'):
                    token,word = lex()
                    statements()
                else:
                    print("SyntaxError :  expected  ':' in line : " , line)
                    exit(1)
            else:
                print("SyntaxError :  expected  ')' in line : " , line)
                exit(1)
        else:
            print("SyntaxError :  expected  '(' in line : " , line)
            exit(1)
    if(token == 'default_token'):
        token,word = lex()
        if(token == 'colon_token'):
            token,word = lex()
            statements()
        else:
            print("SyntaxError :  expected  ':' in line : " , line)
            exit(1)
    else:
        print("SyntaxError :  expected  'dafault' in line : " , line)
        exit(1)
                    


def incase_stat():
    global token,word,line
    while(token == 'when_token'):
        token,word = lex()
        if( token == 'leftParentheses_token'):
            token,word = lex()
            condition()
            if(token ==  'rightParentheses_token'):
                token,word = lex()
                if(token == 'colon_token'):
                    token,word = lex()
                    statements()
                else:
                    print("SyntaxError :  expected  ':' in line : " , line)
                    exit(1)
            else:
                print("SyntaxError :  expected  ')' in line : " , line)
                exit(1)
        else:
            print("SyntaxError :  expected  '(' in line : " , line)
            exit(1)
    return



def call_stat():
    global token,word,line
    if(token == 'id_token'):
        token,word = lex()
        actualpars()
    else:
        print("SyntaxError :  expected  'id' parametar in line : " , line)
        exit(1)
    return



def return_stat():
    global token,word,line
    token,word = lex()
    expression()



def input_stat():
    global token,word,line
    if(token == 'leftParentheses_token'):
        token,word = lex()
        if(token == 'id_token'):
            token,word = lex()
            if(token == 'rightParentheses_token'):
                token,word = lex()
                return
            else:
                print("SyntaxError :  expected  ')' in line : " , line)
                exit(1)
        else:
            print("SyntaxError :  expected  'id' parametar in line : " , line)
            exit(1)
    else:
        print("SyntaxError :  expected  '(' in line : " , line)
        exit(1)



def print_stat():
    global token,word,line
    if(token == 'leftParentheses_token'):
        token,word = lex()
        expression()
        if(token == 'rightParentheses_token'):
            token,word = lex()
            return
        else:
            print("SyntaxError :  expected  ')' in line : " , line)
            exit(1)
    else:
        print("SyntaxError :  expected  '(' in line : " , line)
        exit(1)



def actualpars():
    global token,word,line
    if(token == 'leftParentheses_token'):
        token,word = lex()
        actualparlist()
        if(token == 'rightParentheses_token'):
            token,word = lex()
        else:
            print("SyntaxError :  expected ')01' in line : " , line)
            exit(1)



def actualparlist():
    global token,word,line
    actualparitem()
    while(token == 'comma_token'):
        token,word = lex()
        actualparitem()
    return



def actualparitem():
    global token,word,line
    if(token == 'in_token'):
        token,word = lex()
        expression()
    elif (token == 'inout_token'):
        token,word = lex()
        if(token =='id_token'):
            token,word = lex()
            return
        else:
            print("SyntaxError :  expected 'id' in line : " , line)
            exit(1)
    else:
        print("SyntaxError :  expected 'in' or 'inout' in line : " , line)
        exit(1)
    return



def condition():
    global token,word,line
    boolterm()
    while(token == 'or_token'): #repair code1
        token,word = lex()
        boolterm()
    return



def boolterm():
    global token,word,line
    boolfactor()
    while(token == 'and_token'):
        token,word = lex()
        boolfactor()
    return



def boolfactor():
    global token,word,line
    if(token == 'not_token'):
        token,word = lex()
        if(token == 'leftBracket_token'):
            token,word = lex()
            condition()
            if(token == 'rightBracket_token'):
                token,word = lex()
                return
            else:
                print("SyntaxError :  expected ']' in line : " , line)
                exit(1)
        else:
            print("SyntaxError :  expected '[' after not in line : " , line)
            exit(1)
    elif (token == 'leftBracket_token'):
        token,word = lex()
        condition()
        if(token == 'rightBracket_token'):
            token,word = lex()
            return
        else:
            print("SyntaxError :  expected ']' in line : " , line)
            exit(1)
    else:
        expression()
        relational_oper()
        expression()



def expression():
    global token,word,line
    optional_sign()
    term()
    while (token == 'plus_token' or token == 'minus_token'):
        add_oper()
        term()

        

def term():
    global token,word,line
    factor()
    while( token == 'multiply_token' or token == 'div_token'):
        mul_oper()
        factor()



def factor():
    global token,word,line
    if(token == 'number_token'):
        token,word = lex()
        return
    elif(token == 'leftParentheses_token'):
        token,word = lex()
        expression()
        if(token == 'rightParentheses_token'):
            token,word = lex()
            return
        else:
            print("SyntaxError :  expected ')' in line : " , line)
            exit(1)
    elif (token == 'id_token'):
        token,word = lex()
        idtail()
        return
    else:
        print("SyntaxError :  expected 'id' or 'number' or 'expression' in line : " , line)
        exit(1) 



def idtail():
    global token,word,line
    actualpars()



def relational_oper():
    global token,word,line
    if(token == 'equal_token'):
        token,word = lex()
    elif(token == 'lessOrEqual_token'):
        token,word = lex()
    elif(token == 'greaterOrEqual_token'):
        token,word = lex()
    elif(token == 'greaterThan_token'):
        token,word = lex()
    elif(token == 'lessThan_token'):
        token,word = lex()
    elif(token == 'different_token'):
        token,word = lex()
    else:
        return



def add_oper():
    global token,word,line
    if(token == 'plus_token'):
        token,word = lex()
    elif(token == 'minus_token'):
        token,word = lex()
    else:
        return



def mul_oper():
    global token,word,line
    if(token == 'multiply_token'):
        token,word = lex()
    elif(token == 'div_token'):
        token,word = lex()
    else:
        return



def optional_sign():
    global token,word,line
    add_oper()
    return



token,word = lex()
program()