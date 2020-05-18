#Toncho Tonchev  3168  cse53168

import sys
import os
line = 1
token = ''
word = ''
char = ''

#Intermediate Code Generator
list_of_all_quads = []     # a list of all quartets
count_quads = 1           # quarter counter
t_i = 1                  # T_i counter
list_of_all_temp_var = []       # list to store temp var (T_)
is_function = 0
f = open(sys.argv[1],'r')
c_file = open('new_c_file.c', 'w')
int_file = open('new_int_file.int', 'w')

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
            elif(char == ' '):
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
            elif(char == ' '):
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
    #print("word:",word)
    #print("token:",token)
    #print ("\n")
    return token,word



#------------ Useful funcions for intermediate code ------------#

def next_quad():
    global count_quads

    return count_quads



def gen_quad(operation, x, y, z):
    global count_quads
    global list_of_all_quads

    list = [next_quad()]
    list += [operation] + [x] + [y] + [z]
    count_quads += 1
    list_of_all_quads += [list]

    return list



def new_temp():
    global t_i
    global list_of_all_temp_var

    list = ['T_']
    list.append(str(t_i))
    t_i += 1
    temp_variable = "".join(list)
    list_of_all_temp_var += [temp_variable]         # Save them in list  list_of_all_temp_var (is used in C-Code)

    entity = Entity()
    entity.type = 'temp_variable'
    entity.name = temp_variable
    entity.tempVar.offset = compute_offset()
    new_entity(entity)

    return temp_variable



def empty_list():
    empty_list = []

    return empty_list



def make_list(x):
    make_list = [x]

    return make_list



def merge(list_1, list_2):
    list = []
    list += list_1 + list_2

    return list



def back_patch(list, label):
    global list_of_all_quads

    for i in range(len(list)):
        for j in range(len(list_of_all_quads)):
            if (list[i] == list_of_all_quads[j][0] and list_of_all_quads[j][4] == '_'):
                list_of_all_quads[j][4] = label


#---------------------------------------------------------------------




#---------- Usefull Classes and Functions for Symbols Table ----------#


class Argument:

	def __init__(self):
		self.name = ''		#Dinw to name gia na kserw poio Argument einai.
		self.type = 'int'	#All variables in this language will be Int.
		self.parMode = ''	# 'CV', 'REF'



class Entity:

    def __init__(self):
        self.name = ''
        self.type = ''

        self.variable = self.Variable()
        self.subprogram = self.SubProgram()
        self.parameter = self.Parameter()
        self.tempVar = self.TempVar()


    class Variable:

        def __init__(self):
            self.type = 'int'
            self.offset = 0


    class SubProgram:

        def __init__(self):
            self.type = ''
            self.startQuad = 0
            self.frameLength = 0
            self.argumentList = []
            self.nestingLevel = 0


    class Parameter:

        def __init__(self):
            self.mode = ''
            self.offset = 0


    class TempVar:

        def __init__(self):
            self.type = 'int'
            self.offset = 0



class Scope:

    def __init__(self):
        self.name = ''
        self.entityList = []
        self.nestingLevel = 0
        self.enclosingScope = None



def new_argument(object):
    global topScope

    topScope.entityList[-1].subprogram.argumentList.append(object)



def new_entity(object):
    global topScope

    topScope.entityList.append(object)

topScope = None



def new_scope(name):
    global topScope

    nextScope = Scope()
    nextScope.name = name
    nextScope.enclosingScope = topScope

    if(topScope == None):
        nextScope.nestingLevel = 0
    else:
        nextScope.nestingLevel = topScope.nestingLevel + 1

    topScope = nextScope



def delete_scope():
    global topScope

    freeScope = topScope
    topScope = topScope.enclosingScope
    del freeScope



def compute_offset():
    global topScope

    counter = 0
    if(topScope.entityList is not []):
        for entity in (topScope.entityList):
            if(entity.type == 'variable' or entity.type == 'parameter' or entity.type == 'temp_variable'):
                counter += 1

    offset = 12 + (counter * 4)

    return offset



def compute_startQuad():
    global topScope

    topScope.enclosingScope.entityList[-1].subprogram.startQuad = next_quad()



def compute_framelength():
    global topScope

    topScope.enclosingScope.entityList[-1].subprogram.frameLength = compute_offset()



def add_parameters():
    global topScope

    for arg in topScope.enclosingScope.entityList[-1].subprogram.argumentList:
        entity = Entity()
        entity.name = arg.name
        entity.type = 'parameter'
        entity.parameter.mode = arg.parMode
        entity.parameter.offset = compute_offset()
        new_entity(entity)



