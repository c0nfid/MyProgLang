import re

class TokenType:
    def __init__(self, name, regex):
        self.name = name
        self.regex = regex

    def __eq__(self, other):
        if type(other) is not TokenType:
            raise TypeError(other.name, type(other))

        return self.name == other.name and self.regex == other.regex


TokenList = {"FLOAT": TokenType("FLOAT", '([0-9]*\.[0-9]+)'),
             "INT": TokenType("INT", '[0-9]*'),
             "PLUS": TokenType("PLUS", '\\+'),
             "MINUS": TokenType("MINUS", '\\-'),
             "MULTIPLY": TokenType("MULTIPLY", '\\*'),
             "DIV": TokenType("DIV", '\\/'),
             "LPAREN": TokenType("LPAREN", '\\('),
             "RPAREN": TokenType("RPAREN", '\\)'),
             "FOR": TokenType("FOR", 'for'),
             "IF": TokenType("IF", 'if'),
             "ELSE": TokenType("ELSE", 'else'),
             "WHILE": TokenType('WHILE', 'while'),
             "SEMICOLON": TokenType("SEMICOLON", ';'),
             "ASSIGN": TokenType("ASSIGN", '='),
             "NEWLINE": TokenType("NEWLINE", '[\\n]'),
             "SPACE": TokenType("SPACE", '[ \\n\\t\\r]'),
             "VAR": TokenType("VAR", '[a-z]*'),
             "!=": TokenType("!=", '!='),
             "<": TokenType("<", '\\<'),
             ">": TokenType(">", "\\>"),
             "FLPAREN": TokenType("FLPAREN", "\\{"),
             "FRPAREN": TokenType("FRPAREN", "\\}")}

class Token:
    def __init__(self, type, text=None, pos=None):
        self.type = type
        self.text = text
        self.pos = pos

    def __str__(self):
        if self.text: return f'{self.type}: {self.text}'
        return f'{self.type}'


class Lexer:
    def __init__(self, text):
        self.Error = 1
        self.text = text
        self.pos = 0
        self.tokenl = []

    def next_token(self):
        if self.pos >= len(self.text):
            return False
        for i in TokenList:
            regex = '^' + TokenList[i].regex
            result = re.findall(regex, self.text[self.pos::])
            if result and result[0]:
                self.tokenl.append(Token(TokenList[i], result[0], self.pos))
                self.pos += len(result[0])
                return True

        self.Error = 404
        return False

    def getToken(self):
        temp = []
        for i in self.tokenl:
            if i.type != TokenList['SPACE']:
                temp.append(i)
        self.tokenl = temp
        return self.tokenl

    def make_tokens(self):
        while self.next_token():
            pass

        if self.Error != 1:
            print('Ошибка в позиции ' + str(self.pos) + ": \'" + self.text[self.pos] + "\'")
            return False
        print(self.tokenl)
        return True

    def line_tokens(self):
        a = []
        newtoken = []
        for i in self.tokenl:
            if i.type == 'NEWLINE' and a:
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
