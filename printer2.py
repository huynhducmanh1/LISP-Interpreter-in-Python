
import typestest as types

def printObject(object):
    if isinstance(object, list) == True:
        return "(" + " ".join(map(lambda e: printObject(e), object)) + ")" #because we don't append '()' to thisList, so we have to manually join it here
    elif(isinstance(object, types.SEXP)):
        if object.type == "()":
            return "()"
        elif object.type == "T":
            return "T"
        elif(isinstance(object, types.NUMSXP)):
            return object.intval
        elif(isinstance(object, types.SYMSXP)):
            return object.symVal
    elif str(object) == "None":
        return ""
    else:
        return object.__str__()