def print_symbol_table():
    global topScope

    scope = topScope

    while scope != None:
        print("Nesting-Level:"+str(scope.nestingLevel) +"\t\t"+ "SCOPE: "+"Name: "+scope.name)
        print("\t\t\tENTITIES:")
        for entity in scope.entityList:

            if(entity.type == 'Sub_Program'):
                print("\t\t\t\t |--> "+" Name:"+entity.name+"\t Type:"+entity.type+"\t Sub_Type:" +entity.subprogram.type+"\t Start-Quad:"+str(entity.subprogram.startQuad)+"\t frameLength:"+str(entity.subprogram.frameLength))
                print("\t\t\t\t\tARGUMENTS:")
                for argument in entity.subprogram.argumentList:
                    print("\t\t\t\t\t |--> "+" Name:"+argument.name+"\t Type:"+argument.type+"\t Parameter-Mode:"+argument.parMode)

            elif(entity.type == 'variable'):
                print("\t\t\t\t |--> "+" Name:"+entity.name+"\t Type:"+entity.type+"\t Variable-Type:"+entity.variable.type+"\t Offset:"+str(entity.variable.offset))

            elif(entity.type == 'parameter'):
                print("\t\t\t\t |--> "+" Name:"+entity.name+"\t Type:"+entity.type+"\t Mode:"+entity.parameter.mode+"\t Offset:"+str(entity.parameter.offset))

            elif(entity.type == 'temp_variable'):
                print("\t\t\t\t |--> "+" Name:"+entity.name+"\t Type:"+entity.type+"\t Temp-Type:"+entity.tempVar.type+"\t Offset:"+str(entity.tempVar.offset))

        scope = scope.enclosingScope

    print("------------------------------------------------------------------------------------------")



# ----------------------------------------------------------------------------------




#------------------- Useful funcions for Final Code -------------------#

ascFile = open('new_asm_file.asm','w')
ascFile.write('         \n\n\n')


def gnlvcode(name):  #DIAFANEIA 7

	global topScope
	global ascFile

	ascFile.write('lw $t0,-4($sp)\n') #stoiva tou patera

	(sc1,entity1)=search_comb(name)

	#/*an einai pappous h' megaliteros progonos,kane to loop "my_help" fores*/
	my_help= topScope.nestingLevel - sc1.nestingLevel;
	my_help=my_help-1 #giati gia ton patera exoume paragei

	for i in range(0,my_help):
		ascFile.write('lw $t0,-4($t0)\n')


	if entity1.type=='variable':
		x=entity1.variable.offset
	elif entity1.type=='PARAM':
		x=entity1.parameter.offset

	ascFile.write('add $t0,$t0,-%d\n' % (x))



def loadvr(v,r): #DIAFANEIES 8 eos 11 (r akeraios, v string)

		global topScope

		global ascFile

		if v.isdigit():  #DIAFANEIA 9 (panw) αν v είναι σταθερά
			ascFile.write('li $t%d,%s\n' % (r,v))

		else: # allios v einai metavliti
			(sc1,entity1)=search_comb(v)

			#DIAFANEIA 9 (katw)
			#sc1.nestingLevel==0 simainei sximatika sto KATW epipedo (kirios programma)
			if sc1.nestingLevel==0 and entity1.type=='variable': #, αν v είναι καθολική μεταβλητή – δηλαδή ανήκει στο κυρίως πρόγραμμα
					ascFile.write('lw $t%d,-%d($s0)\n' % (r,entity1.variable.offset))
			elif sc1.nestingLevel==0 and entity1.type=='temp_variable': #DIAFANEIA 9, αν v είναι καθολική μεταβλητή – δηλαδή ανήκει στο κυρίως πρόγραμμα
					ascFile.write('lw $t%d,-%d($s0)\n' % (r,entity1.tempVar.offset))

			#DIAFANEIA 10 (panw) αν v είναι τοπική μεταβλητή, ή τυπική παράμετρος που περνάει με τιμή και βάθος φωλιάσματος ίσο με το τρέχον, ή προσωρινή μεταβλητή
			elif sc1.nestingLevel == topScope.nestingLevel: #βάθος φωλιάσματος ίσο με το τρέχον
				if entity1.type=='variable': #αν v είναι τοπική μεταβλητή
						ascFile.write('lw $t%d,-%d($sp)\n' % (r,entity1.variable.offset))

				elif entity1.type=='temp_variable': # ή προσωρινή μεταβλητή
						ascFile.write('lw $t%d,-%d($sp)\n' % (r,entity1.tempVar.offset))

				elif entity1.type=='PARAM' and entity1.parameter.mode=='CV': #τυπική παράμετρος που περνάει με τιμή
						ascFile.write('lw $t%d,-%d($sp)\n' % (r,entity1.parameter.offset))

				#DIAFANEIA 10 (katw) αν v είναι τυπική παράμετρος που περνάει με αναφορά
				elif entity1.type=='PARAM' and entity1.parameter.mode=='REF':
						ascFile.write('lw $t0,-%d($sp)\n' % (entity1.parameter.offset))
						ascFile.write('lw $t%d,($t0)\n' % (r))

			#DIAFANEIA 11 (panw) αν v είναι τοπική μεταβλητή, ή τυπική παράμετρος που περνάει με τιμή και βάθος φωλιάσματος μικρότερο από το τρέχον
			elif sc1.nestingLevel < topScope.nestingLevel: # βάθος φωλιάσματος μικρότερο από το τρέχον
				if entity1.type=='variable':
						gnlvcode(v)
						ascFile.write('lw $t%d,($t0)\n' % (r))
				elif entity1.type=='PARAM' and entity1.parameter.mode=='CV':
						gnlvcode(v)
						ascFile.write('lw $t%d,($t0)\n' % (r))

				#DIAFANEIA 11 (katw) αν v είναι τυπική παράμετρος που περνάει με αναφορά
				elif entity1.type=='PARAM' and entity1.parameter.mode=='REF':
						gnlvcode(v)
						ascFile.write('lw $t0,($t0)\n')
						ascFile.write('lw $t%d,($t0)\n' % (r))


