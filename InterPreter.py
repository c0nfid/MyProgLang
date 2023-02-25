from Parser import *

class Interpreter:

    def __init__(self, sourceCode):
        self.sourceCode = sourceCode
        self.parserObj = Parser(lexAnalys(text))
        self.codeS = self.parserObj.parseCode()


    def run(self, node):
        if type(node) == NumberNode:
            return int(node.number.text) if node.number.type == ListTokenType.INT else float(node.number.text)
        # if type(node) == UnarOperationNode

        if type(node) == BinOperationNode:
            if node.operator.type == ListTokenType.PLUS:
                return self.run(node.leftNode) + self.run(node.rightNode)
            elif node.operator.type == ListTokenType.MINUS:
                return self.run(node.leftNode) - self.run(node.rightNode)
            elif node.operator.type == ListTokenType.ADD:
                return self.run(node.leftNode) * self.run(node.rightNode)
            elif node.operator.type == ListTokenType.DIV:
                return self.run(node.leftNode) / self.run(node.rightNode)
            elif node.operator.type == ListTokenType.ASSIGN:
                result = self.run(node.rightNode)
                variableNode = node.leftNode
                self.parserObj.scope[variableNode.variable.text] = result
                return result
            elif (node.operator.type == ListTokenType.SIGNMORE or node.operator.type == ListTokenType.SIGNLESS or node.operator.type == ListTokenType.NEQUAL):
                flag = False
                if type(node.leftNode) == VariableNode:
                    try:
                        if self.parserObj.scope[node.leftNode.variable.text] or self.parserObj.scope[node.leftNode.variable.text] == 0:
                            flag = True
                    except KeyError:
                        raise Exception('Переменная с именем \'' + node.leftNode.variable.text +'\' не была инициализирована')
                if type(node.rightNode) == VariableNode:
                    try:
                        if self.parserObj.scope[node.rightNode.variable.text] or self.parserObj.scope[node.rightNode.variable.text] == 0:
                            left = int(self.parserObj.scope[node.leftNode.variable.text]) if flag else int(node.leftNode.number.text)
                            right = int(self.parserObj.scope[node.rightNode.variable.text])
                            return (left < right) if node.operator.type == ListTokenType.SIGNLESS else ((left > right) if node.operator.type == ListTokenType.SIGNMORE else (left != right))
                    except KeyError:
                        raise Exception('Переменная с именем \'' + node.rightNode.variable.text + '\' не была инициализирована')
                else:
                    left = int(self.parserObj.scope[node.leftNode.variable.text]) if flag else int(node.leftNode.number.text)
                    right = int(node.rightNode.number.text)
                    return (left < right) if node.operator.type == ListTokenType.SIGNLESS else (
                        (left > right) if node.operator.type == ListTokenType.SIGNMORE else (left != right))

            #
            #
        if type(node) == VariableNode:
            try:
                if self.parserObj.scope[node.variable.text] or self.parserObj.scope[node.variable.text] == 0:
                    return self.parserObj.scope[node.variable.text]
            except KeyError:
                raise Exception('Переменная с именем \'' + node.variable.text +'\' не была инициализирована')

        if type(node) == ifNode:
            condition = self.run(node.condition.stop)
            if condition:
                for i in node.body:
                    self.run(i)
            return

        if type(node) == LoopNode:
            if node.key.type == ListTokenType.WHILE:
                condition = self.run(node.condition.stop)
                if condition:
                    for i in node.body:
                        self.run(i)
                    self.run(node)
            if node.key.type == ListTokenType.FOR:
                iter = node.condition.start.leftNode.variable.text
                try:
                    self.parserObj.scope[iter]
                except KeyError:
                    self.run(node.condition.start)
                condition = self.run(node.condition.stop)
                if condition:
                    for i in node.body:
                        self.run(i)
                    self.parserObj.scope[iter] += int(node.condition.step.text)
                    self.run(node)
            return

        if type(node) == UnarOperationNode:
            if type(node.operand) == VariableNode:
                try:
                    print(self.parserObj.scope[node.operand.variable.text])
                except KeyError:
                    raise Exception('Переменная с именем \'' + node.operand.variable.text + '\' не была инициализирована')
            if type(node.operand) == NumberNode:
                print(node.operand.number.text)

            if type(node.operand) == BinOperationNode:
                print(self.run(node.operand))
            return

        if type(node) == StatementsNode:
            for i in node.codeStrings:
                self.run(i)
            return



text = '''a = (5 - 3) - (9)
b = a + 11
c = 0
for (i = 0; i < 5; 1){
    a = a + 5
}
print(a)
'''
a = Interpreter(text)
a.run(a.codeS)