from Parser import *
import PySimpleGUI as sg
import time


class Interpreter:
    def __init__(self, sourceCode):
        self.parserObj = Parser(lexAnalys(sourceCode))
        self.codeS = self.parserObj.parseCode()
        self.output = list()

    def run(self, node):
        if isinstance(node, NumberNode):
            return int(node.number.text) if node.number.type == ListTokenType.INT else float(node.number.text)

        if isinstance(node, ListNode):
            array = []
            for i in node.list:
                array.append(self.run(i))
            return array

        if isinstance(node, BinOperationNode):
            if node.operator.type == ListTokenType.PLUS:
                return self.run(node.leftNode) + self.run(node.rightNode)
            elif node.operator.type == ListTokenType.MINUS:
                if isinstance(node.leftNode, ListNode):
                    raise Exception("Операция вычитания с списками не поддерживается")
                else:
                    return self.run(node.leftNode) - self.run(node.rightNode)
            elif node.operator.type == ListTokenType.ADD:
                if isinstance(node.leftNode, ListNode):
                    raise Exception("Операция умножения с списками не поддерживается")
                else:
                    return self.run(node.leftNode) * self.run(node.rightNode)
            elif node.operator.type == ListTokenType.DIV:
                return self.run(node.leftNode) / self.run(node.rightNode)
            elif node.operator.type == ListTokenType.ASSIGN:
                result = self.run(node.rightNode)
                variableNode = node.leftNode
                if isinstance(variableNode, CallListNode):
                    index = self.run(variableNode.iter)
                    self.parserObj.scope[variableNode.list.text][index] = result
                else:
                    self.parserObj.scope[variableNode.variable.text] = result
                return result
            elif (
                    node.operator.type == ListTokenType.SIGNMORE or node.operator.type == ListTokenType.SIGNLESS or node.operator.type == ListTokenType.NEQUAL):
                flag = False
                if isinstance(node.leftNode, VariableNode):
                    try:
                        if self.parserObj.scope[node.leftNode.variable.text] or self.parserObj.scope[
                            node.leftNode.variable.text] == 0:
                            flag = True
                    except KeyError:
                        raise Exception(
                            'Переменная с именем \'' + node.leftNode.variable.text + '\' не была инициализирована')
                if isinstance(node.rightNode, VariableNode):
                    try:
                        if self.parserObj.scope[node.rightNode.variable.text] or self.parserObj.scope[
                            node.rightNode.variable.text] == 0:
                            left = int(self.parserObj.scope[node.leftNode.variable.text]) if flag else int(
                                node.leftNode.number.text)
                            right = int(self.parserObj.scope[node.rightNode.variable.text])
                            return (left < right) if node.operator.type == ListTokenType.SIGNLESS else (
                                (left > right) if node.operator.type == ListTokenType.SIGNMORE else (left != right))
                    except KeyError:
                        raise Exception(
                            'Переменная с именем \'' + node.rightNode.variable.text + '\' не была инициализирована')
                else:
                    left = int(self.parserObj.scope[node.leftNode.variable.text]) if flag else int(
                        node.leftNode.number.text)
                    right = int(node.rightNode.number.text)
                    return (left < right) if node.operator.type == ListTokenType.SIGNLESS else (
                        (left > right) if node.operator.type == ListTokenType.SIGNMORE else (left != right))

        if isinstance(node, VariableNode):
            try:
                if self.parserObj.scope[node.variable.text] or self.parserObj.scope[node.variable.text] == 0:
                    return self.parserObj.scope[node.variable.text]
            except KeyError:
                raise Exception('Переменная с именем \'' + node.variable.text + '\' не была инициализирована')

        if isinstance(node, ifNode):
            condition = self.run(node.condition.stop)
            if condition:
                for i in node.body:
                    self.run(i)
            return

        if isinstance(node, ListActionNode):
            result = self.run(node.item)
            if node.action == "append":
                self.parserObj.scope[node.list.variable.text].append(result)
            elif node.action == "index":
                return self.parserObj.scope[node.list.variable.text].index(result)
            elif node.action == 'find':
                return [index for index, value in enumerate(self.parserObj.scope[node.list.variable.text]) if value == result]
            return None

        if isinstance(node, LoopNode):
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

        if isinstance(node, UnarOperationNode):
            if isinstance(node.operand, CallListNode):
                index = self.run(node.operand.iter)
                if self.parserObj.scope[node.operand.list.text][index] or self.parserObj.scope[node.operand.list.text][
                    index] == 0:
                    temp = self.parserObj.scope[node.operand.list.text][index]
                    self.output.append(temp)
                return
            if isinstance(node.operand, ListActionNode):
                temp = self.run(node.operand)
                self.output.append(temp if type(temp) != list else temp.copy())
                return
            if isinstance(node.operand, VariableNode):
                try:
                    temp = self.parserObj.scope[node.operand.variable.text]
                    self.output.append(temp if type(temp) != list else temp.copy())
                except KeyError:
                    raise Exception(
                        'Переменная с именем \'' + node.operand.variable.text + '\' не была инициализирована')

            if isinstance(node.operand, NumberNode):
                temp = node.operand.number.text
                self.output.append(temp)
                return
            if isinstance(node.operand, BinOperationNode):
                temp = self.run(node.operand)
                self.output.append(temp)
            return

        if isinstance(node, StatementsNode):
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
print(b)
'''

sg.theme("LightPurple")
layout = [
    [sg.Text('MyProgramLanguage', font=('Arial Bold', 20), expand_x=True, justification='center'), sg.Button("⏵"),
     sg.Button('↓'), sg.Button('🗀')],
    [sg.Multiline("Input your code", enable_events=True, key='-INPUT-', expand_x=True, expand_y=True,
                  justification='left')],
    [sg.Text("Run:", key='out', font=('Arial Bold', 16), expand_x=True, justification='left')],
    [sg.Multiline("Program output", enable_events=True, key='-OUTPUT-', size=(100, 10),
                  justification='left')]]
win = sg.Window("Interpreter", layout, size=(700, 500))
while True:
    event, values = win.Read()
    if event == sg.WIN_CLOSED:
        break
    elif event == '⏵':
        time.sleep(0.25)
        try:
            inter = Interpreter(values["-INPUT-"])
            inter.run(inter.codeS)
            out = ""
            for x in inter.output: out += (str(x) + '\n')
            win["-OUTPUT-"].update(out)
        except SyntaxError as err:
            win["-OUTPUT-"].update(err)
        except Exception as err:
            win["-OUTPUT-"].update(err)
        continue
    elif event == '↓':
        savelayout = [
            [sg.Text('Input path', font=('Arial Bold', 20), expand_x=True, justification='center'),
             sg.Button('SAVE')],
            [sg.InputText()]]
        savelay = sg.Window("Save File", savelayout, size=(300, 100))
        while True:
            saveevent, savevalues = savelay.Read()
            if saveevent == sg.WIN_CLOSED:
                break
            elif saveevent == 'SAVE':
                file = open(savevalues[0], 'w')
                print(savevalues[0])
                file.write(values["-INPUT-"])
                file.close()
                savelay.close()
                break
    elif event == '🗀':
        savelayout = [
            [sg.Text('Input path', font=('Arial Bold', 20), expand_x=True, justification='center'),
             sg.Button('OPEN')],
            [sg.InputText()]]
        savelay = sg.Window("Open File", savelayout, size=(300, 100))
        while True:
            saveevent, savevalues = savelay.Read()
            if saveevent == sg.WIN_CLOSED:
                savelay.close()
                break
            elif saveevent == 'OPEN':
                try:
                    file = open(savevalues[0], 'r')
                    win["-INPUT-"].update(file.read())
                    file.close()
                    savelay.close()
                except FileNotFoundError:
                    warning = [[sg.Text('File not found')], [sg.Button('OK')]]
                    warn = sg.Window("Warning", warning, size=(200, 75))
                    while True:
                        warnevent, warnval = warn.Read()
                        if warnevent == sg.WIN_CLOSED:
                            warn.close()
                            break
                        elif warnevent == "OK":
                            warn.close()
                            break
                print(savevalues[0])
                break
