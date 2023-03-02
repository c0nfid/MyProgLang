from Lex import *
from Node import *


class Parser:

    def __init__(self, tokens):
        self.pos = 0
        self.scope = {}
        self.tokens = tokens

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
            if self.match([ListTokenType.SQLPAREN]):
                iter = self.parseFormula()
                varNode = CallListNode(var, iter)
                self.require([ListTokenType.SQRPAREN])
                return varNode
            return VariableNode(var)
        raise SyntaxError(f'Ошибка синтаксиса на позиции {self.pos}')

    def parseParenthes(self):
        if self.match([ListTokenType.LPAREN]):
            node = self.parseFormula()
            self.require([ListTokenType.RPAREN])
            if self.match([ListTokenType.ADD]):
                self.pos-=1
                operator = self.match([ListTokenType.ADD])
                rightNode = self.parseParenthes()
                node = BinOperationNode(operator, node, rightNode)
            return node
        elif self.pos+1 < len(self.tokens) and self.tokens[self.pos+1].type == ListTokenType.ADD:
            leftNode = self.parsVarOrNumb()
            operator = self.match([ListTokenType.ADD])
            rightNode = self.parseParenthes()
            return BinOperationNode(operator, leftNode, rightNode)
        else:
            return self.parsVarOrNumb()

    def parseFormula(self):
        if self.match([ListTokenType.LIST, ListTokenType.SQLPAREN]):
            flag = False
            if self.match([ListTokenType.LPAREN]):
                flag = True
            array = list()
            array.append(self.parseParenthes())
            operator = self.match([ListTokenType.COLON])
            while operator:
                array.append(self.parseParenthes())
                operator = self.match([ListTokenType.COLON])
            if flag:
                self.require([ListTokenType.RPAREN])
            else:
                self.require([ListTokenType.SQRPAREN])
            return ListNode(array)
        elif (self.match([ListTokenType.VAR])):
            self.pos -= 1
            varNode = self.parsVarOrNumb()
            if self.match([ListTokenType.DOT]):
                key = self.match([ListTokenType.APPEND, ListTokenType.INDEX, ListTokenType.FIND])
                action = ''
                if key and self.match([ListTokenType.LPAREN]):
                    addable = self.parseFormula()
                    self.require([ListTokenType.RPAREN])
                    if key.type == ListTokenType.APPEND: action = "append"
                    elif key.type == ListTokenType.INDEX: action = "index"
                    elif key.type == ListTokenType.FIND: action = "find"
                    return ListActionNode(varNode, action, addable)
                else:
                    raise Exception("Ошибка синтаксиса")
        else:
            leftNode = self.parseParenthes()
            operator = self.match(
                [ListTokenType.PLUS, ListTokenType.MINUS, ListTokenType.SIGNLESS, ListTokenType.SIGNMORE, ListTokenType.ADD,
                 ListTokenType.DIV])
            while operator:
                rightNode = self.parseParenthes()
                leftNode = BinOperationNode(operator, leftNode, rightNode)
                operator = self.match(
                    [ListTokenType.PLUS, ListTokenType.MINUS, ListTokenType.SIGNLESS, ListTokenType.SIGNMORE,ListTokenType.ADD,
                     ListTokenType.DIV])
            return leftNode

    def parseLoopCondition(self):
        if self.require([ListTokenType.LPAREN]) == None:
            return None
        if self.match([ListTokenType.VAR]):
            self.pos -= 1
            varNode = self.parsVarOrNumb()
            assignOperator = self.match([ListTokenType.ASSIGN])
            if assignOperator:
                rightFormulNode = self.parseFormula()
                binaryNode = BinOperationNode(assignOperator, varNode, rightFormulNode)
            else:
                raise SyntaxError("Ошибка в синтаксисе присваивания")
        else:
            raise SyntaxError("Ошибка в определении цикла")

        if self.require([ListTokenType.SEMICOLON]) == None:
            raise Exception(f'Ожидается знак \';\' на позиции {self.pos - 1}')

        leftNode = self.parsVarOrNumb()
        operator = self.match([ListTokenType.SIGNMORE, ListTokenType.SIGNLESS])
        stop = BinOperationNode(operator, leftNode, self.parsVarOrNumb())

        if self.require([ListTokenType.SEMICOLON]) == None:
            raise SyntaxError(f'Ожидается знак \';\' на позиции {self.pos - 1}')
        step = self.match([ListTokenType.INT])
        if self.require([ListTokenType.RPAREN]) == None:
            raise SyntaxError(f'Ожидается знак \')\' на позиции {self.pos - 1}')
        return Condition(binaryNode, stop, step)

    def parseCondition(self):
        if self.require([ListTokenType.LPAREN]) == None:
            raise SyntaxError(f'Ожидается знак \'(\' на позиции {self.pos - 1}')

        leftNode = self.parsVarOrNumb()
        operator = self.match([ListTokenType.SIGNMORE, ListTokenType.SIGNLESS, ListTokenType.NEQUAL])
        stop = BinOperationNode(operator, leftNode, self.parsVarOrNumb())

        if self.require([ListTokenType.RPAREN]) == None:
            return None

        return Condition(None, stop, None)

    def parseBody(self):
        if self.require([ListTokenType.FLPAREN]) == None:
            raise SyntaxError(f'Ожидается знак открытия тела на позиции {self.pos - 1}')
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
            if self.match([ListTokenType.DOT]):
                if self.match([ListTokenType.APPEND]) and self.match([ListTokenType.LPAREN]):
                    addable = self.parseFormula()
                    self.require([ListTokenType.RPAREN])
                    return ListActionNode(varNode, "append", addable)
                elif self.match([ListTokenType.INDEX]) and self.match([ListTokenType.LPAREN]):
                    addable = self.parseFormula()
                    self.require([ListTokenType.RPAREN])
                    return ListActionNode(varNode, "index", addable)
                else:
                    raise Exception("Ошибка синтаксиса")

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
                raise SyntaxError(f'Ожидается знак \'(\' на позиции {self.pos - 1}')
            operand = self.parseFormula()
            if self.require([ListTokenType.RPAREN]) == None:
                raise SyntaxError(f'Ожидается знак \')\' на позиции {self.pos - 1}')

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
