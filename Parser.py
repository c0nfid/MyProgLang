from Lex import *
from Nodes import *


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens  # Token[]
        self.pos = 0

    def match(self, expected):
        if self.pos < len(self.tokens):
            currentToken = self.tokens[self.pos]
            if currentToken.type in expected:
                self.pos += 1
                return currentToken

        return None

    def require(self, expected):
        token = self.match(expected)
        if token is None:
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
            if self.match([TokenList['SQLPAREN']]):
                iterator = self.match([TokenList["VAR"]]).text
                self.require([TokenList["SQRPAREN"]])
                return CallDictNode(VarNode(var), iterator)
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
        if self.match([TokenList["MATH"]]):
            self.pos -=1
            lib = self.match([TokenList["MATH"]])
            if self.match([TokenList["DOT"]]) and self.match(
                    [TokenList["GCD"], TokenList["LOG"], TokenList["SQRT"], TokenList["SIN"], TokenList["COS"],
                     TokenList["TANH"]]):
                self.pos -=1
                operator = self.match(
                    [TokenList["GCD"], TokenList["LOG"], TokenList["SQRT"], TokenList["SIN"], TokenList["COS"],
                     TokenList["TANH"]])
                if self.require([TokenList["LPAREN"]]):
                    if operator.type == TokenList["GCD"]:
                        arg = list()
                        arg.append(self.parseVariableOrNumbers())
                        separator = self.match([TokenList["COMMA"]])
                        while separator:
                            arg.append(self.parseParenthes())
                            separator = self.match([TokenList["COMMA"]])
                    else:
                        arg = self.parseVariableOrNumbers()
                else:
                    arg = None
                self.require([TokenList["RPAREN"]])
                return LibOperationNode(lib, operator, arg)
            else:
                return None

        if self.match([TokenList["FLPAREN"]]):
            dicttemp = {}
            key = self.parseVariableOrNumbers()
            key = key.variable.text if isinstance(key, VarNode) else key.number.text
            self.require([TokenList["COLON"]])
            value = self.parseVariableOrNumbers()
            dicttemp[key] = value.variable.text if isinstance(value, VarNode) else (int(value.number.text) if value.number.type == TokenList['INT'] else float(value.number.text))
            sep = self.match([TokenList["COMMA"]])
            while sep:
                key = self.parseVariableOrNumbers()
                key = key.variable.text if isinstance(key, VarNode) else key.number.text
                self.require([TokenList["COLON"]])
                value = self.parseVariableOrNumbers()
                dicttemp[key] = value.variable.text if isinstance(value, VarNode) else (int(value.number.text) if value.number.type == TokenList['INT'] else float(value.number.text))
                sep = self.match([TokenList["COMMA"]])
            self.require([TokenList["FRPAREN"]])
            return DictNode(dicttemp)

        leftNode = self.parseParenthes()
        operator = self.match(
            [TokenList['PLUS'], TokenList['MINUS'], TokenList['<'], TokenList['>'], TokenList['MULTIPLY'],
             TokenList['DIV']])
        while operator:
            rightNode = self.parseParenthes()
            leftNode = BinOperationNode(operator, leftNode, rightNode)
            operator = self.match(
                [TokenList['PLUS'], TokenList['MINUS'], TokenList['<'], TokenList['>'], TokenList['MULTIPLY'],
                 TokenList['DIV']])

        return leftNode

    def parseCondition(self, loop_type):
        if self.require([TokenList['LPAREN']]) is None:
            return None

        if loop_type.type == TokenList['FOR']:
            if self.match([TokenList['VAR']]):
                self.pos -= 1

                var_node = self.parseVariableOrNumbers()
                assign = self.match([TokenList['ASSIGN']])
                right_node = self.parseFormula() if assign else None

                start = BinOperationNode(assign, var_node, right_node)

            else:
                print("ErrorStartLoop Syntax, require")
                return None

            if self.require([TokenList['SEMICOLON']]) is None:
                print("ErrorSemicolon" + self.pos - 1)
                return None
        else:
            start = None

        left_node = self.parseVariableOrNumbers()
        stop = BinOperationNode(self.match([TokenList['<'], TokenList['>'], TokenList['!=']]), left_node,
                                self.parseVariableOrNumbers())

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
        if self.require([TokenList['FLPAREN']]) is None:
            return None
        body = []

        while self.match([TokenList['FRPAREN']]) is None:
            if self.match([TokenList['NEWLINE']]) is None:
                pass
            if self.match([TokenList['FRPAREN']]):
                return body

            bodyNode = self.parseExpression()
            if bodyNode is None:
                return None
            body.append(bodyNode)

        return body

    def parseExpression(self):
        if self.match([TokenList['IMPORT']]):
            lib = self.match([TokenList["MATH"]]).text
            return LibNode(lib)

        elif self.match([TokenList['VAR']]):
            self.pos -= 1
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
            self.pos -= 1
            operator = self.match([TokenList['PRINT']])
            if self.require([TokenList['LPAREN']]) is None:
                return None
            operand = self.parseFormula()
            if self.require([TokenList['RPAREN']]) is None:
                return None

            return CommNode(operator, operand)

        raise SyntaxError("Ошибка определения оператора")

    def parseCode(self):
        root = RootNode()
        while self.pos < len(self.tokens):
            codeStringNode = self.parseExpression()
            self.match([TokenList['NEWLINE']])  # skip newline tokens after node
            root.addNode(codeStringNode)
        return root


def test_Parser():
    text = '''import math
    a = math.cos(x)'''
    a = run(text)
    a = Parser(a)

    l = a.parseCode()
    for i in l.codeNodes:
        print(i.right if isinstance(i, BinOperationNode) else i)
