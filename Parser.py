from Lex import *
from Nodes import *

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens #Token[]
        self.pos = 0

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

    def parseVariableOrNumbers(self):
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
            if self.match([TokenList['MULTIPLY']]):
                self.pos -= 1
                operator = self.match([TokenList['MULTIPLY']])
                rightNode = self.parseParenthes()
                node = BinOperationNode(operator, node, rightNode)
            return node
        elif self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1].type == TokenList['MULTIPLY']:
            leftNode = self.parseVariableOrNumbers()
            operator = self.match([TokenList['MULTIPLY']])
            rightNode = self.parseParenthes()
            return BinOperationNode(operator, leftNode, rightNode)
        else:
            return self.parseVariableOrNumbers()

    def parseFormula(self):
        leftNode = self.parseParenthes()
        operator = self.match([TokenList['PLUS'], TokenList['MINUS'], TokenList['<'], TokenList['>'], TokenList['MULTIPLY'], TokenList['DIV']])
        while operator:
            rightNode = self.parseParenthes()
            leftNode = BinOperationNode(operator, leftNode, rightNode)
            operator = self.match([TokenList['PLUS'], TokenList['MINUS'], TokenList['<'], TokenList['>'], TokenList['MULTIPLY'], TokenList['DIV']])

        return leftNode

    def parseCondition(self, loop_type):
        if self.require([TokenList['LPAREN']]) is None:
            return None

        if loop_type.type == TokenList['FOR']:
            if self.match([TokenList['VAR']]):
                self.pos -= 1

                var_node = self.parseVariableOrNumbers()
                assign = self.match([TokenList['ASSIGN']])

                if assign:
                    right_node = self.parseFormula()
                    start = BinOperationNode(assign, var_node, right_node)
                else:
                    print("Error Assign syntax")
                    return None

            else:
                print("ErrorStartLoop Syntax, require")
                return None

            if self.require([TokenList['SEMICOLON']]) is None:
                print("ErrorSemicolon" + self.pos - 1)
                return None
        else:
            start = None

        left_node = self.parseVariableOrNumbers()
        stop = BinOperationNode(self.match([TokenList['<'], TokenList['>'], TokenList['!=']]), left_node, self.parseVariableOrNumbers())

        if loop_type.type == TokenList['FOR']:
            if self.require([TokenList['SEMICOLON']]) is None:
                print("ErrorSemicolon" + self.pos - 1)
                return None

            step = self.match([TokenList['INT']])
        else:
            step = None

        if self.require([TokenList['RPAREN']]) is None:
            return None

        return LoopConditionNode(start, stop, step)

    def parseBody(self):
        if self.require([TokenList['FLPAREN']]) == None:
            return None
        body = []

        while (self.match([TokenList['FRPAREN']]) == None):
            if self.match([TokenList['NEWLINE']]) == None:
                pass
            if self.match([TokenList['FRPAREN']]):
                return body

            bodyNode = self.parseExpression()
            if bodyNode == None:
                return None
            body.append(bodyNode)

        return body

    def parseExpression(self):
        if(self.match([TokenList['VAR']])):
            self.pos -=1
            varNode = self.parseVariableOrNumbers()
            assignOperator = self.match([TokenList['ASSIGN']])
            if assignOperator:
                rightFormulNode = self.parseFormula()
                binaryNode = BinOperationNode(assignOperator, varNode, rightFormulNode)
                return binaryNode

        elif self.match([TokenList['FOR'], TokenList['WHILE'], TokenList['IF']]):
            self.pos -= 1
            key_token = self.match([TokenList['FOR'], TokenList['WHILE'], TokenList['IF']])
            condition = self.parseCondition(key_token)
            body = self.parseBody()
            if key_token.type == TokenList['IF']:
                return ConditionalNode(key_token, condition, body)

            return LoopNode(key_token, condition, body)

        elif self.match([TokenList['PRINT']]):
            self.pos -=1
            operator = self.match([TokenList['PRINT']])
            if self.require([TokenList['LPAREN']]) == None:
                return None
            operand = self.parseFormula()
            if self.require([TokenList['RPAREN']]) == None:
                return None

            return CommNode(operator, operand)
        return None

    def parseCode(self):
        root = RootNode()
        while self.pos < len(self.tokens):
            codeStringNode = self.parseExpression()
            self.match([TokenList['NEWLINE']])  # skip newline tokens after node
            root.addNode(codeStringNode)
        return root


def run_Parser():
    text = '''a = 3 + 5
    for (i = 3; i < n; 35){
            while (a != 5) {
                g = 7
                a = 5
            }
         b = 5
         }
         a = 3 + 5 '''
    a = Parser(run(text))


    l = a.parseCode()
    for i in l.codeNodes:
        print(i)