def storerv(r,v):  #DIAFANEIES 12 eos 15 (r akeraios, v string)

	global topScope
	global ascFile

	(sc1,entity1)=search_comb(v)

	#DIAFANEIA 13
	#sc1.nestingLevel==0 simainei sximatika sto KATW epipedo (kirios programma)
	if sc1.nestingLevel==0 and entity1.type=='variable':
		ascFile.write('sw $t%d,-%d($s0)\n' % (r,entity1.variable.offset))
	elif sc1.nestingLevel==0 and entity1.type=='temp_variable':
		ascFile.write('sw $t%d,-%d($s0)\n' % (r,entity1.tempVar.offset))

	#DIAFANEIA 14 (panw) αν v είναι τοπική μεταβλητή, ή τυπική παράμετρος που περνάει με τιμή και βάθος φωλιάσματος ίσο με το τρέχον, ή προσωρινή μεταβλητή
	elif sc1.nestingLevel == topScope.nestingLevel:
		if entity1.type=='variable':
			ascFile.write('sw $t%d,-%d($sp)\n' % (r,entity1.variable.offset))

		elif entity1.type=='temp_variable':
			ascFile.write('sw $t%d,-%d($sp)\n' % (r,entity1.tempVar.offset))

		elif entity1.type=='PARAM' and entity1.parameter.mode=='CV':
			ascFile.write('sw $t%d,-%d($sp)\n' % (r,entity1.parameter.offset))

		#DIAFANEIA 14 (katw) αν v είναι τυπική παράμετρος που περνάει με αναφορά
		elif entity1.type=='PARAM' and entity1.parameter.mode=='REF':
			ascFile.write('lw $t0,-%d($sp)\n' %  (entity1.parameter.offset))
			ascFile.write('sw $t%d,($t0)\n' % (r))

	#DIAFANEIA 15 (panw) αν v είναι τοπική μεταβλητή, ή τυπική παράμετρος που περνάει με τιμή και βάθος φωλιάσματος μικρότερο από το τρέχον
	elif sc1.nestingLevel < topScope.nestingLevel:
		if entity1.type=='variable':
			gnlvcode(v)
			ascFile.write('sw $t%d,($t0)\n' % (r))
		elif entity1.type=='PARAM' and entity1.parameter.mode=='CV':
			gnlvcode(v)
			ascFile.write('sw $t%d,($t0)\n' % (r))

		#DIAFANEIA 15 (katw) αν v είναι τυπική παράμετρος που περνάει με αναφορά
		elif entity1.type=='PARAM' and entity1.parameter.mode=='REF':
			gnlvcode(v)
			ascFile.write('lw $t0,($t0)\n')
			ascFile.write('sw $t%d,($t0)\n' % (r))




def search_list_after(i):

	global list_of_all_quads

	start=i
	while start>=i:

		if (list_of_all_quads[start][1] == 'call'):  # molis vro to "call"
			return str(list_of_all_quads[start][2])  #epistrefo to onoma tis sinartisis/diadikasias

		start=start+1

seira=-1

