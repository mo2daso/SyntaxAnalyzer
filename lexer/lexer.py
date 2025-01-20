import re
from dataclasses import dataclass
from typing import List

@dataclass
class Token:
    """Represents a token in the source code"""
    type: str
    value: str
    position: int
    line: int

class Lexer:
    """Performs lexical analysis of source code"""
    
    TOKEN_SPECS = [
        ('NUMBER',     r'\b\d+(\.\d+)?\b'),
        ('STRING',     r'"[^"]*"|\'[^\']*\''),
        ('KEYWORD',    r'\b(if|else|while|for|return|def|class|import|from)\b'),
        ('BOOL_OP',    r'\b(and|or|not)\b'),
        ('COMPARE_OP', r'<=|>=|==|!=|<|>'),
        ('ASSIGN_OP',  r'=|\+=|-=|\*=|/='),
        ('OPERATOR',   r'[+\-*/]'),
        ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z_0-9]*\b'),
        ('LPAREN',     r'\('),
        ('RPAREN',     r'\)'),
        ('LBRACE',     r'\{'),
        ('RBRACE',     r'\}'),
        ('LBRACKET',   r'\['),
        ('RBRACKET',   r'\]'),
        ('SEMICOLON',  r';'),
        ('COMMA',      r','),
        ('DOT',        r'\.'),
        ('NEWLINE',    r'\n'),
        ('WHITESPACE', r'[ \t]+'),
        ('MISMATCH',   r'.'),
    ]

    def __init__(self):
        self.token_regex = '|'.join(f'(?P<{name}>{pattern})' 
                                  for name, pattern in self.TOKEN_SPECS)
        self.errors = []

    def tokenize(self, code: str) -> List[Token]:
        """Convert source code into a list of tokens"""
        tokens = []
        line_num = 1
        
        for match in re.finditer(self.token_regex, code):
            kind = match.lastgroup
            value = match.group()
            position = match.start()
            
            if kind == 'WHITESPACE':
                continue
            elif kind == 'NEWLINE':
                line_num += 1
                continue
            elif kind == 'MISMATCH':
                self.errors.append(
                    f"Invalid character '{value}' at line {line_num}, position {position}")
                continue
                
            tokens.append(Token(kind, value, position, line_num))
            
        return tokens