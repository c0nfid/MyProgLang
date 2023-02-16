from TokenType import TokenType
class Token:
    def __init__(self, type, text=None, pos=None):
        self.type = type
        self.text = text
        self.pos = pos

    def p(self):
        if self.text: return f'{self.type.name}: {self.text}'
        return f'{self.type}'