def final():  # tin kalw PANTA META to "end_block" kai prin to "delete_scope"  (mesa stin block)

	global topScope
	global list_of_all_quads, seira
	global ascFile

	for i in range(len(list_of_all_quads)): # diasxise tis tetrades mexri stigmis

		ascFile.write('L%d: \n' % (list_of_all_quads[i][0])) # Lkati: (label)

		if (list_of_all_quads[i][1] == 'jump'): #DIAFANEIA 16 (panw)
			ascFile.write('j L'+str(list_of_all_quads[i][4])+'\n')
		elif (list_of_all_quads[i][1] == '='): #DIAFANEIA 16 (katw)
			loadvr(list_of_all_quads[i][2],1)
			loadvr(list_of_all_quads[i][3],2)
			ascFile.write('beq,$t1,$t2,L'+str(list_of_all_quads[i][4])+'\n')
		elif (list_of_all_quads[i][1] == '<>'): #DIAFANEIA 16 (katw)
			loadvr(list_of_all_quads[i][2],1)
			loadvr(list_of_all_quads[i][3],2)
			ascFile.write('bne,$t1,$t2,L'+str(list_of_all_quads[i][4])+'\n')
		elif (list_of_all_quads[i][1] == '>'): #DIAFANEIA 16 (katw)
			loadvr(list_of_all_quads[i][2],1)
			loadvr(list_of_all_quads[i][3],2)
			ascFile.write('bgt,$t1,$t2,L'+str(list_of_all_quads[i][4])+'\n')
		elif (list_of_all_quads[i][1] == '<'): #DIAFANEIA 16 (katw)
			loadvr(list_of_all_quads[i][2],1)
			loadvr(list_of_all_quads[i][3],2)
			ascFile.write('blt,$t1,$t2,L'+str(list_of_all_quads[i][4])+'\n')
		elif (list_of_all_quads[i][1] == '>='):	 #DIAFANEIA 16 (katw)
			loadvr(list_of_all_quads[i][2],1)
			loadvr(list_of_all_quads[i][3],2)
			ascFile.write('bge,$t1,$t2,L'+str(list_of_all_quads[i][4])+'\n')
		elif (list_of_all_quads[i][1] == '<='): #DIAFANEIA 16 (katw)
			loadvr(list_of_all_quads[i][2],1)
			loadvr(list_of_all_quads[i][3],2)
			ascFile.write('ble,$t1,$t2,L'+str(list_of_all_quads[i][4])+'\n')
		elif (list_of_all_quads[i][1] == ':='): #DIAFANEIA 17
			loadvr(list_of_all_quads[i][2],1)
			storerv(1,list_of_all_quads[i][4])
		elif (list_of_all_quads[i][1] == '+'): #DIAFANEIA 18
			loadvr(list_of_all_quads[i][2],1)
			loadvr(list_of_all_quads[i][3],2)
			ascFile.write('add,$t1,$t1,$t2'+'\n')
			storerv(1,list_of_all_quads[i][4])
		elif (list_of_all_quads[i][1] == '-'): #DIAFANEIA 18
			loadvr(list_of_all_quads[i][2],1)
			loadvr(list_of_all_quads[i][3],2)
			ascFile.write('sub,$t1,$t1,$t2'+'\n')
			storerv(1,list_of_all_quads[i][4])
		elif (list_of_all_quads[i][1] == '*'): #DIAFANEIA 18
			loadvr(list_of_all_quads[i][2],1)
			loadvr(list_of_all_quads[i][3],2)
			ascFile.write('mul,$t1,$t1,$t2'+'\n')
			storerv(1,list_of_all_quads[i][4])
		elif (list_of_all_quads[i][1] == '/'): #DIAFANEIA 18
			loadvr(list_of_all_quads[i][2],1)
			loadvr(list_of_all_quads[i][3],2)
			ascFile.write('div,$t1,$t1,$t2'+'\n')
			storerv(1,list_of_all_quads[i][4])
		elif (list_of_all_quads[i][1] == 'out'): #DIAFANEIA 19 (panw)
			ascFile.write('li $v0,1'+'\n')
			loadvr(list_of_all_quads[i][2],1)   # den to exei (gia na parw to "x")
			ascFile.write('move $a0,$t1'+'\n') # den to exei
			ascFile.write('syscall'+'\n')
		elif (list_of_all_quads[i][1] == 'inp'): #DIAFANEIA 19 (katw)
			ascFile.write('li $v0,5'+'\n')
			ascFile.write('syscall'+'\n')
			ascFile.write('move $t1,$v0'+'\n') # den to exei
			storerv(1,list_of_all_quads[i][2])    # den to exei
		elif (list_of_all_quads[i][1] == 'retv'):  #DIAFANEIA 20 (panw)
			loadvr(list_of_all_quads[i][2],1)
			ascFile.write('lw $t0,-8($sp)\n')
			ascFile.write('sw $t1,($t0)\n')
		elif (list_of_all_quads[i][1] == 'par'):  #DIAFANEIA 21 eos 27
			if seira==-1:  #DIAFANEIA 21 (PRIN to proto par)
				# prepei na PSAKSO apo tin tetrada "i" pros ta katw to "call", giati ekei vrisketai to onoma
				# tis sinartisis/diadikasias (fname) pou thelo, oste telika na vro to FRAMELENGTH
				fname=search_list_after(i)
				(sc1,entity1)=search_comb(fname)
				ascFile.write('add $fp,$sp,%d\n' % (entity1.subprogram.frameLength))   #FRAMELENGTH
				seira=0   #  arxikopoiisi tou "i"

			if (list_of_all_quads[i][3] == 'CV'):  #DIAFANEIA 22
				loadvr(list_of_all_quads[i][2],0)
				ascFile.write('sw $t0,-%d($fp)\n' % (12+4*seira))
				seira=seira+1  # stis diafaneies to exei "i"
			elif (list_of_all_quads[i][3] == 'RET'):
				(sc1,entity1)=search_comb(list_of_all_quads[i][2])   #DIAFANEIA 27
				ascFile.write('add $t0,$sp,-%d\n' % (entity1.tempVar.offset))
				ascFile.write('sw $t0,-8($fp)\n')
			elif (list_of_all_quads[i][3] == 'REF'):  #DIAFANEIA 23 eos 26
				(sc1,entity1)=search_comb(list_of_all_quads[i][2])

				if sc1.nestingLevel==topScope.nestingLevel:  #DIAFANEIA 23 kai 24 (ίδιο βάθος φωλιάσματος)
					if entity1.type=='variable':  #DIAFANEIA 23
						ascFile.write('add $t0,$sp,-%d\n' % (entity1.variable.offset))
						ascFile.write('sw $t0,-%d($fp)\n' % (12+4*seira))
					elif entity1.type=='PARAM' and entity1.parameter.mode=='CV':  #DIAFANEIA 23
						ascFile.write('add $t0,$sp,-%d\n' % (entity1.parameter.offset))
						ascFile.write('sw $t0,-%d($fp)\n' % (12+4*seira))
					elif entity1.type=='PARAM' and entity1.parameter.mode=='REF':  #DIAFANEIA 24
						ascFile.write('lw $t0,-%d($sp)\n' % (entity1.parameter.offset))
						ascFile.write('sw $t0,-%d($fp)\n' % (12+4*seira))

				elif sc1.nestingLevel<topScope.nestingLevel:  #DIAFANEIA 25 kai 26 (διαφορετικο βάθος φωλιάσματος)
					gnlvcode(list_of_all_quads[i][2])
					if entity1.type=='PARAM' and entity1.parameter.mode=='REF':  #DIAFANEIA 26
					    ascFile.write('lw $t0,($t0)\n')
					    ascFile.write('sw $t0,-%d($fp)\n' % (12+4*seira))
					else: #DIAFANEIA 25
					    ascFile.write('sw $t0,-%d($fp)\n' % (12+4*seira))
				seira=seira+1
		elif (list_of_all_quads[i][1] == 'call'): #DIAFANEIA 28 kai 29
			seira=-1 # reset

			(sc1,entity1)=search_comb(list_of_all_quads[i][2])
            #print("to topScope level einai:",topScope.nestingLevel)
            #print("to entity1 level einai:",entity1.nestingLevel)
			if topScope.nestingLevel == entity1.subprogram.nestingLevel:  #DIAFANEIA 28 (1i periptosi)
				ascFile.write('lw $t0,    einai edw  -4($sp)\n')
				ascFile.write('sw $t0,-4($fp)\n')
			elif topScope.nestingLevel < entity1.subprogram.nestingLevel:  #DIAFANEIA 28 (2i periptosi)
				ascFile.write('sw $sp,-4($fp)\n')

			ascFile.write('add $sp,$sp,%d\n' % (entity1.subprogram.frameLength)) #DIAFANEIA 29
			ascFile.write('jal L%d\n' % (entity1.subprogram.startQuad))          #DIAFANEIA 29
			ascFile.write('add $sp,$sp,-%d\n' % (entity1.subprogram.frameLength)) #DIAFANEIA 29

		elif ( list_of_all_quads[i][1] == 'begin_block' and topScope.nestingLevel!=0):  #DIAFANEIA 30 (panw) [OXI sto program, dld mono se function/procedure]
			ascFile.write('sw $ra,($sp)\n')
		elif ( list_of_all_quads[i][1] == 'begin_block' and topScope.nestingLevel==0):  #DIAFANEIA 31 [TWRA sto program]
			ascFile.seek(0, os.SEEK_SET)
			ascFile.write('j L%d\n'% (list_of_all_quads[i][0]))  #  DIAFANEIA 31 j Lmain , prepei na grafei stin arxi tou arxeiou
			ascFile.seek(0, os.SEEK_END)

			ascFile.write('add $sp,$sp,%d\n' % (compute_offset()))   #DIAFANEIA 31
			ascFile.write('move $s0,$sp\n')                            #DIAFANEIA 31
		elif ( list_of_all_quads[i][1] == 'end_block' and topScope.nestingLevel!=0):  #DIAFANEIA 30 (katw) [OXI sto program, dld mono se function/procedure]
			ascFile.write('lw $ra,($sp)\n')
			ascFile.write('jr $ra\n')




	# reset, giati otan kalw ti final PREPEI na exoun diagrafei oi proigoumenes tetrades METAKSI begin_block kai end_block
	list_of_all_quads = []

