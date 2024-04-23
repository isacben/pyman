text = '''
GET http://test.com
GET http://123.com/?p=12
HTTP 200
POST http:/bad.url
'''

import string

DIGITS = '0123456789'
CHARACTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
print(CHARACTERS)

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

TT_STRING   = 'STRING'
TT_INT      = 'INT'
TT_URL      = 'URL'
TT_KEYWORD  = 'KEYWORD'
TT_EOF      = 'EOF'

class Token:
    def __init__(self, type_, value=None) -> None:
       self.type = type_
       self.value = value

    def __repr__(self) -> str:
        if self.value: return f'{self.type}:{self.value}' 
        return f'{self.type}'

    
KEYWORDS = [
    'GET',
    'POST',
    'HTTP',
    '[Postman]'
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
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in CHARACTERS + DIGITS:
                tokens.append(self.make_identifier())
            else:
                self.advance()
                #return []
        
        return tokens

    def make_number(self):
        num_str = ''
        
        while self.current_char != None and self.current_char in DIGITS:
            num_str += self.current_char
            self.advance()

        return Token(TT_INT, int(num_str))

    def make_identifier(self):
        id_str = ''
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in CHARACTERS + DIGITS:
            id_str += self.current_char
            self.advance()

        if id_str in KEYWORDS:
            tok_type = TT_KEYWORD 
        elif id_str.startswith('http://') or id_str.startswith('https://'):
            tok_type = TT_URL
        else:
            tok_type = TT_STRING
        
        return Token(tok_type, id_str)


lexer = Lexer('file_name', text)
tokens = lexer.make_tokens()

print(tokens)