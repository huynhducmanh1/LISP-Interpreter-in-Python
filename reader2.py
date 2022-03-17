import re
import typestest as types

class Reader(): #Simple reader object to manipulate token: nextPosition() returns current token value and increment position, currentToken() is for returning token value at current position
    def __init__(self, tokens, position=0):
        self.tokens = tokens
        self.position = position

    def nextPosition(self):
        self.position += 1
        return self.tokens[self.position-1]

    def currentToken(self):
        if len(self.tokens) > self.position:
            return self.tokens[self.position]
        else:
            return None

def tokenize(str): #use regex to tokenize a string input into a Python list: ignore space, receive () for processing list later, symbol/number/nil
    tokenRE = re.compile(r"""[\s]*([()]|"(?:[\\].|[^\\"])*"?|;.*|[^\s\[\]{}()'"`@,;]+)""");
    return [token for token in re.findall(tokenRE, str)]

""" Test for tokenize
a = "(+ 2 3)"
b = "( abc  abc )"
c = "(+ 2 (* 3 4) )"
print(tokenize(a))
print(tokenize(b))
print(tokenize(c))
"""
def readString(input): 
    tokens = tokenize(input)
    return readForm(Reader(tokens)) #Call Reader object directly to parse a tokens (python list)

def readForm(reader): #if it is a list, call a function to process Lisp List. Otherwise, it is an atom 
    token = reader.currentToken() #get the current position's token
    if(token == ')'):
        raise Exception("Expect a beginning of list")
    elif(token == '('):
        return readList(reader)
    else:
        return readAtom(reader)

def readList(reader):
    thisList = []
    token = reader.nextPosition()
    token = reader.currentToken()
    while token != ')': #loop until end of LISP list
        if not token: 
            raise Exception("EOF before reaching end of list, lacking left parenthesis somewhere")
        thisList.append(readForm(reader))
        token = reader.currentToken()
    token = reader.nextPosition()
    return thisList

def readAtom(reader):
    intRE= re.compile(r"-?[0-9]+$") #because token is already a string, use regex to distinguish int/float/string for later evaluation
    floatRE = re.compile(r"-?[0-9][0-9.]*$")
    token = reader.nextPosition()
    if re.match(intRE, token):
        return types.NUMSXP(token)
    elif re.match(floatRE, token):
        return types.NUMSXP(int(token))
    elif token == "()":
        return types.SEXP("()")
    elif token == "T":
        return types.SEXP("T")
    else:
        return types.SYMSXP(token)
