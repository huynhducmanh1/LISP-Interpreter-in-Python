
#A data structure for S-expression
class SEXP:
    def __init__(self, type: str) :
        self.type = type

#A data structure for Number (int) that reports its type to super class SEXP
class NUMSXP(SEXP) :
    def __init__(self, intval: int):
        super().__init__("Number")
        self.intval = intval

#data strucuture for Symbol (str) that reports its type to super class SEXP
class SYMSXP(SEXP): 
    def __init__(self,symVal:str):
        super().__init__("Symbol")
        self.symVal = symVal



#A normal data structure for LISP list, check if list by PYTHON isinstance method
class List(list):
    def __add__(self, rhs): 
        return List(list.__add__(self, rhs))
    def __getitem__(self, i):
        if type(i) == slice: 
            return List(list.__getitem__(self, i))
        elif i >= len(self): 
            return None
        else:                
            return list.__getitem__(self, i)
    def __getslice__(self, *a): 
        return List(list.__getslice__(self, *a))

def _list(*vals): return List(vals)

def _isList(expr):
    if isinstance(expr,list):return True
    else: return False



