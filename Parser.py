from Lex import *
from Node import *


class Parser:
    tokens = []  # Token[]
    pos = 0
    scope = {}

    def __init__(self, tokens):
        self.tokens = tokens

    def match(self, expected):
        if (self.pos < len(self.tokens)):
            currentToken = self.tokens[self.pos]
            if currentToken.type in expected:
                self.pos += 1
                return currentToken
        return None

    def require(self, expected):
        token = self.match(expected)
        if (token == None):
            print('requereError', expected[0].name)
        else:
            return token
        return None

    def parsVarOrNumb(self):
        number = self.match([ListTokenType.INT, ListTokenType.FLOAT])
        if number:
            return NumberNode(number)

        var = self.match([ListTokenType.VAR])
        if var:
            return VariableNode(var)
        print('VarOrNumbERROR')

    def parseParenthes(self):
        if self.match([ListTokenType.LPAREN]):
            node = self.parseFormula()
            self.require([ListTokenType.RPAREN])
            return node
        else:
            return self.parsVarOrNumb()

    def parseFormula(self):
        leftNode = self.parseParenthes()
        operator = self.match([ListTokenType.PLUS, ListTokenType.MINUS])
        while operator:
            rightNode = self.parseParenthes()
            leftNode = BinOperationNode(operator, leftNode, rightNode)
            operator = self.match([ListTokenType.PLUS, ListTokenType.MINUS])
        return leftNode

    def parseLoopCondition(self):
        if self.require([ListTokenType.LPAREN]) == None:
            return None
        if (self.match([ListTokenType.VAR])):
            self.pos -= 1
            varNode = self.parsVarOrNumb()
            assignOperator = self.match([ListTokenType.ASSIGN])
            if assignOperator:
                rightFormulNode = self.parseFormula()
                binaryNode = BinOperationNode(assignOperator, varNode, rightFormulNode)
            else:
                print("Error Assign syntax")
                return None
        else:
            print("ErrorStartLoop Syntax")
            return None
        if self.require([ListTokenType.SEMICOLON]) == None:
            print("ErrorSemicolon" + self.pos -1)
            return None

        leftNode = self.parsVarOrNumb()
        operator = self.match([ListTokenType.SIGNMORE, ListTokenType.SIGNLESS])
        stop = BinOperationNode(operator, leftNode, self.parsVarOrNumb())

        if self.require([ListTokenType.SEMICOLON]) == None:
            print("ErrorSemicolon" + self.pos -1)
            return None
        step = self.match([ListTokenType.INT])
        if self.require([ListTokenType.RPAREN]) == None:
            return None
        return Condition(binaryNode, stop, step)

    def parseCondition(self):
        if self.require([ListTokenType.LPAREN]) == None:
            return None

        leftNode = self.parsVarOrNumb()
        operator = self.match([ListTokenType.SIGNMORE, ListTokenType.SIGNLESS, ListTokenType.NEQUAL])
        stop = BinOperationNode(operator, leftNode, self.parsVarOrNumb())

        if self.require([ListTokenType.RPAREN]) == None:
            return None

        return Condition(None, stop, None)

    def parseBody(self):
        if self.require([ListTokenType.FLPAREN]) == None:
            return None
        body = []
        while (self.match([ListTokenType.FRPAREN]) == None):
            if self.match([ListTokenType.NEWLINE]) == None:
                pass
            if self.match([ListTokenType.FRPAREN]):
                return body
            bodyNode = self.parseExpression()
            if bodyNode == None:
                return None
            body.append(bodyNode)
        return body


    def parseExpression(self):
        if (self.match([ListTokenType.VAR])):
            self.pos -= 1
            varNode = self.parsVarOrNumb()
            assignOperator = self.match([ListTokenType.ASSIGN])
            if assignOperator:
                rightFormulNode = self.parseFormula()
                binaryNode = BinOperationNode(assignOperator, varNode, rightFormulNode)
                return binaryNode

        elif self.match([ListTokenType.FOR]):
            self.pos -= 1
            keyToken = self.match([ListTokenType.FOR])
            condition = self.parseLoopCondition()
            body = self.parseBody()
            return LoopNode(keyToken, condition, body)

        elif self.match([ListTokenType.WHILE]):
            self.pos -= 1
            keyToken = self.match([ListTokenType.WHILE])
            condition = self.parseCondition()
            body = self.parseBody()
            return LoopNode(keyToken, condition, body)

        return None


    def parseCode(self):
        root = StatementsNode()
        while self.pos < len(self.tokens):
            codeStringNode = self.parseExpression()
            self.match([ListTokenType.NEWLINE]) #skip newline tokens after node
            #self.require([ListTokenType.SEMICOLON])
            root.addNode(codeStringNode)
        return root


def run_Parser():
    text = '''for (i = 3; i < n; 35){
     for (i = 6; i < j; 3){
        ggdsjdsk = 2234
     } 
     b = 5
     }
     while (a != 5) {
        g = 7
     }
     a = 3
     fuyuf = a + 789 - 89 + 90'''
    tes = 'a = a - (a + 5)'
    a = Parser(run(text))

    #print(a.tokens[0].type.name)
    l = a.parseCode()
    for i in l.codeStrings:
        print(i)


# def runable(node):
#    if type(node) == NumberNode:
#        return parseInt(node.number.text)

run_Parser()
