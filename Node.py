from Lex import Token


class Node:
    pass


class StatementsNode(Node):
    def __init__(self):
        self.codeStrings = []  # Nodes

    def addNode(self, node):
        self.codeStrings.append(node)


class VariableNode(Node):

    def __init__(self, variable):
        self.variable = variable


class NumberNode(Node):

    def __init__(self, number):
        self.number = number


class Condition(Node):
    def __init__(self, start, stop, step):  # start - binOP, stop - binOP, step - Int
        self.start = start
        self.stop = stop
        self.step = step


class ifNode(Node):
    def __init__(self, condition, body, elseNode):
        self.condition = condition
        self.body = body
        self.elseNode = elseNode if elseNode else None


class LoopNode(Node):
    def __init__(self, key, condition, body):  # body: Token[]
        self.key = key
        self.condition = condition
        self.body = body


class BinOperationNode(Node):

    def __init__(self, operator, leftNode, rightNode):
        self.operator = operator
        self.leftNode = leftNode
        self.rightNode = rightNode


class UnarOperationNode(Node):

    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

class ListNode(Node):

    def __init__(self, list):
        self.list = list

class CallListNode(Node):

    def __init__(self, list, iter):
        self.list = list
        self.iter = iter

class ListActionNode(Node):
    def __init__(self, list, action, item):
        self.list = list
        self.action = action
        self.item = item