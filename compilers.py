#Toncho Tonchev  3168  cse53168

import sys
import os
line = 1
token = ''
word = ''
char = ''

#Intermediate Code Generator
list_of_all_quads = []     # a list of all quartets
count_quads = 1           # quartet counter
t_i = 1                  # T_i counter
list_of_temp_var = []       # list to store temp var (T_)
is_func_flag = 0
id = ''
f = open('check3.txt','r')

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
            if (char.isdigit() or char.isalpha() or char == '(' ):
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
                start_comment = line
                line += 1
                while ('*/' not in comments):
                    char = f.read(1)
                    comments += char
                    if char == '\n':
                        line += 1
                    if char =='' and '*/' not in comments:
                        print ("The commentsBlock never be closed in line :\nStart Comments from line:", start_comment)
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

#Useful funcions for intermediate code
def next_quad():
    global count_quads
    return count_quads


def gen_quad(first, second, third, fourth):
    global count_quads
    global list_of_all_quads
    list =  []
    list = [next_quad()]
    list += [first] + [second] + [third] + [fourth]
    count_quads += 1
    list_of_all_quads += [list]
    return list


def new_temp():
    global t_i
    global list_of_temp_var
    list = ['T_']
    list.append(str(t_i))
    temp_variable = "".join(list)
    t_i += 1
    list_of_temp_var += [temp_variable]         #Save them in list  temp_variableList (is used in C-Code)
    return temp_variable


def empty_list():
    poiter_list = []
    return poiter_list


def make_list(x):
    this_list = [x]
    return this_list


def merge(list1, list2):
    list = []
    list += list1 + list2
    return list

def back_patch(list,z):
    global list_of_all_quads
    for i in range(len(list)):
        for j in range(len(list_of_all_quads)):
            if (list[i] == list_of_all_quads[j][0] and list_of_all_quads[j][4] == '_'):
                list_of_all_quads[j][4] = z
                j = len(list_of_all_quads)


# ----------------------------------------------------------------------------------



# Syntaktikos Analutis
def program():
    global token,word,line
    if(token == 'program_token'):
        token,word = lex()
        if(token == 'id_token'):
            program_name = word
            token,word = lex()
            if (token == 'leftCurly_token'):
                token,word = lex()
                block(program_name, 1)
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



def block(program_name,main_program_flag):
    declarations()
    subprograms()
    gen_quad('begin_block', program_name, '_', '_')
    statements()
    if(main_program_flag == 1):
        gen_quad('halt', '_', '_', '_')
    gen_quad('end_block', program_name, '_', '_')



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
        name = word
        token,word = lex()
        funcbody(name,0)
    else:
        print("SyntaxError :  'Wring function/procedure' name in line : " , line)
        exit(1)



def funcbody(name,is_function):
    global token,word,line
    formalpars()
    if(token == 'leftCurly_token'):
        token,word = lex()
        block(name, 0)
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
    global token,word,line,id
    if (token == 'id_token'):
        id = word
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
    # S -> id := E{P1}
    global token, word, line, is_func_flag, id
    if(token == 'assignment_token'):
        token,word = lex()
        Eplace = expression()
        #{P1}:
        if(is_func_flag == 1):		# if its function
            gen_quad(':=', temp, '_', id)
            is_func_flag = 0
        else:
            gen_quad(':=', Eplace, '_', id)
    else:
        print("SyntaxError :  expected  ':=' in line : " , line)
        exit(1)



def if_stat():
    global token,word,line
    # IS-> if C then {P1} BOS {P2} else() {P3}
    if(token == 'leftParentheses_token'):
        token,word = lex()
        C = condition()
        if(token == 'rightParentheses_token'):
            token,word = lex()
            if(token == 'then_token'):
                token,word = lex()
                #{P1}
                back_patch(C[0], next_quad())
                statements()
                #{P2}
                if_list = make_list(next_quad())
                gen_quad('jump', '_', '_', '_')
                back_patch(C[1], next_quad())
                elsepart()
                #{P3}:
                back_patch(if_list, next_quad())
            else:
                print("SyntaxError :  expected 'then' in line : " , line)
                exit(1)
        else:
            print("SyntaxError :  expected '(' in line : " , line)
            exit(1)
    else:
        print("SyntaxError :  expected  '(' in line : " , line)
        exit(1)
    is_true = C[0]
    is_false = C[1]
    return is_true, is_false



def elsepart():
    global token,word,line
    if( token == 'else_token'):
        token,word = lex()
        statements()
    return



