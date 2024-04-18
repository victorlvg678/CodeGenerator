from rply import LexerGenerator

class Lexer():
	def __init__(self):
		self.lexer = LexerGenerator()

	def _add_tokens(self):
		self.lexer.add('IDENTIFIER', r'(?!(int|float|void|if|else|while|return|printf))[a-zA-Z_]{1,}')
		self.lexer.add('FLOAT', r'([+-]?[0-9]+\.[0-9]+)')
		self.lexer.add('INTEGER', r'\d+')
		self.lexer.add('STRING', r'\".*\"')
		self.lexer.add('INTEGER_DATATYPE', r'int')
		self.lexer.add('FLOAT_DATATYPE', r'float')
		self.lexer.add('VOID_DATATYPE', r'void')
		self.lexer.add('ADD_OPERATOR', r'\+')
		self.lexer.add('SUBSTRACTION_OPERATOR', r'\-')
		self.lexer.add('MULTIPLICATION_OPERATOR', r'\*')
		self.lexer.add('DIVISION_OPERATOR', r'\/')
		self.lexer.add('LESS_THAN_OPERATOR', r'\<')
		self.lexer.add('LESS_THAN_OR_EQUAL_OPERATOR', r'\<\=')
		self.lexer.add('GREATER_THAN_OPERATOR', r'\>')
		self.lexer.add('GREATER_THAN_OR_EQUAL_OPERATOR', r'\>\=')
		self.lexer.add('OR_LOGICAL_OPERATOR', r'\|{2}')
		self.lexer.add('AND_LOGICAL_OPERATOR', r'\&{2}')
		self.lexer.add('EQUALITY_OPERATOR', r'\=\=')
		self.lexer.add('INEQUALITY_OPERATOR', r'\!\=')
		self.lexer.add('NOT_LOGICAL_OPERATOR', r'\!')
		self.lexer.add('SEMICOLON', r'\;')
		self.lexer.add('COMMA', r'\,')
		self.lexer.add('LEFT_PARENTHESIS', r'\(')
		self.lexer.add('RIGHT_PARENTHESIS', r'\)')
		self.lexer.add('LEFT_BRACE', r'\{')
		self.lexer.add('RIGHT_BRACE', r'\}')
		self.lexer.add('ASSIGNMENT', r'\=')
		self.lexer.add('IF_KEYWORD', r'if')
		self.lexer.add('WHILE_KEYWORD', r'while')
		self.lexer.add('RETURN_KEYWORD', r'return')
		self.lexer.add('ELSE_KEYWORD', r'else')
		self.lexer.add('NEW_LINE', r'\n+')
		self.lexer.add('PRINT_FUNCTION', r'printf')
		self.lexer.ignore('\s+')
		self.lexer.ignore('/\\*(.*?)\\*/')

	def get_lexer(self):
		self._add_tokens()
		return self.lexer.build()

