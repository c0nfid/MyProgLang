from Lex import *


class Parser:
    tokens = []  # Token[]
    pos = 0
    scope = {}

    def __init__(self, tokens):
        self.tokens = tokens

    def match(self, expected):
        print(expected)
        if (self.pos < len(self.tokens)):
            print()
            currentToken = self.tokens[self.pos]
            if currentToken.type in expected:
                self.pos += 1
                return currentToken
        return None

    def require(self, expected):
        token = self.match(expected)
        if (token == None):
            print('Error')
        else:
            return token
        return None


def run_Parser():
    text = '''for (i = 03; i < n; i += 35){
    l = 4534534536.234564563453453453453453
}
if (i < 3){
    i++
}'''
    a = Parser(run(text))

    print(a.match([ListTokenType.FOR]))
    print(a.tokens)


run_Parser()