def while_stat():
    # WS-> while ({P1} C) {P2} BOS {P3}
    global token,word,line
    if(token == 'leftParentheses_token'):
        token,word = lex()
        #{P1}:
        Cquad = next_quad()
        C = condition()
        if(token == 'rightParentheses_token'):
            #{P2}
            back_patch(C[0], next_quad())

            token,word = lex()
            statements()
            #{P3}
            gen_quad('jump', '_', '_', Cquad)
            back_patch(C[1], next_quad())  ##C[1] is list of false.
        else:
            print("SyntaxError :  expected  ')' in line : " , line)
            exit(1)
    else:
        print("SyntaxError :  expected  '(' in line : " , line)
        exit(1)
    WStrue = C[0]
    WSfalse = C[1]
    return WStrue,WSfalse



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
    Cquad = next_quad()
    while(token == 'when_token'):
        token,word = lex()
        if(token == 'leftParentheses_token'):
            token,word = lex()
            C = condition()
            #{P1}
            back_patch(C[0],next_quad())

            if(token == 'rightParentheses_token'):
                token,word = lex()
                if(token == 'colon_token'):
                    token,word = lex()
                    statements()
                    #{P2}
                    gen_quad('jump', '_', '_', Cquad)
                    back_patch(C[1], next_quad())
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
        idName = word
        token,word = lex()
        actualpars(0, idName)
    else:
        print("SyntaxError :  expected  'id' parametar in line : " , line)
        exit(1)
    return



def return_stat():
    # S -> return (E) {P1}
    global token,word,line
    Eplace = expression()
    #token,word = lex()
    #{P1}
    gen_quad('retv', Eplace, '_', '_')



def input_stat():
    # S -> print (E) {P2}
    global token,word,line
    if(token == 'leftParentheses_token'):
        token,word = lex()
        if(token == 'id_token'):
            iDplace = word
            token,word = lex()
            if(token == 'rightParentheses_token'):
                #{P2}
                gen_quad('out', iDplace, '_', '_')
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
    # S -> print (E) {P2}
    global token,word,line
    if(token == 'leftParentheses_token'):
        token,word = lex()
        Eplace = expression()
        if(token == 'rightParentheses_token'):
            token,word = lex()
            #{P2}
            gen_quad('out', Eplace, '_', '_')
        else:
            print("SyntaxError :  expected  ')' in line : " , line)
            exit(1)
    else:
        print("SyntaxError :  expected  '(' in line : " , line)
        exit(1)
    return



def actualpars(is_func_flag, idName):
    global token,word,line,temp
    if(token == 'leftParentheses_token'):
        token,word = lex()
        actualparlist()
        if(token == 'rightParentheses_token'):
            token,word = lex()
            #If it is function
            if(is_func_flag == 1):
                w = new_temp()
                gen_quad('par', w, 'RET', '_')
                gen_quad('call', idName, '_', '_')

                temp = w
            else:
                gen_quad('call', idName, '_', '_')

        else:
            print("SyntaxError :  expected ')' in line : " , line)
            exit(1)
    return



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
        thisExpression = expression()
        gen_quad('par', thisExpression, 'CV', '_')
    elif (token == 'inout_token'):
        token,word = lex()
        if(token =='id_token'):
            gen_quad('par', word, 'REF', '_')
            token,word = lex()
            #return
        else:
            print("SyntaxError :  expected 'id' in line : " , line)
            exit(1)
    else:
        print("SyntaxError :  expected 'in' or 'inout' in line : " , line)
        exit(1)
    return



def condition():
    #C-> BT1 {P1} (or {P2} BT2 {P3})*
    global token,word,line
    Ctrue = []
    Cfalse = []
    BT1 = boolterm()
    #{P1}
    Ctrue = BT1[0]
    Cfalse = BT1[1]
    while(token == 'or_token'): #repair code1
        token,word = lex()
        #{P2}:
        back_patch(Cfalse, next_quad())
        BT2 = boolterm()

        #{P3}
        Ctrue = merge(Ctrue , BT2[0])
        Cfalse = BT2[1]
    return Ctrue, Cfalse



def boolterm():
    # BT -> BF1 {P1} (and {P2} BF2 {P3})*
    global token,word,line
    BTtrue = []
    BTfalse = []
    BF1 = boolfactor()
    #{P1}
    BTtrue = BF1[0]
    BTfalse = BF1[1]

    while(token == 'and_token'):
        token,word = lex()
        #{P2}
        back_patch(BTtrue, next_quad())
        BF2 = boolfactor()
        #{P3}
        BTfalse = merge(BTfalse, BF2[1])
        BTtrue = BF2[0]
    return BTtrue,BTfalse



