import re


class TokenType:
    def __init__(self, name, regex):
        self.name = name
        self.regex = regex


class Token:
    def __init__(self, type, text=None, pos=None):
        self.type = type
        self.text = text
        self.pos = pos

    def p(self):
        if self.text: return f'{self.type.name}: {self.text}'
        return f'{self.type}'


class ListTokenType:
    FLOAT = TokenType('FLOAT', '([0-9]*\.[0-9]+)')
    INT = TokenType('INT', '[0-9]*')
    PLUS = TokenType('PLUS', '\\+')
    MINUS = TokenType('MINUS', '\\-')
    ADD = TokenType('ADD', '\\*')
    DIV = TokenType('DIV', '\\/')
    LPAREN = TokenType('LPAREN', '\\(')
    RPAREN = TokenType('RPAREN', '\\)')
    FOR = TokenType('FOR', 'for')
    IF = TokenType('IF', 'if')
    ELSE = TokenType('ELSE', "else")
    SEMICOLON = TokenType('SEMICOLON', ';')
    ASSIGN = TokenType('ASSIGN', '=')
    NEWLINE = TokenType('NEWLINE', '[\\n]')
    SPACE = TokenType('SPACE', '[ \\n\\t\\r]')
    VAR = TokenType('VAR', '[a-z]*')
    SIGNLESS = TokenType("<", '\\<')
    SIGNMORE = TokenType('>', "\\>")
    FLPAREN = TokenType('FLPAREN', "\\{")
    FRPAREN = TokenType('FRPAREN', "\\}")

    @classmethod
    def items(cls):
        return list(cls.__dict__.items())[1:-5]

    @classmethod
    def values(cls):
        return list(cls.__dict__.values())[1:-5]


class Lexer:
    def __init__(self, text):
        self.Error = 1
        self.text = text
        self.itertxt = text
        self.pos = 0
        self.tokenl = []

    def next_token(self):
        if (self.pos >= len(self.text)):
            return False

        for currentToken in ListTokenType.values():
            regex = '^' + currentToken.regex
            result = re.findall(regex, self.itertxt[self.pos::])
            if result and result[0]:
                # print(result[0], i)
                # print(self.pos)
                self.tokenl.append(Token(currentToken, result[0], self.pos))
                # print(self.tokenl[0].p())
                self.pos += len(result[0])
                return True

        self.Error = 203
        return False

    def getToken(self):
        temp = []
        for i in self.tokenl:
            if i.type != ListTokenType.SPACE:
                temp.append(i)
        self.tokenl = temp
        return self.tokenl

    def make_tokens(self):
        while (self.next_token()):
            None

        if self.Error != 1:
            print('Ошибка в позиции ' + str(self.pos) + ": \'" + self.text[self.pos] + "\'")
            print('~' * self.pos + '^')
            return False
        # print(self.tokenl)
        return True

    def line_tokens(self):
        a = []
        newtoken = []
        for i in self.tokenl:
            if i.type.name == 'NEWLINE' and a:
                newtoken.append(a)
                a = []
                continue
            a.append(i)
        if a:
            newtoken.append(a)
        return newtoken


def run(text):
    lexer = Lexer(text)
    lexer.make_tokens()
    return lexer.getToken()
