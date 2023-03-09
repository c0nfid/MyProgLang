from Parser import *


class Interpreter:

    def __init__(self, sourceCode, strings):
        self.sourceCode = sourceCode
        self.codeS = strings
        self.scope = {}

    def run(self, node):
        if type(node) == NumberNode:
            return int(node.number.text) if node.number.type == TokenList['INT'] else float(node.number.text)

        if type(node) == BinOperationNode:
            if node.operator.type == TokenList['PLUS']:
                return self.run(node.left) + self.run(node.right)
            elif node.operator.type == TokenList['MINUS']:
                return self.run(node.left) - self.run(node.right)
            elif node.operator.type == TokenList['ASSIGN']:
                result = self.run(node.right)
                variableNode = node.left
                self.scope[variableNode.variable.text] = result
                return result
            elif (
                    node.operator.type == TokenList['>'] or node.operator.type == TokenList[
                '<'] or node.operator.type == TokenList['!=']):
                flag = False
                if type(node.left) == VarNode:
                    try:
                        if self.scope[node.left.variable.text] or self.scope[
                            node.left.variable.text] == 0:
                            flag = True
                    except KeyError:
                        raise Exception(
                            'Переменная с именем \'' + node.left.variable.text + '\' не была инициализирована')
                if type(node.right) == VarNode:
                    try:
                        if self.scope[node.right.variable.text] or self.scope[
                            node.right.variable.text] == 0:
                            left = int(self.scope[node.left.variable.text]) if flag else int(
                                node.left.number.text)
                            right = int(self.scope[node.right.variable.text])
                            return (left < right) if node.operator.type == TokenList['<'] else (
                                (left > right) if node.operator.type == TokenList['>'] else (left != right))
                    except KeyError:
                        raise Exception(
                            'Переменная с именем \'' + node.right.variable.text + '\' не была инициализирована')
                else:
                    left = int(self.scope[node.left.variable.text]) if flag else int(
                        node.left.number.text)
                    right = int(node.right.number.text)
                    return (left < right) if node.operator.type == TokenList['<'] else (
                        (left > right) if node.operator.type == TokenList['>'] else (left != right))

            #
            #
        if type(node) == VarNode:
            try:
                if self.scope[node.variable.text] or self.scope[node.variable.text] == 0:
                    return self.scope[node.variable.text]
            except KeyError:
                raise Exception('Переменная с именем \'' + node.variable.text + '\' не была инициализирована')

        if type(node) == ConditionalNode:
            condition = self.run(node.condition.stop)
            if condition:
                for i in node.body:
                    self.run(i)
            return

        if type(node) == LoopNode:
            if node.type.type == TokenList['WHILE']:
                condition = self.run(node.condition.stop)
                if condition:
                    for i in node.body:
                        self.run(i)
                    self.run(node)
            if node.type.type == TokenList['FOR']:
                iter = node.condition.start.left.variable.text
                try:
                    self.scope[iter]
                except KeyError:
                    self.run(node.condition.start)
                condition = self.run(node.condition.stop)
                if condition:
                    for i in node.body:
                        self.run(i)
                    self.scope[iter] += int(node.condition.step.text)
                    self.run(node)
            return

        if type(node) == CommNode:
            if type(node.operand) == VarNode:
                try:
                    print(self.scope[node.operand.variable.text])
                except KeyError:
                    raise Exception(
                        'Переменная с именем \'' + node.operand.variable.text + '\' не была инициализирована')
            if type(node.operand) == NumberNode:
                print(node.operand.number.text)

            if type(node.operand) == BinOperationNode:
                print(self.run(node.operand))
            return

        if isinstance(node, RootNode):
            for i in node.codeNodes:
                self.run(i)
            return


def startCoding(string_code):
    lexer = run(string_code)
    exp_parser = Parser(lexer)
    inter = Interpreter(string_code, exp_parser.parseCode())
    inter.run(inter.codeS)
    print(inter.scope)


text = '''a = 3 + 5
n = 1
    for (i = 3; i < n; 35){
            while (a != 5) {
                g = 7
                a = 5
            }
         b = 5
         }
         a = n < i 
         print(a)'''
startCoding(text)