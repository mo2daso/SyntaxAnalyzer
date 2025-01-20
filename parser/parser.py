from dataclasses import dataclass
from typing import List, Optional
from lexer.lexer import Token

@dataclass
class Node:
    """Represents a node in the parse tree"""
    type: str
    value: str
    children: List['Node']
    token: Token

class Parser:
    """Performs syntax analysis and builds parse tree"""
    
    def __init__(self):
        self.tokens: List[Token] = []
        self.current = 0
        self.errors = []

    def parse(self, tokens: List[Token]) -> Optional[Node]:
        """Parse the tokens and return the root node of the parse tree"""
        self.tokens = tokens
        self.current = 0
        self.errors = []
        
        if not tokens:
            return None
            
        try:
            return self.parse_expression()
        except Exception as e:
            self.errors.append(str(e))
            return None

    def parse_expression(self) -> Node:
        """Parse an expression"""
        return self.parse_assignment()

    def parse_assignment(self) -> Node:
        """Parse an assignment expression"""
        left = self.parse_logical()
        
        while self.match('ASSIGN_OP'):
            operator = self.previous()
            right = self.parse_logical()
            left = Node("assign", operator.value, [left, right], operator)
            
        return left

    def parse_logical(self) -> Node:
        """Parse a logical expression"""
        left = self.parse_comparison()
        
        while self.match('BOOL_OP'):
            operator = self.previous()
            right = self.parse_comparison()
            left = Node("logical", operator.value, [left, right], operator)
            
        return left

    def parse_comparison(self) -> Node:
        """Parse a comparison expression"""
        left = self.parse_term()
        
        while self.match('COMPARE_OP'):
            operator = self.previous()
            right = self.parse_term()
            left = Node('compare', operator.value, [left, right], operator)
            
        return left

    def parse_term(self) -> Node:
        """Parse a term"""
        left = self.parse_factor()
        
        while self.match('OPERATOR'):
            operator = self.previous()
            right = self.parse_factor()
            left = Node('operator', operator.value, [left, right], operator)
            
        return left

    def parse_factor(self) -> Node:
        """Parse a factor"""
        if self.match('NUMBER', 'STRING', 'IDENTIFIER'):
            return Node('literal', self.previous().value, [], self.previous())
            
        if self.match('LPAREN'):
            expr = self.parse_expression()
            self.consume('RPAREN', "Expected ')' after expression")
            return Node('group', '()', [expr], self.previous())
            
        raise Exception(f"Unexpected token: {self.peek().value}")

    def match(self, *types) -> bool:
        """Check if current token matches any of the given types"""
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def check(self, type: str) -> bool:
        """Check if current token is of the given type"""
        if self.is_at_end():
            return False
        return self.peek().type == type

    def advance(self) -> Token:
        """Advance to next token"""
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self) -> bool:
        """Check if we've reached the end of tokens"""
        return self.current >= len(self.tokens)

    def peek(self) -> Token:
        """Look at current token"""
        return self.tokens[self.current]

    def previous(self) -> Token:
        """Get previous token"""
        return self.tokens[self.current - 1]

    def consume(self, type: str, message: str) -> Token:
        """Consume current token if it matches the type"""
        if self.check(type):
            return self.advance()
        raise Exception(message)