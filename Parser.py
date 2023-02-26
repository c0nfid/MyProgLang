from Lex import *
from Nodes import *

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
        number = self.match([TokenList['INT'], TokenList['FLOAT']])
        if number:
            return NumberNode(number)

        var = self.match([TokenList['VAR']])
        if var:
            return VarNode(var)
        print('VarOrNumbERROR')

    def parseParenthes(self):
        if self.match([TokenList['LPAREN']]):
            node = self.parseFormula()
            self.require([TokenList['RPAREN']])
            return node
        else:
            return self.parsVarOrNumb()

    def parseFormula(self):
        leftNode = self.parseParenthes()
        operator = self.match([TokenList['PLUS'], TokenList['MINUS']])
        while operator:
            rightNode = self.parseParenthes()
            leftNode = BinOperationNode(operator, leftNode, rightNode)
            operator = self.match([TokenList['PLUS'], TokenList['MINUS']])

        return leftNode

    def parseExpression(self):
        if(self.match([TokenList['VAR']])):
            self.pos -=1
            varNode = self.parsVarOrNumb()
            assignOperator = self.match([TokenList['ASSIGN']])
            if assignOperator:
                rightFormulNode = self.parseFormula()
                binaryNode = BinOperationNode(assignOperator, varNode, rightFormulNode)
                return binaryNode
        return None

    def parseCode(self):
        root = RootNode()
        while self.pos < len(self.tokens):
            codeStringNode = self.parseExpression()
            root.addNode(codeStringNode)
        return root


def run_Parser():
    tes = 'a = 5 - 5'
    a = Parser(run(tes))


    l = a.parseCode()
    for i in l.codeNodes:
        print(i.right)


run_Parser()