def search_comb(n):
	global topScope

	sco=topScope
	while sco != None:
		for entity in sco.entityList:
			if(entity.name == n):
				return (sco,entity)
		sco=sco.enclosingScope

	print("Den brethike ston pinaka simbolon kombos me onoma " + str(n))
	exit()



# ----------------------------------------------------------------------------------



#---------- Syntax Analyzer ----------#
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
        print("SyntaxError : Not found the word 'program' which was expected in line : " , line)
        exit(1)



def block(program_name, is_main_program):
    global token,word,line

    new_scope(program_name)
    if(is_main_program != 1):
        add_parameters()

    declarations()
    subprograms()
    gen_quad('begin_block', program_name, '_', '_')

    if(is_main_program != 1):
        compute_startQuad()

    statements()

    if(is_main_program == 1):
        gen_quad('halt', '_', '_', '_')
    else:
        compute_framelength()

    gen_quad('end_block', program_name, '_', '_')

    print_symbol_table()
    final()
    delete_scope()
    print("Last scope has been deleted.")



def declarations():
    global token,word,line

    while(token == 'declare_token'):
        c_file.write("int ")
        token,word = lex()
        varlist()
        if(token == 'semicolon_token'):
            token,word = lex()
        else:
            print("SyntaxError :  ';' was expected in line : " , line)
            exit(1)
    c_file.write(";\n\t")



