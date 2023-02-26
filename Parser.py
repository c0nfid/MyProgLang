from Lex import *
from Node import *


class Parser:

    def __init__(self, tokens):
        self.pos = 0
        self.scope = {}
        self.tokens = tokens
        print(tokens)

    def match(self, expected):
        if self.pos < len(self.tokens):
            currentToken = self.tokens[self.pos]
            if currentToken.type in expected:
                self.pos += 1
                return currentToken
        return None

    def require(self, expected):
        token = self.match(expected)
        if token == None:
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
        operator = self.match(
            [ListTokenType.PLUS, ListTokenType.MINUS, ListTokenType.SIGNLESS, ListTokenType.SIGNMORE, ListTokenType.ADD,
             ListTokenType.DIV])
        while operator:
            rightNode = self.parseParenthes()
            # opp = self.match([ListTokenType.PLUS, ListTokenType.MINUS, ListTokenType.SIGNLESS, ListTokenType.SIGNMORE, ListTokenType.ADD, ListTokenType.DIV])
            # if opp == ListTokenType.ADD or opp == ListTokenType.DIV:
            #    leftNode = BinOperationNode(operator, leftNode, rightNode)
            leftNode = BinOperationNode(operator, leftNode, rightNode)
            operator = self.match(
                [ListTokenType.PLUS, ListTokenType.MINUS, ListTokenType.SIGNLESS, ListTokenType.SIGNMORE,
                 ListTokenType.ADD, ListTokenType.DIV])
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
            raise Exception("Require Semicolon")
            # print("ErrorSemicolon" + self.pos -1)
            # return None

        leftNode = self.parsVarOrNumb()
        operator = self.match([ListTokenType.SIGNMORE, ListTokenType.SIGNLESS])
        stop = BinOperationNode(operator, leftNode, self.parsVarOrNumb())

        if self.require([ListTokenType.SEMICOLON]) == None:
            print("ErrorSemicolon" + self.pos - 1)
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

        elif self.match([ListTokenType.IF]):
            self.pos -= 1

            keyToken = self.match([ListTokenType.IF])

            condition = self.parseCondition()
            body = self.parseBody()
            return ifNode(condition, body, None)

        elif self.match([ListTokenType.PRINT]):
            self.pos -= 1
            operator = self.match([ListTokenType.PRINT])
            if self.require([ListTokenType.LPAREN]) == None:
                return None
            operand = self.parseFormula()
            if self.require([ListTokenType.RPAREN]) == None:
                return None

            return UnarOperationNode(operator, operand)

        return None

    def parseCode(self):
        root = StatementsNode()
        while self.pos < len(self.tokens):
            codeStringNode = self.parseExpression()
            self.match([ListTokenType.NEWLINE])  # skip newline tokens after node
            # self.require([ListTokenType.SEMICOLON])
            root.addNode(codeStringNode)
        return root

# def runable(node):
#    if type(node) == NumberNode:
#        return parseInt(node.number.text)

# run_Parser()
