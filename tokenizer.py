text = '''
GET 
GET
POST 
'''

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self
    
    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)
    

# TOKENS

TT_URL      = 'URL'
TT_KEYWORD  = 'KEYWORD'

class Token:
    def __init__(self, type_, value=None) -> None:
       self.type = type_
       self.value = value

    def __repr__(self) -> str:
        if self.value: return f'{self.type}:{self.value}' 
        return f'{self.type}'

    
KEYWORDS = [
    'GET',
    'POST'
]


class Lexer:
    def __init__(self, file_name, text) -> None:
       self.file_name = file_name
       self.text = text 
       self.pos = Position(-1, 0, -1, file_name, text)
       self.current_char = None
       self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
    
    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t\n':
                self.advance()
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())
            else:
                self.advance()
                return []
        
        return tokens

    def make_identifier(self):
        id_str = ''
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in LETTERS:
            id_str += self.current_char
            self.advance()

        tok_type = TT_KEYWORD if id_str in KEYWORDS else 'NULL'
        return Token(tok_type, id_str)


lexer = Lexer('file_name', text)
tokens = lexer.make_tokens()

print(tokens)