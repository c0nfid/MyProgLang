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
        if self.text: return f'{self.type.name}: {self.text}'
        return f'{self.type}'


ListTokenType = {"T_FLOAT": TokenType('FLOAT','([0-9]*\.[0-9]+)'), "T_INT": TokenType('INT', '[0-9]*'), "T_PLUS": TokenType('PLUS', '\\+'), "T_MINUS": TokenType('MINUS', '\\-'), 'T_ADD': TokenType('ADD', '\\*'),
                 "T_DIV": TokenType('DIV', '\\/'), "T_LPAREN": TokenType('LPAREN', '\\('), "T_RPAREN": TokenType('RPAREN', '\\)'), "T_FOR": TokenType('FOR', 'for'), "T_IF": TokenType('IF', 'if'), "T_ELSE": TokenType('ELSE', "else"),
                 "T_SEMICOLON": TokenType('SEMICOLON', ';'), "T_ASSIGN": TokenType('ASSIGN', '='), "T_NEWLINE" : TokenType('NEWLINE', '[\\n]'), "SPACE": TokenType('SPACE', '[ \\n\\t\\r]'),"T_VAR": TokenType('VAR', '[a-z]*'), "T_<": TokenType("<", '\\<'),
                 "T_>": TokenType('>', "\\>"), "T_FLPAREN": TokenType('FLPAREN',"\\{"), "T_FRPAREN": TokenType('FRPAREN', "\\}")}


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
            regex = '^' + ListTokenType[i].regex
            result = re.findall(regex, self.itertxt[self.pos::])
            if result and result[0]:
                #print(result[0], i)
                #print(self.pos)
                self.tokenl.append(Token(ListTokenType[i], result[0], self.pos))
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
        #print(self.tokenl)
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
    #for i in lexer.line_tokens():
    #    for j in i:
    #        print(j.text, end='')
    #    print()
    return lexer.getToken()