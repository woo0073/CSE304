#!/usr/bin/env python
# coding: utf-8

# In[159]:
import sys


Punctuation ={
    ";": "SEMICOLON", "(" : "LPAREN", ")" : "RPAREN",   "," : "COMMA",  "{" : "LBRACE", "}" : "RBRACE",
    "[" : "LBRACKET", "]" :"RBRACKET"
}
Operators ={"=" : "ASSIGN", "<" : "LT", ">"  : "GT", "==" : "EQ",
    "+" : "PLUS", "-" : "MINUS", "*" : "MULT", "/" : "DIV", "!" : "NOT", "&&" : "AND", "||" : "OR"}

Keywords = {"int" : "INT", "float" : "FLOAT", "if" : "IF", "else" : "ELSE", "while" : "WHILE", "read" : "READ", "print" : "PRINT"}



otherType = ["NONE", "ID", "ICONST", "FCONST"]


# In[160]:


lineOFcode = ""
token = ""
tType = "NONE"
cur = ""

#comment = False


# In[161]:


def nextToken():
    global token
    global cur
    global tType
    global lineOFcode
    token = ''
    tokenIndex = 0
    num = 0
    # cur = lineOFcode[tokenIndex]

    while (isSpace(cur)):
        tokenIndex += 1
        cur = lineOFcode[tokenIndex]

    if(isDigit(cur)):
        while(isDigit(cur)):
            token += cur
            tokenIndex += 1
            cur = lineOFcode[tokenIndex]
        
        num = int(token)
        tType = 'ICONST'
        if(cur == '.'):
            token += cur
            tokenIndex += 1
            cur = lineOFcode[tokenIndex]
            while(isDigit(cur)):
                token += cur
                tokenIndex += 1
                cur = lineOFcode[tokenIndex]
            
            num = float(token)
            tType = 'FCONST'
          
    
    elif(isAlpha(cur)):
        while(isAlpha(cur) or isDigit(cur)):
            token += cur
            tokenIndex += 1
            cur = lineOFcode[tokenIndex]
        
        if(isKeyword(token)):
            tType = Keywords[token]
        
        else:
            if token == 'const':
                nextToken()
                if token == 'int':
                    tType = 'ICONST'
                elif token == 'float':
                    tType = 'FCONST'
                else:
                    return False
            else: 
                tType = "ID"
        
    
    elif(isOperation(cur)):
        if cur in '|&=' and len(lineOFcode) > 1:
            before = cur
            tokenIndex += 1
            cur = lineOFcode[tokenIndex]
            if cur in '|&=':
                before = before + cur
                tokenIndex += 1
                cur = lineOFcode[tokenIndex]
            token = before
            tType = Operators[token]

        else:
            token = cur
            tType = Operators[token]
            tokenIndex += 1
            cur = lineOFcode[tokenIndex]


    elif(isPunctuation(cur)):
        tType = Punctuation[cur]
        token = cur
        tokenIndex += 1
        cur = lineOFcode[tokenIndex]


    else:
        print("INVALID")
        return False
    
    #
    while(isSpace(cur)):
        tokenIndex += 1
        if(len(lineOFcode) <= 2):
            tokenIndex = 0
            return True
        cur = lineOFcode[tokenIndex]
    

    # print(str(token)+ " : "+ tType+"\n")
    # cut off the list, codeOFline
    if(tokenIndex != 0):
        lineOFcode = lineOFcode[tokenIndex:]
    
    return True


# In[162]:

def isPunctuation(cur):
    return cur in Punctuation

def isSpace(cur):
    return cur in ["\n", " ", "\t"]


# In[163]:


def isDigit(cur):
    return cur in '0123456789'


# In[164]:


def isOperation(cur):
    return cur in Operators


# In[165]:


def isKeyword(cur):
    return cur in Keywords


# In[166]:


def isAlpha(cur):
    return  cur.isalpha()
        


# In[167]:


