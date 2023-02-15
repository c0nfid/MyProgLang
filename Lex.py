ListTokenType = {"T_FLOAT": '([0-9]*\.[0-9]+)', "T_INT": '[0-9]*', "T_PLUS": '\\+', "T_MINUS": '\\-', 'T_ADD': '\\*',
                 "T_DIV": '\\/', "T_LPAREN": '\\(', "T_RPAREN": '\\)', "T_FOR": 'for',
                 "T_SEMICOLON": ';', "T_ASSIGN": '=', "T_NEWLINE" : '[\\n]',"SPACE": '[ \\n\\t\\r]',"T_VAR": '[a-z]*' , "T_<": '\\<',
                 "T_>": "\\>", "T_FLPAREN": "\\{", "T_FRPAREN": "\\}"}
import re


###################################################################
## CONSOLE > 3 + 2
## for (i = 0; i < n; 1) {
##  ghbdnrjwe = 0;
##  dsfhkjshdfkskdf += 1;
## }
###################################################################
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
        if self.text: return f'{self.type}: {self.text}'
        return f'{self.type}'


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
        for i in ListTokenType:
            regex = '^' + ListTokenType[i]
            result = re.findall(regex, self.itertxt[self.pos::])
            if result and result[0]:
                #print(result[0], i)
                #print(self.pos)
                self.tokenl.append(Token(i, result[0], self.pos).p())
                #print(self.tokenl[0].p())
                self.pos += len(result[0])
                return True

        self.Error = 203
        return False

    def getToken(self):
        return self.tokenl

    def make_tokens(self):
        while (self.next_token()):
            None

        if self.Error != 1:
            print('Ошибка в позиции ' + str(self.pos) + ": \'" + self.text[self.pos] + "\'")
            print('~'*self.pos + '^')
            return False
        print(self.tokenl)
        return True


def run(text):
    lexer = Lexer(text)
    tokens = lexer.getToken()
    return lexer.make_tokens()
