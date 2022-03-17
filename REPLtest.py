
import typestest as types
import reader2, printer2
from pathlib import Path

#Declare NIL and TRUE as SEXP
NIL = types.SEXP("()")
TRUE = types.SEXP("T")

#Lexer and Parser:elminate white spaces, tokenize and put it into list of four main types: SEXP, NUMSXP, SYMSXP, List
def READ(input):
    return reader2.readString(input)

func_env = {}  #Create an empty Python dictionary of function, funcname: args, expr

#Evaluate and call eval_ast recursively for list evaluation
def EVAL(ast,env):
    if isinstance(ast,list) == False:
        return eval_ast(ast,env)
    else:
        if(len(ast)==0):
            return NIL
        elif ast[0].type == "Symbol":
            a0 = ast[0].symVal
            if a0 == "SET": #SET the variable name of variable to an expression's value
                if(ast[1].type == "Symbol"): 
                    a2 = EVAL(ast[2],env) #we get the value for the expression
                    repl_env[ast[1].symVal] = a2
                    return a2
                else: #cannot set variable name as other types other than string
                    raise Exception ("The variable name cannot be list or number, must be string")
            elif a0 == "IF": #IF command: if expr1 is NIL, then evaluate the exprF, vice versa
                expr1 = EVAL(ast[1],env)
                if expr1.type == "()":
                    return EVAL(ast[3],env)
                elif expr1.type == "T":
                    return EVAL(ast[2],env)
                else: return NIL
            elif a0 == "WHILE": #WHILE command: evaluate condition until NIL, return the result of expression in while loop
                while ((EVAL(ast[1], env)) != NIL):
                    result = EVAL(ast[2], env)
            elif a0 == "BEGIN": #BEGIN command: evaluate expr
                exprs = ast[1:]
                for expr in exprs:
                    EVAL(expr, repl_env)
            elif a0 == "DEFINE": #Define a function with ast[2] is the args, store the name of the function and the expr along with args to call later
                if(ast[1].type == "Symbol"):
                    if isinstance(ast[2],list):
                        for i in ast[2]:
                            if not i.type == "Symbol":
                                raise Exception("You cannot input args other than Symbol type")
                        func_env[ast[1].symVal] = [ast[2], ast[3]] 
                        # return "Function created"
                    else: 
                        raise Exception("The parameters can only be list type, cannot be empty list")
                else:
                    raise Exception("The function name cannot be other types other than string")
            elif a0 in func_env.keys():
                funcname = a0
                args = ast[1:] #by this we don't have to have another parenthesis around expressions
                return eval_func(funcname, args)
            elif a0 in env.keys():
                el = eval_ast(ast,env)
                f = el[0]
                return f(*el[1:])
            elif isinstance(ast,list):
                return ast
            elif not a0 in env.keys():
                raise Exception("wrong keyword for symbol")
            else:
                return ast
        else:
            return ast

#Evaluation when a function is called
def eval_func(funcname,args):
    x = func_env.get(funcname) #get args and expr value from the dictionary of functions
    x1 = x[0] #x1 is parsed as args, later on, exprs from call are evaluated and parsed to each args symbols
    x2 = x[1] #x2 is parsed as expression to be evaluated
    if len(args) > len(x1):
        raise Exception("You input more args/exprs that function can allow")
    elif len(args) < len(x1): 
        raise Exception("You didn't input enough args/exprs to be evaluated with this function, neeed "+len(x1))
    else: 
        for i in range(len(args)):
            result = EVAL(args[i],repl_env) #Evaluate the expressions from call first
            repl_env[x1[i].symVal] = result #set the symbols to the result of according called expr
    resultEXPR = EVAL(x2, repl_env) #now we evaluate the expr that is in the function
    return resultEXPR 



#Evaluate
def eval_ast(ast,env):
    if isinstance(ast, list):
        return types._list(*map(lambda a: EVAL(a, env), ast))
    elif ast.type == "Symbol":
        if ast.symVal in env.keys(): #Check if ast is for calculations/special symbols
            return env.get(ast.symVal)
        else: return ast  
    else:
        return ast

#Print handles each type: if it is (), t, SEXP, NUMXSP, SYMSXP
def PRINT(input):
    return printer2.printObject(input)

#A Read-Evaluate-Print function
def REP(input):
    ast = READ(input)
    result = EVAL(ast,repl_env)
    return print(PRINT(result))

#Basic calculation
def normalOP(key, x, y):
    result = 0
    if(x.type == "Symbol" or x.type == "Symbol"): raise Exception("Cannot be symbol, must be number")
    if(key == '+'): result = int(x.intval) + int(y.intval)
    elif(key == '-'): result = int(x.intval) - int(y.intval)
    elif(key == '*'): result = int(x.intval) * int(y.intval)
    elif(key == '/'): result = int(int(x.intval) / int(y.intval))
    elif(key == '%'): result = int(int(x.intval) % int(y.intval))
    return types.NUMSXP(result)

#check if greater or smaller
def compareOP(key, x, y):
    if(x.type == "Symbol" or x.type == "Symbol"): raise Exception("Cannot be symbol, must be number")
    if(key == '>'):
        if int(x.intval) > int(y.intval):
            return TRUE
        else: return NIL
    elif(key == '<'):
        if int(x.intval) < int(y.intval):
            return TRUE
        else: return NIL
    else: return NIL

