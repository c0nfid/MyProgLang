import Lex

class Parser:
    tokens = [] #Token[]
    pos = 0
    scope = {}

    def __init__(self, tokens):
        self.tokens = tokens
    
    def match(self, expected):
        if (self.pos < len(self.tokens)):
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


def run():
    text = '''for (i = 03; i < n; i += 35){
    l = 4534534536.234564563453453453453453
}
if (i < 3){
    i++
}'''
    a = Parser(Lex.run(text))
    print(a.require([Lex.ListTokenType["T_FOR"]]))


run()