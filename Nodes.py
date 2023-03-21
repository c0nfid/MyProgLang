from Lex import Token


class Node:
    pass


class RootNode(Node):
    def __init__(self):
        self.codeNodes = []  # Nodes

    def addNode(self, node):
        self.codeNodes.append(node)


class VarNode(Node):

    def __init__(self, variable):
        self.variable = variable


class NumberNode(Node):

    def __init__(self, number):
        self.number = number


class BinOperationNode(Node):

    def __init__(self, operator: Token, leftNode: Node, rightNode: Node):
        self.operator = operator
        self.left = leftNode
        self.right = rightNode


class LoopConditionNode(Node):

    def __init__(self, start, stop, step):
        self.start = start
        self.step = step
        self.stop = stop


class LoopNode(Node):

    def __init__(self, ltype, condition, body):
        self.type = ltype
        self.condition = condition
        self.body = body


class ConditionalNode(Node):  # change name please
    def __init__(self, condition: Node, body: [], elseNode):
        self.condition = condition
        self.body = body
        self.elseNode = elseNode if elseNode else None


class CommNode(Node):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand


class LibNode(Node):

    def __init__(self, library):
        self.library = library


class LibOperationNode(Node):

    def __init__(self, lib, operator, arg):
        self.lib = lib
        self.operator = operator
        self.arg = arg


class DictNode(Node):

    def __init__(self, dict):
        self.dict = dict


class CallDictNode(Node):
    def __init__(self, variable, iter):
        self.variable = variable
        self.iter = iter