def subprograms():
    global token,word,line

    while(token == 'function_token' or token == 'procedure_token'):
        if(token == 'function_token'):
            token,word = lex()
            subprogram(0)
        else:
            token,word = lex()
            subprogram(1)



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
        c_file.write(word)

        entity = Entity()
        entity.type = 'variable'
        entity.name = word
        entity.variable.offset = compute_offset()
        new_entity(entity)

        token ,word = lex()
        while(token == 'comma_token'):
            c_file.write(word)
            token,word = lex()
            if(token == 'id_token' ):
                c_file.write(word)

                entity = Entity()
                entity.type = 'variable'
                entity.name = word
                entity.variable.offset = compute_offset()
                new_entity(entity)

                token,word = lex()
            else:
                print("SyntaxError :  'id' was expected in line : " , line)
                exit(1)



def subprogram(is_procedure):
    global token,word,line

    if(token == 'id_token' and is_procedure == 1):
        subprogram_name = word

        entity = Entity()
        entity.name = word
        entity.type = 'Sub_Program'
        entity.subprogram.type = 'Procedure'
        entity.subprogram.nestingLevel = topScope.nestingLevel + 1 # gia TELIKO
        new_entity(entity)

        token,word = lex()
        funcbody(subprogram_name,0)
    elif(token == 'id_token' and is_procedure == 0):
        subprogram_name = word

        entity = Entity()
        entity.type = 'Sub_Program'
        entity.name = word
        entity.subprogram.type = 'Function'
        entity.subprogram.nestingLevel = topScope.nestingLevel + 1
        new_entity(entity)

        token,word = lex()
        funcbody(subprogram_name,0)
    else:
        print("SyntaxError :  'Wrong function/procedure' name in line : " , line)
        exit(1)



def funcbody(subprogram_name,is_function):
    global token,word,line

    formalpars()
    if(token == 'leftCurly_token'):
        token,word = lex()
        block(subprogram_name, 0)
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

    argument = Argument()

    if(token == 'in_token' ):
        token,word = lex()
        if(token == 'id_token'):


            argument.name = word
            argument.parMode = 'CV'
            new_argument(argument)

            token,word = lex()
        else:
            print("SyntaxError : parameters was expected in line : " , line)
            exit(1)
    elif(token == 'inout_token'):
        token,word = lex()
        if(token == 'id_token'):

            argument.name = word
            argument.parMode = 'REF'
            new_argument(argument)

            token,word = lex()
        else:
            print("SyntaxError : parameters was expected in line : " , line)
            exit(1)



def statement():
    global token,word,line

    if (token == 'id_token'):
        id = word
        token,word = lex()
        assignment_stat(id)
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



def assignment_stat(id):
    global token, word, line, is_function, temp
    # S -> id := E{P1}

    if(token == 'assignment_token'):
        token,word = lex()
        e_place = expression()
        #{P1}:
        if(is_function == 1):
            gen_quad(':=', temp, '_', id)
            is_function = 0
        else:
            gen_quad(':=', e_place, '_', id)
    else:
        print("SyntaxError :  expected  ':=' in line : " , line)
        exit(1)



def if_stat():
    global token,word,line
    # S-> if B then {P1} S1 {P2} TAIL {P3}

    if(token == 'leftParentheses_token'):
        token,word = lex()
        b_true, b_false = condition()
        if_is_true = b_true
        if_is_false = b_false
        if(token == 'rightParentheses_token'):
            token,word = lex()
            if(token == 'then_token'):
                token,word = lex()
                #{P1}
                back_patch(b_true, next_quad())
                statements()
                #{P2}
                if_list = make_list(next_quad())
                gen_quad('jump', '_', '_', '_')
                back_patch(b_false, next_quad())
                #TAIL
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

    return if_is_true, if_is_false



def elsepart():
    global token,word,line

    if( token == 'else_token'):
        token,word = lex()
        statements()



def while_stat():
    global token,word,line
    # S -> while {P1} B do {P2} S2 {P3}

    if(token == 'leftParentheses_token'):
        token,word = lex()
        #{P1}:
        b_quad = next_quad()
        b_true, b_false = condition()
        while_is_true = b_true
        while_is_false = b_false
        if(token == 'rightParentheses_token'):
            #{P2}
            back_patch(b_true, next_quad())
            token,word = lex()
            statements()
            #{P3}
            gen_quad('jump', '_', '_', b_quad)
            back_patch(b_false, next_quad())
        else:
            print("SyntaxError :  expected  ')' in line : " , line)
            exit(1)
    else:
        print("SyntaxError :  expected  '(' in line : " , line)
        exit(1)

    return while_is_true, while_is_false



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
    token,word = lex()

    return


def forcase_stat():
    global token,word,line
    # forcase {P1} (when (B) {P2} : Si )*        i,j = 1,2,3,4,
    #                default: Sj

    #{P1}
    b_quad = next_quad()
    while(token == 'when_token'):
        token,word = lex()
        if(token == 'leftParentheses_token'):
            token,word = lex()
            b_true, b_false = condition()
            #{P2}
            back_patch(b_true,next_quad())

            if(token == 'rightParentheses_token'):
                token,word = lex()
                if(token == 'colon_token'):
                    token,word = lex()
                    statements()
                    #{P2}
                    gen_quad('jump', '_', '_', b_quad)
                    back_patch(b_false, next_quad())
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
        procedure_name = word
        token,word = lex()
        actualpars(0, procedure_name)
    else:
        print("SyntaxError :  expected  'id' parametar in line : " , line)
        exit(1)
    return



