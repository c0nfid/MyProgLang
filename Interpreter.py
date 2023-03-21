from Parser import *
import math


class Interpreter:

    def __init__(self, sourceCode, strings):
        self.sourceCode = sourceCode
        self.codeS = strings
        self.scope = {}
        self.modules = list()

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

                if isinstance(node.left, CallDictNode):
                    variable = node.left.variable
                    iterator = node.left.iter
                    self.scope[variable.variable.text][iterator] = result

                else:
                    variable = node.left
                    self.scope[variable.variable.text] = result

                return result

            elif (node.operator.type == TokenList['>'] or
                  node.operator.type == TokenList['<'] or
                  node.operator.type == TokenList['!=']):

                flag = False
                if type(node.left) == VarNode:
                    try:
                        if self.scope[node.left.variable.text] or \
                                self.scope[node.left.variable.text] == 0:
                            flag = True

                    except KeyError:

                        raise Exception(
                            'Переменная с именем \'' + node.left.variable.text + '\' не была инициализирована')

                if type(node.right) == VarNode:
                    try:
                        if self.scope[node.right.variable.text] or \
                                self.scope[node.right.variable.text] == 0:

                            left = int(self.scope[node.left.variable.text]) if flag else int(
                                node.left.number.text)
                            right = int(self.scope[node.right.variable.text])

                            return (left < right) if node.operator.type == TokenList['<'] else (
                                (left > right) if node.operator.type == TokenList['>'] else
                                (left != right))

                    except KeyError:
                        raise Exception(
                            'Переменная с именем \'' + node.right.variable.text + '\' не была инициализирована')

                else:
                    left = int(self.scope[node.left.variable.text]) if flag else int(
                        node.left.number.text)
                    right = int(node.right.number.text)

                    return (left < right) if node.operator.type == TokenList['<'] else (
                        (left > right) if node.operator.type == TokenList['>'] else
                        (left != right))
            else:
                raise ValueError("Переменная не была объявлена")

        if isinstance(node, DictNode):
            return node.dict

        if isinstance(node, CallDictNode):
            value = self.run(node.variable)
            iterator = node.iter

            return value[iterator]

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

        if isinstance(node, LibNode):
            self.modules.append(node.library)
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

        if isinstance(node, LibOperationNode):
            if node.lib.text in self.modules:
                if node.operator.type == TokenList["COS"]:
                    return math.cos(self.run(node.arg))
                elif node.operator.type == TokenList["SIN"]:
                    return math.sin(self.run(node.arg))
                elif node.operator.type == TokenList["LOG"]:
                    return math.log(self.run(node.arg))
                elif node.operator.type == TokenList["GCD"]:
                    return math.gcd(*node.arg)
                elif node.operator.type == TokenList["SQRT"]:
                    return math.sqrt(self.run(node.arg))
                elif node.operator.type == TokenList["TANH"]:
                    return math.tan(self.run(node.arg))
                else:
                    raise Exception("Ошибка в определении мат операции")
            else:
                raise Exception(f'Модуль {node.lib.text} не подключен')

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
    #print(inter.scope)


text = '''import math
a = {sd:5, sq:sds}
n = 5
i = 3
a[sq] = 6
b = a[sq]
print(b)
a = 5
    for (i; i < n; 35){
            while (a != 5) {
                g = 7
                a = 5
            }
         b = math.cos(2)
         }
         print(a)'''

startCoding(text)
