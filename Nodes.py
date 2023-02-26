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