def boolfactor():
    global token,word,line
    BFtrue = []
    BFfalse = []
    Eplace1 = ''
    Eplace2 = ''
    relop = ''

    if(token == 'not_token'):
        # BF-> not [C] {P1}
        token,word = lex()
        if(token == 'leftBracket_token'):
            token,word = lex()
            C = condition()  #returns 2 lists (list of true & false), as tuples.
            if(token == 'rightBracket_token'):
                token,word = lex()
                #{P1}:
                BFtrue = C[1]					#C[1] is list of false.
                BFfalse = C[0]					#C[0] is list of true.
            else:
                print("SyntaxError :  expected ']' in line : " , line)
                exit(1)
        else:
            print("SyntaxError :  expected '[' after not in line : " , line)
            exit(1)
    elif (token == 'leftBracket_token'):
        # BF-> [C] {P1}
        token,word = lex()
        C = condition()
        if(token == 'rightBracket_token'):
            token,word = lex()
            #{P1}:
            BFtrue = C[0]						#C[0] is list of true.
            BFfalse = C[1]						#C[1] is list of false.
        else:
            print("SyntaxError :  expected ']' in line : " , line)
            exit(1)
    else:
        # BF-> E1 relop E2 {P1}
        Eplace1 = expression()
        relop = relational_oper()
        Eplace2 = expression()

        #{P1}
        BFtrue = make_list(next_quad())
        gen_quad(relop, Eplace1, Eplace2, '_')	#will be back_patched later on.
        BFfalse = make_list(next_quad())
        gen_quad('jump', '_', '_', '_')			#will be back_patched later on.
    return BFtrue, BFfalse



def expression():
    # E -> T1(+- T2 {P1}) *{P2}
    global token,word,line
    optional_sign()
    T1place = term()
    while (token == 'plus_token' or token == 'minus_token'):
        plusOrMinus = add_oper()
        T2place = term()
        #{P1}
        w = new_temp()
        gen_quad(plusOrMinus, T1place, T2place, w)
        T1place = w
    #{P2}
    Eplace = T1place
    return Eplace


def term():
    # T-> F1 (mulOper F2 {P1})* {P2}
    global token,word,line
    F1place = factor()
    while( token == 'multiply_token' or token == 'div_token'):
        mulOrDiv = mul_oper()
        F2place = factor()
        #{P1}
        w = new_temp()
        gen_quad(mulOrDiv, F1place, F2place, w)
        F1place = w
    #{P2}
    Tplace = F1place
    return Tplace



def factor():
    global token,word,line
    print ("eimai factor kai wo word einai:",word)
    if(token == 'number_token'):
        fact = word
        token,word = lex()
    elif(token == 'leftParentheses_token'):
        token,word = lex()
        Eplace = expression()
        if(token == 'rightParentheses_token'):
            fact = Eplace
            token,word = lex()
        else:
            print("SyntaxError :  expected ')' in line : " , line)
            exit(1)
    elif (token == 'id_token'):
        fact = word
        token,word = lex()
        idtail(fact)
    else:
        print("SyntaxError :  expected 'id error' or 'number' or 'expression' in line : " , line)
        exit(1)
    return fact



def idtail(idName):
    global token,word,line,is_func_flag
    if(token == 'leftParentheses_token'):
        is_func_flag = 1
        actualpars(1, idName)
        return



def relational_oper():
    global token,word,line
    if(token == 'equal_token'):
        relod = word
        token,word = lex()
    elif(token == 'lessOrEqual_token'):
        relod = word
        token,word = lex()
    elif(token == 'greaterOrEqual_token'):
        relod = word
        token,word = lex()
    elif(token == 'greaterThan_token'):
        relod = word
        token,word = lex()
    elif(token == 'lessThan_token'):
        relod = word
        token,word = lex()
    elif(token == 'different_token'):
        relod = word
        token,word = lex()
    else:
        print('error: Missing = or < or <= or <> or >= or > in line ',line)
        exit(1)
    return relod



def add_oper():
    global token,word,line
    if(token == 'plus_token'):
        oper = word
        token,word = lex()
        return oper
    elif(token == 'minus_token'):
        oper = word
        token,word = lex()
        return oper



def mul_oper():
    global token,word,line
    if(token == 'multiply_token'):
        oper = word
        token,word = lex()
        return oper
    elif(token == 'div_token'):
        oper = word
        token,word = lex()
        return oper



def optional_sign():
    global token,word,line
    addoper = add_oper()
    return addoper




token,word = lex()
program()
for i in range(len(list_of_all_quads)):
	print (str(list_of_all_quads[i][0])+" "+str(list_of_all_quads[i][1])+" "+str(list_of_all_quads[i][2])+" "+str(list_of_all_quads[i][3])+" "+str(list_of_all_quads[i][4]))