def arraydimtail():
    global token
    print("arraydimtail -> ", end = "")
    if tType in ["ID", "ICONST"]:
        print(tType+" ", end = "")
        nextToken()   
        if tType == "RBRACKET":
            print(Punctuation[token])
            nextToken()
        else:
            raise Exception( "RBRACKET is needed" )
            # print("INVAILD")
            # nextToken()
    else:
        print("INVAILD")
        nextToken()
        


# In[168]:


def arraydim():
    global token
    if tType == "LBRACKET": # arraydim -> LBRACKET arraydimtail 
        print("arraydim -> " + Punctuation[token] + " arraydimtail")
        nextToken()
        arraydimtail()
    return True
        


# In[169]:


def variabletail():
    global token
    print("variabletail -> ", end = "")
    if token is not "[":
        print("e")# variabletail -> ε
        # if token is '=':
        #     nextToken()

    else:
        print("arraydim")# variabletail -> arraydim
        arraydim()
    return True 
        


# In[170]:


def variable():
    global token
    if tType == "ID":
        print("variable -> " +tType + " variabletail")
        nextToken()
        variabletail()
    else:
        nextToken()
        print("INVALID")


# In[171]:


def variablelist():
    global token
    print("variablelist -> variable variablelisttail")
    variable()
    variablelisttail()


# In[172]:


def variablelisttail():
    global token
    print("variablelisttail -> ", end = "")
    if tType == "COMMA":
        print(Punctuation[token]+" variable variablelisttail")
        nextToken()
        variable()
        variablelisttail()
    elif tType == "SEMICOLON":
        print(Punctuation[token])
        nextToken()
    else:
        nextToken()
        nextToken()
        if tType == "SEMICOLON":
            print(Punctuation[token])
            nextToken()
        else:
            raise Exception('SEMICOLON is needed!')
    return True
        


# In[173]:


def typespec():
    global token
    print("typespec -> ", end = "")
    if token == "int":
        print("INT")
        nextToken()
    elif token == "float":
        print("FLOAT")
        nextToken()
        return True
    else:
        print("INVALID")
        nextToken()
        return False


# In[174]:


def decl():
    global token
    print("decl -> typespec variablelist")
    typespec()
    variablelist()
    return True


# In[175]:


def decllist():
    global token
    print("decllist -> ", end = "")
    if token == "{": # -> ε
        print("e")
    elif token in Keywords:
        print("decl declist")
        decl()
        decllist()
    else:
        return True
        
    


# In[176]:


def statement():
    global token
    print("statement -> ", end = "")
    if token == 'while':
        nextToken()
        print('whilestatement')
        whilestatement()
    elif token == "if":
        print('ifstatement')
        nextToken()
        ifstatement()
    elif token == "read":
        print('readstatement')
        nextToken()
        readstatement()
    elif token == "print":
        nextToken()
        print('printexpression')
        printexpression()
    else:
      #  nextToken()
        print('assignmentexpression')
        assignmentexpression()


# In[177]:


def whilestatement():
    global token
    print('whilestatement -> WHILE condexpr whiletail')
    condexpr()
    whiletail()
    


# In[178]:


def condexprtail():
    global token
    if token in Operators:
        print('condexprtail -> '+ Operators[token] + ' vorc')
        nextToken()
        vorc()
    else:
        print("INVALID")
    
        


# In[179]:


def condexpr():
    global token
    print('condexpr -> ', end = "")
    if token == '(':
        print('LPAREN vorc condexprtail RPAREN')
        nextToken()
        vorc()
        condexprtail()
        if token == ')':
            nextToken()
        else:
            print("INAVLID")
            nextToken()
    elif token == 'NOT':
        print('NOT condexprtail')
        nextToken()
        condexpr()
    else:
        print(' vorc condexprtail')

        condexprtail()
    


# In[180]:


def vorc():
    global token
    global tType
    if tType == ('ICONST' or 'FCONST'):
        print('vorc -> '+tType)
        nextToken()
    else:
        print('vorc -> variable')
        variable()