def return_stat():
    global token,word,line
    # S -> return (E) {P1}

    e_place = expression()
    #{P1}
    gen_quad('retv', e_place, '_', '_')



def input_stat():
    global token,word,line
    # S -> input (id) {P2}

    if(token == 'leftParentheses_token'):
        token,word = lex()
        if(token == 'id_token'):
            id_place = word
            token,word = lex()
            if(token == 'rightParentheses_token'):
                #{P1}
                gen_quad('inp', id_place, '_', '_')
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
    # S -> print (E) {P2}

    if(token == 'leftParentheses_token'):
        token,word = lex()
        e_place = expression()
        if(token == 'rightParentheses_token'):
            token,word = lex()
            #{P2}
            gen_quad('out', e_place, '_', '_')
        else:
            print("SyntaxError :  expected  ')' in line : " , line)
            exit(1)
    else:
        print("SyntaxError :  expected  '(' in line : " , line)
        exit(1)



def actualpars(is_function, id_name):
    global token,word,line,temp

    if(token == 'leftParentheses_token'):
        token,word = lex()
        actualparlist()
        if(token == 'rightParentheses_token'):
            token,word = lex()
            #is function
            if(is_function == 1):
                w = new_temp()
                gen_quad('par', w, 'RET', '_')
                temp = w

            gen_quad('call', id_name, '_', '_')

        else:
            print("SyntaxError :  expected ')' in line : " , line)
            exit(1)



def actualparlist():
    global token, word, line

    actualparitem()
    while(token == 'comma_token'):
        token,word = lex()
        actualparitem()



def actualparitem():
    global token,word,line

    if(token == 'in_token'):
        token,word = lex()
        in_expression = expression()
        gen_quad('par', in_expression, 'CV', '_')
    elif (token == 'inout_token'):
        token,word = lex()
        if(token == 'id_token'):
            gen_quad('par', word, 'REF', '_')
            token,word = lex()
        else:
            print("SyntaxError :  expected 'id' in line : " , line)
            exit(1)
    else:
        print("SyntaxError :  expected 'in' or 'inout' in line : " , line)
        exit(1)



def condition():
    global token,word,line
    # B -> Q1 {P1} (or {P2} Q2 {P3})*

    q1_true, q1_false = boolterm()
    #{P1}
    b_true = q1_true
    b_false = q1_false
    while(token == 'or_token'):
        token,word = lex()
        #{P2}:
        back_patch(b_false, next_quad())
        q2_true, q2_false = boolterm()

        #{P3}
        b_true = merge(b_true , q2_true)
        b_false = q2_false

    return b_true, b_false



def boolterm():
    global token,word,line
    # Q -> R1 {P1} (and {P2} R2 {P3})*

    r1_true, r1_false = boolfactor()
    #{P1}
    q_true = r1_true
    q_false = r1_false

    while(token == 'and_token'):
        token,word = lex()
        #{P2}
        back_patch(q_true, next_quad())
        r2_true, r2_false = boolfactor()
        #{P3}
        q_false = merge(q_false, r2_false)
        q_true = r2_true

    return q_true, q_false



def boolfactor():
    global token,word,line

    # R -> not (B) {P1}
    if(token == 'not_token'):
        token,word = lex()
        if(token == 'leftBracket_token'):
            token,word = lex()
            b_true, b_false = condition()
            if(token == 'rightBracket_token'):
                token,word = lex()
                #{P1}:
                r_true = b_false					# change because of 'not' : true -> fasle
                r_false = b_true					# change because of 'not' : false -> true
            else:
                print("SyntaxError :  expected ']' in line : " , line)
                exit(1)
        else:
            print("SyntaxError :  expected '[' after not in line : " , line)
            exit(1)

    # R -> (B) {P1}
    elif (token == 'leftBracket_token'):
        token,word = lex()
        b_true, b_false = condition()
        if(token == 'rightBracket_token'):
            token,word = lex()
            #{P1}:
            r_true = b_true
            r_false = b_false
        else:
            print("SyntaxError :  expected ']' in line : " , line)
            exit(1)
    else:
        # R-> E1 relop E2 {P1}
        e1_place = expression()
        relop = relational_oper()
        e2_place = expression()

        #{P1}
        r_true = make_list(next_quad())
        gen_quad(relop, e1_place, e2_place, '_')
        r_false = make_list(next_quad())
        gen_quad('jump', '_', '_', '_')

    return r_true, r_false



def expression():
    global token,word,line
    # E -> T1(+/- T2 {P1}) *{P2}

    optional_sign()
    t1_place = term()
    while (token == 'plus_token' or token == 'minus_token'):
        plus_or_minus = add_oper()
        T2place = term()
        #{P1}
        w = new_temp()
        gen_quad(plus_or_minus, t1_place, T2place, w)
        t1_place = w
    #{P2}
    e_place = t1_place

    return e_place



