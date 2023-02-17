from Lex import Token


class Node:
    pass


class StatementsNode(Node):
    codeStrings = []  # Nodes

    def addNode(self, node: Token):
        self.codeStrings.append(node)


class VariableNode(Node):

    def __init__(self, variable: Token):
        self.variable = variable


class NumberNode(Node):

    def __init__(self, number: Token):
        self.number = number

class Condition(Node):
    def __init__(self, start: Node, stop: Node, step: Token ): #start - binOP, stop - binOP, step - Int
        self.start = start
        self.stop = stop
        self.step = step
class LoopNode(Node):
    def __init__(self, key: Token, condition: Node, body): #body: Token[]
        self.key = key
        self.condition = condition
        self.body = body

class BinOperationNode(Node):

    def __init__(self, operator: Token, leftNode: Node, rightNode: Node):
        self.operator = operator
        self.leftNode = leftNode
        self.rightNode = rightNode


class UnarOperationNode(Node):

    def __init__(self, operator: Token, operand: Node):
        self.operator = operator
        self.operand = operand
