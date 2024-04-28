# another option: https://www.youtube.com/watch?v=LgsW0eGk-6U

text = '''
GET http://test.com
HTTP 301
GET http://123.com/?p=12
HTTP 200
GET http://yes.com
HTTP 400
GET http://no.com
HTTP 300
'''

DIGITS = '0123456789'
LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details
    
    def as_string(self):
        result  = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        return result

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)


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
TT_GET      = 'GET'
TT_POST     = 'POST'
TT_HTTP     = 'HTTP'
TT_IN       = 'IN'
TT_KEYWORD  = 'KEYWORD'
TT_EOF      = 'EOF'

class Token:
    def __init__(self, type_, value=None) -> None:
       self.type = type_
       self.value = value

    def matches(self, type_, value):
        return self.type == type_ and self.value == value
    
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
            if self.current_char in ' \t\r\n':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")
        
        tokens.append(Token(TT_EOF))    
        return tokens, None

    def make_number(self):
        num_str = ''
        
        while self.current_char != None and self.current_char in DIGITS:
            num_str += self.current_char
            self.advance()

        return Token(TT_INT, int(num_str))

    def make_identifier(self):
        id_str = ''
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in LETTERS + DIGITS + ';/?:@&=+$,#' + '-.!~*\'()':
            id_str += self.current_char
            self.advance()

        if id_str == "GET":
            return(Token(TT_GET))
        elif id_str == "HTTP":
            return(Token(TT_HTTP))
        elif id_str.startswith('http://') or id_str.startswith('https://'):
            tok_type = TT_URL
        else:
            tok_type = TT_STRING
        
        return Token(tok_type, id_str)


# NODES

class UrlNode:
    def __init__(self, tok) -> None:
        self.tok = tok
    
    def __repr__(self) -> str:
        return f'{self.tok}'

class NumberNode:
    def __init__(self, tok) -> None:
        self.tok = tok
    
    def __repr__(self) -> str:
        return f'{self.tok}'

class BinOpNode:
    def __init__(self, left_node, right_node) -> None:
       self.left_node = left_node
       self.op_tok = Token(TT_IN)
       self.right_node = right_node

    def __repr__(self) -> str:
        return f'({self.left_node}, {self.op_tok}, {self.right_node})' 

class UnaryNode:
    def __init__(self, op_tok, node) -> None:
        self.op_tok = op_tok
        self.node = node

    def __repr__(self) -> str:
        return f'({self.op_tok}, {self.node})'

class AssignNode:
    def __init__(self, op_tok, node) -> None:
        self.op_tok = op_tok
        self.node = node

    def __repr__(self) -> str:
        return f'({self.op_tok}, {self.node})'

class FunctionNode:
    def __init__(self, func_tok, primary_node, assign_node) -> None:
        self.func_tok = func_tok
        self.primary_node = primary_node
        self.assign_node = assign_node

    def __repr__(self) -> str:
        return f'({self.func_tok}, {self.primary_node}, {self.assign_node})'

# PARSER

class Parser:
    def __init__(self, tokens) -> None:
         self.tokens = tokens
         self.tok_idx = -1
         self.advance()

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok
        
    def parse(self):
        # res = self.function()
        # return res

        blocks = []
        for ct in self.tokens:
            if ct.type == TT_GET:
                blocks.append(self.function())
        
        return blocks 
    
    def function(self):
        req_tok = self.current_tok

        if self.current_tok.type == TT_GET:
            self.advance()
            if self.current_tok.type == TT_URL:
                primary_node = self.primary()

                if self.current_tok.type == TT_HTTP:
                    assign_node = self.assing()
            return FunctionNode(req_tok, primary_node, assign_node)


    def assing(self):
        if self.current_tok.type == TT_HTTP:
            op_tok = self.current_tok
            self.advance()
            primary = self.primary()
            return AssignNode(op_tok, primary)

    def primary(self):
        tok = self.current_tok

        if tok.type == TT_URL:
            self.advance()
            return UrlNode(tok)
        elif tok.type == TT_INT:
            self.advance()
            return NumberNode(tok)


lexer = Lexer('file_name', text)
tokens, error = lexer.make_tokens()

if error:
    print(error)
    exit(1)

print(tokens)
# generate AST
parser = Parser(tokens)
ast = parser.parse()

print(ast)