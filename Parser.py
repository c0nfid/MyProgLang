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
            return self.parsVarOrNumb();
    def parseFormula(self):
        leftNode = self.parseParenthes()
        operator = self.match([ListTokenType.PLUS, ListTokenType.MINUS])
        while operator:
            rightNode = self.parseParenthes()
            leftNode = BinOperationNode(operator, leftNode, rightNode)
            operator = self.match([ListTokenType.PLUS, ListTokenType.MINUS])
        return leftNode

    def parseExpression(self):
        if(self.match([ListTokenType.VAR])):
            self.pos -=1
            varNode = self.parsVarOrNumb()
            assignOperator = self.match([ListTokenType.ASSIGN])
            if assignOperator:
                rightFormulNode = self.parseFormula()
                binaryNode = BinOperationNode(assignOperator, varNode, rightFormulNode)
                return binaryNode
        return None

    def parseCode(self):
        root = StatementsNode()
        while self.pos < len(self.tokens):
            codeStringNode = self.parseExpression()
            self.require([ListTokenType.SEMICOLON])
            root.addNode(codeStringNode)
        return root


def run_Parser():
    text = '''for (i = 03; i < n; i += 35){
    l = 4534534536.234564563453453453453453
}
if (i < 3){
    i++
}'''
    tes = 'a = a - (a + 5);'
    a = Parser(run(tes))

    print(a.tokens[0].type.name)
    #print(a.match([ListTokenType.FOR]))
    l = a.parseCode()
    for i in l.codeStrings:
        print(i.rightNode.rightNode.operator.text)



#def runable(node):
#    if type(node) == NumberNode:
#        return parseInt(node.number.text)

run_Parser()