def term():
    global token,word,line
    # T-> F1 ( (* or /) F2 {P1} )* {P2}

    f1_place = factor()
    while( token == 'multiply_token' or token == 'div_token'):
        mul_or_div = mul_oper()
        f2_place = factor()
        #{P1}
        w = new_temp()
        gen_quad(mul_or_div, f1_place, f2_place, w)
        f1_place = w
    #{P2}
    t_place = f1_place

    return t_place



def factor():
    global token,word,line

    if(token == 'number_token'):
        f_place = word
        token,word = lex()
    elif(token == 'leftParentheses_token'):
        token,word = lex()
        e_place = expression()
        if(token == 'rightParentheses_token'):
            f_place = e_place
            token,word = lex()
        else:
            print("SyntaxError :  expected ')' in line : " , line)
            exit(1)
    elif (token == 'id_token'):
        f_place = word
        token,word = lex()
        idtail(f_place)
    else:
        print("SyntaxError :  expected 'id error' or 'number' or 'expression' in line : " , line)
        exit(1)
    return f_place



def idtail(idName):
    global token,word,line,is_function

    if(token == 'leftParentheses_token'):
        is_function = 1
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
        print('Error: Missing = or < or <= or <> or >= or > in line ',line)
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



def create_int_file():
    global int_file

    for i in range(len(list_of_all_quads)):
        int_file.write(str(list_of_all_quads[i][0]))
        int_file.write(" ")
        int_file.write(str(list_of_all_quads[i][1]))
        int_file.write(" ")
        int_file.write(str(list_of_all_quads[i][2]))
        int_file.write(" ")
        int_file.write(str(list_of_all_quads[i][3]))
        int_file.write(" ")
        int_file.write(str(list_of_all_quads[i][4]))
        int_file.write("\n")



def create_c_file():
	global list_of_all_temp_var,list_of_all_quads

	if(len(list_of_all_temp_var)!=0):
		c_file.write("int ")
	for i in range(len(list_of_all_temp_var)):
		c_file.write(list_of_all_temp_var[i])
		if(len(list_of_all_temp_var) == i+1):
			c_file.write(";\n\n\t")
		else:
			c_file.write(",")

	for j in range(len(list_of_all_quads)):
		if(list_of_all_quads[j][1] == 'begin_block'):
			c_file.write("L_"+str(j+1)+":\n\t")
		elif(list_of_all_quads[j][1] == ":="):
			c_file.write("L_"+str(j+1)+": "+ list_of_all_quads[j][4]+"="+list_of_all_quads[j][2]+";\n\t")
		elif(list_of_all_quads[j][1] == "+" or list_of_all_quads[j][1] == "-" or list_of_all_quads[j][1] == "*" or list_of_all_quads[j][1] == "/"):
			c_file.write("L_"+str(j+1)+": "+ list_of_all_quads[j][4]+"="+list_of_all_quads[j][2]+""+list_of_all_quads[j][1]+"" +list_of_all_quads[j][3]+";\n\t")
		elif(list_of_all_quads[j][1] == "jump"):
			c_file.write("L_"+str(j+1)+": "+"goto L_"+str(list_of_all_quads[j][4])+ ";\n\t")
		elif(list_of_all_quads[j][1] == "<" or list_of_all_quads[j][1] == ">" or list_of_all_quads[j][1] == ">=" or list_of_all_quads[j][1] == "<="):
			c_file.write("L_"+str(j+1)+": "+"if ("+list_of_all_quads[j][2]+""+ list_of_all_quads[j][1] +""+list_of_all_quads[j][3]+") goto L_"+str(list_of_all_quads[j][4])+";\n\t")
		elif(list_of_all_quads[j][1] == "<>"):
			c_file.write("L_"+str(j+1)+": "+"if ("+str(list_of_all_quads[j][2])+"!="+str(list_of_all_quads[j][3])+") goto L_"+str(list_of_all_quads[j][4])+";\n\t")
		elif(list_of_all_quads[j][1] == "="):
			c_file.write("L_"+str(j+1)+": "+"if ("+list_of_all_quads[j][2]+"=="+list_of_all_quads[j][3]+") goto L_"+str(list_of_all_quads[j][4])+";\n\t")
		elif(list_of_all_quads[j][1] == "out"):
			c_file.write("L_"+str(j+1)+": "+"printf(\""+list_of_all_quads[j][2]+"= %d\", "+list_of_all_quads[j][2]+");\n\t")
		elif(list_of_all_quads[j][1] == 'halt'):
			c_file.write("L_"+str(j+1)+": {}\n\t")



token,word = lex()
c_file.write("int main(){\n\t")
program()
create_c_file()
create_int_file()
c_file.write("\n}")
c_file.close()
int_file.close()
ascFile.close()
#for i in range(len(list_of_all_quads)):
#	print (str(list_of_all_quads[i][0])+" "+str(list_of_all_quads[i][1])+" "+str(list_of_all_quads[i][2])+" "+str(list_of_all_quads[i][3])+" "+str(list_of_all_quads[i][4]))
