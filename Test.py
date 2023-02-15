class TokenType:
    def __init__(self, name, regex):
        self.name = name
        self.regex = regex


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


print(ListTokenType.FLOAT.regex)

for i in ListTokenType.values():
    print(i.name)