#check if equal ('=')
def isEqual( x, y):
    if(isinstance(x,list) and isinstance(y,list)):
        if len(x) == len(y): return TRUE
        else: return NIL
    elif(isinstance(x, list) or isinstance(y,list)):
        return NIL
    elif(x.type == "()" and y.type == "()"):
        return TRUE
    elif( x.type == "T" and y.type == "T"):
        return TRUE
    elif x.type == "Number" and y.type == "Number":
        if(int(x.intval) == int(y.intval)):
            return TRUE
        else: return NIL
    elif x.type == "Symbol" and y.type == "Symbol":
        if(x.symVal == y.symVal):
            return TRUE
        else: return NIL
    else: return NIL

#Join two Sexpression as (x y)
def CONS(x, y):
    return types.List([x]) + types.List([y])


def specialSymbol(op, x):
    if op == 'CAR':
        if not (isinstance(x,list)):
            raise Exception("CAR can only work with List")
        elif (isinstance(x , list)):
            if len(x) == 0:
                raise Exception("CAR cannot work with empty List")
            else:
                return x[0]
    if op == 'CDR':
        if not (isinstance(x,list)):
            raise Exception("CDR can only work with List")
        elif (isinstance(x , list)):
            if len(x) == 0:
                raise Exception("CDR cannot work with empty List")
            else:
                return x[1:]
    elif(op == 'NUMBER?'):
        if isinstance(x, list):
            return NIL
        elif(x.type == "Number"):
            return TRUE
        else: return NIL
    elif(op == 'SYMBOL?'):
        if isinstance(x, list):
            return NIL
        if(x.type == "Symbol"):
            return TRUE
        else: return NIL
    elif(op == 'NULL?'):
        if x.type == NIL.type:
            return TRUE
        else: return NIL
    elif(op == 'LIST?'):
        if(isinstance(x, list)):
            return TRUE
        else: return NIL
    elif(op == 'PRINT'):
        result = printer2.printObject(x)
        return print(result)
    else: return NIL
        

#Environment
repl_env = {'+': lambda x,y: normalOP('+',x,y),
            '-': lambda x,y: normalOP('-',x,y),
            '*': lambda x,y: normalOP('*',x,y),
            '/': lambda x,y: normalOP('/', x,y),
            '%': lambda x,y: normalOP('%', x, y), #this one is for fizzbuzz test
            '>': lambda x,y: compareOP('>', x ,y),
            '<': lambda x,y: compareOP('<', x ,y),
            '=': lambda x,y: isEqual(x, y),
            'CAR': lambda x: specialSymbol('CAR',x),
            'CDR': lambda x: specialSymbol('CDR',x), 
            'CONS': lambda x,y: CONS(x,y),
            'NUMBER?': lambda x: specialSymbol('NUMBER?', x),
            'SYMBOL?': lambda x: specialSymbol('SYMBOL?', x),
            'LIST?': lambda x: specialSymbol('LIST?', x),
            'NULL?': lambda x: specialSymbol('NULL?', x),
            'PRINT': lambda x: specialSymbol('PRINT', x)
        }

#to know that symbols are valid for calculation
# def isDict(key): 
#     Symbols = ['+', '-', '*', '/','=','>','<',
#                 'SYMBOL?', 'NUMBER?','LIST?', 'NULL?', 'PRINT', 
#                 'CAR', 'CONS', 'CDR',
#                 'BEGIN','IF','WHILE','SET', 'DEFINE', 'FUNNAME']
#     if key in Symbols: return True
#     else: return False
def REPL():
    print("You can input exit to quit the interactice mode (or Ctrl+C)")
    while True:   
        prompt = input("manh> ") #If none reported as some commands does not return result, return blank line
        if prompt == "": continue
        if prompt == "exit":
            exit()
        REP(prompt)

def readTest():
    print("I have two tests file: test.txt (for testing all command) and fizzbuzz.txt (simple fizzbuzz program)")
    print("test.txt is in format of: [command]: [output]")
    print("fizzbuzz.txt will just output the fizzbuzz program")

    prompt= input("Input 1 for test.txt and 2 for fizzbuzz.txt: ")        
    if prompt == '1':
        p = Path(__file__).with_name('test.txt')
        with open(p) as file:
            for line in file:
                line1 = line.strip()
                print(line1, end=': ')
                REP(line)
    elif prompt == '2':
        p = Path(__file__).with_name('fizzbuzz.txt')
        with open(p) as file:
            data = file.read().replace('\n', '')
            REP(data)
            REP("(FIZZBUZZ 1)")
    else: 
        print("Wrong input")



print("Welcome to Manh's LISP interpreter in python")
print("Input 1 for read file test mode, 2 for interactive mode, 3 for exit")
prompt = input("Please input your choice: ")
boo = True
while(boo == True):
    if prompt == '1':
        readTest()
        boo = False
    elif prompt == '2':
        REPL()
    elif prompt == '3':
        print("See you again")
        exit()
    else:
        print("Wrong output")



#REPL loop for interactive mode



