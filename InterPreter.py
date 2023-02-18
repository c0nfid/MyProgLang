from Parser import *

def run(node):
    if type(node) == NumberNode:
        return int(node.number.text) if node.number.type == ListTokenType.INT else float(node.number.text)
    #if type(node) == UnarOperationNode

    if type(node) == BinOperationNode:
        if node.operator.type == ListTokenType.PLUS:
            return run(node.leftNode) + run(node.rightNode)
        elif node.operator.type == ListTokenType.MINUS:
            return run(node.leftNode) - run(node.rightNode)
        elif node.operator.type == ListTokenType.ASSIGN:
            result = run(node.rightNode)
            variableNode = node.leftNode
            return result
        #
        #


text = '''a = (5 - 3) - (9 + 2)'''
print(run(run_Parser(text).codeStrings[0]))