# In[181]:


def whiletail():
    global token
    print('whiletail -> compoundstatement')
    compoundstatement()


# In[182]:


def compoundstatement():
    global token
    print('compoundstatemnet -> LBRACE statementlist RBRACE')
    if token == "{":
        nextToken()
        statementlist()
        # if token != "}":
        #     print("INVALID")
        nextToken()
    else:
        print("INVALID")
        nextToken()
        


# In[183]:


def ifstatement():
    global token
    print("ifstatement -> IF condexpr compoundstatement istail")
    condexpr()
    compoundstatement()
    istail()


# In[184]:


def istail():
    global token
    if token == "else":
        print('istail -> ELSE compoundstatement')
        nextToken()
        compoundstatement()
    elif token == "}":
        print('istail -> e')
    else:
        print("INVALID")



# In[185]:


def readstatement():
    global token
    print('readstatement -> READ variable')
    variable()
    return True
    


# In[186]:


def printexpression():
    global token
    print('printexpression -> PRINT variable')
    variable()
    return True
    
        


# In[187]:


def assignmentexpression():
    global token
    print('assignmentexpression -> variable ASSIGN otherexpression')
    variable()
    if token == '=':
        nextToken()
    otherexpression()
        


# In[188]:


def otherexpression():
    global token
    print('otherexpression -> term otherexpressiontail')
    term()
    otherexpressiontail()
    
    


# In[189]:


def otherexpressiontail():
    global token
    if token in '+-':
        print('otherexpression-> ' +Operators[token] +' term otherexpressiontail')
        nextToken()
        term()
        otherexpressiontail()
    else:
        print('otherexpressiontail-> e' )
        # if token != ";":
        #     print("INVALID")





# In[190]:


def term():
    global token
    print('term -> factor termtail')
    factor()
    termtail()


# In[191]:


def factor():
    global token
    if tType in ["ICONST","FCONST"]:
        print('factor -> '+ tType)
        nextToken()
    elif token == '(':
        print('factor -> LPAREN otherexpression RPAREN')
        nextToken()
        otherexpression()
        if token == ')':
            nextToken()
        else:
            print("INVALID")
    elif token == '-':
        print('factor -> MINUS factor')
        nextToken()
        factor()
    else:
        print('factor -> variable')
        variable()
        


# In[192]:


def termtail():
    global token
    if token in '*/':
        print('termtail -> ' + Operators[token] + ' factor termtail')
        nextToken()
        factor()
        termtail()
    elif (token in Operators) or (token in Punctuation):
        print('termtail -> e')

    else:
        raise Exception('Operators is needed')
    


# In[193]:


def statementlist(): 
    global token
    print("statementlist -> statement SEMICOLON statementlist")
    statement()
    if tType == 'SEMICOLON':  
        nextToken()
        if token == "}":
            print("statementlist -> e")
            return
        statementlist()
    else:
        print("statementlist -> e")



# In[194]:


def bstatementlist():
    global token
    print("bstatementlist -> ", end = "")
    if tType == "LBRACE":
        print("LBRACE statementlist RBRACE")
        nextToken()
        statementlist() #  -> ε
        
        if tType == "RBRACE":
            print("Done")

        


# In[195]:


def program():
    global token
    print("program -> decllist bstatementlist DD")
    decllist()
    bstatementlist()
    return True
        


# In[196]:


def initLexer(fileName):
    f = open(fileName, "r")
    global lineOFcode
    global token
    global cur
    cur = '' # current char
    lineOFcode = f.read()
    cur = lineOFcode[0]
    nextToken()
    program()
    f.close()
#
def main():
    try:
        initLexer(sys.argv[1])
    except Exception as e:
        print("You must provide a valid filename as parameter")
        raise

if __name__ == '__main__':
    main()


# def main():
#     initLexer('T51_rascl_test_err2.rsc')
# if __name__ == '__main__':
#     main()
