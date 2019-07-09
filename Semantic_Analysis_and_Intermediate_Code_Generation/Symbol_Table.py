global symbolTable

def initSymTable():
    global symbolTable
    symbolTable = {}
    return symbolTable

def addSymbol(x):
    if symbolTable.setdefault(x, [None, None]) == None:
        return False
    return True

def addAttributeToSymbol(x, att, value):
    temp = symbolTable[x]
    if att is 1:
        temp[0] = value
    elif att is 2:
        temp[1] = value
    symbolTable[x] = temp

def symbolInTable(x):
    if x in symbolTable:
        print(x)
        return True
    print(str(x)+' : Not in the table!')
    return False

def getSymbol(x):
    if x in symbolTable:
        print(str(x) + ' : '+ str(symbolTable[x]))
        return symbolTable
    print(str(x) +' : None')
    return None

def main():
    initSymTable()




    #
    # addSymbol('temperature')
    # addSymbol('velocity')
    # addSymbol('temp')
    #
    # symbolInTable('temperature')
    # symbolInTable('bang')
    #
    # addAttributeToSymbol('temperature', 1, 'int')
    # addAttributeToSymbol('temperature', 2, 0x800000)
    # addAttributeToSymbol('velocity', 1, 'float')
    # addAttributeToSymbol('velocity', 2, 0x800020)
    # addAttributeToSymbol('temp', 1, 'array')
    # addAttributeToSymbol('temp', 2, 0x800040)
    #
    # getSymbol('temperature')
    # getSymbol('velocity')
    # getSymbol('bang')



if __name__ == '__main__':
    main()