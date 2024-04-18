from rply import ParserGenerator, ParsingError
from ast_implementation import *
from global_variables import GlobalVariablesSingleton

class Parser():
	def __init__(self, module, builder, base_func, printf):
		self.pg = ParserGenerator(['IDENTIFIER', 'INTEGER', 'FLOAT', 'STRING', 'INTEGER_DATATYPE', 'FLOAT_DATATYPE', 'VOID_DATATYPE', 'ADD_OPERATOR', 'SUBSTRACTION_OPERATOR', 'MULTIPLICATION_OPERATOR', 'DIVISION_OPERATOR', 'LESS_THAN_OPERATOR', 'LESS_THAN_OR_EQUAL_OPERATOR', 'GREATER_THAN_OPERATOR', 'GREATER_THAN_OR_EQUAL_OPERATOR', 'OR_LOGICAL_OPERATOR', 'AND_LOGICAL_OPERATOR', 'NOT_LOGICAL_OPERATOR', 'EQUALITY_OPERATOR', 'INEQUALITY_OPERATOR', 'SEMICOLON', 'COMMA', 'LEFT_PARENTHESIS', 'RIGHT_PARENTHESIS', 'LEFT_BRACE', 'RIGHT_BRACE', 'ASSIGNMENT', 'IF_KEYWORD', 'WHILE_KEYWORD', 'RETURN_KEYWORD', 'ELSE_KEYWORD', 'NEW_LINE', 'PRINT_FUNCTION'])
		self.module = module
		self.builder = builder
		self.base_func = base_func
		self.printf = printf

	def parse(self):
		@self.pg.production('program : statement')
		@self.pg.production('program : statement NEW_LINE program')
		@self.pg.production('program : function')
		@self.pg.production('program : function NEW_LINE program')
		def program(program_declaration):
			if len(program_declaration) == 1:
				return [program_declaration[0]]
			
			if len(program_declaration) == 3:
				return [program_declaration[0]] + program_declaration[2]
			
		@self.pg.production('type : INTEGER_DATATYPE')
		@self.pg.production('type : FLOAT_DATATYPE')
		@self.pg.production('type : VOID_DATATYPE')
		def type(type_declaration):
			datatype = type_declaration[0]
			if datatype.gettokentype() == 'INTEGER_DATATYPE':
				return Integer(self.builder, self.module, self.base_func, '', 0)

			if datatype.gettokentype() == 'FLOAT_DATATYPE':
				return Float(self.builder, self.module, self.base_func, '', 0)

			return Void(self.builder, self.module, self.base_func, '')

		@self.pg.production('argument : type IDENTIFIER')
		def argument(argument_declaration):
			datatype = argument_declaration[0]
			identifier = argument_declaration[1]
			datatype.set_name(identifier)
			return datatype

		@self.pg.production('arguments : argument')
		@self.pg.production('arguments : arguments argument')
		def arguments(arguments_declaration):
			if len(arguments_declaration) == 1:
				return [arguments_declaration[0]]
			else:
				return [arguments_declaration[0]] + arguments_declaration[1]

		@self.pg.production('variable_declaration : type IDENTIFIER')
		@self.pg.production('variable_declaration : type IDENTIFIER ASSIGNMENT expression')
		@self.pg.production('variable_declaration : IDENTIFIER ASSIGNMENT expression')
		def variable_declaration(variable_declaration_declaration):
			global_variables_instance = GlobalVariablesSingleton()
			
			if len(variable_declaration_declaration) == 2 or len(variable_declaration_declaration) == 4:
				datatype = variable_declaration_declaration[0]
				identifier = variable_declaration_declaration[1].getstr()
				datatype.set_name(identifier)
				
				if isinstance(datatype, (Float, Integer)):
					datatype_name = datatype.get_type()
				else:
					try:
						datatype_name = datatype.getstr()
					except:
						datatype_name = datatype

				try:
					identifier = variable_declaration_declaration[1].getstr()
				except:
					identifier = variable_declaration_declaration[1]

				if len(variable_declaration_declaration) == 2:
					parsed_line = f"{datatype_name} {identifier};"

				if len(variable_declaration_declaration) == 4:
					value = variable_declaration_declaration[3]
					datatype.set_value(value)
					parsed_line = f"{datatype_name} {identifier} = {value};"
			else:
				if isinstance(variable_declaration_declaration[0], Float) or isinstance(variable_declaration_declaration[0], Integer):
					identifier = variable_declaration[0].getstr()
				else:
					try:
						identifier = variable_declaration_declaration[0].getstr()
						source_position = variable_declaration_declaration[0].getsourcepos()
					except:
						print("Error when trying to get token type on variable declaration")
						identifier = variable_declaration_declaration[0]
				
				if global_variables_instance.get_variable(identifier) is None:
					if source_position is not None:
						raise ParsingError(f"No existe variable \"{identifier}\" ya que no ha sido declarada", source_position)
					else:
						raise ValueError(f"No existe variable \"{identifier}\" ya que no ha sido declarada")
				
				datatype = global_variables_instance.get_variable(identifier)
				new_value = variable_declaration_declaration[2]
				datatype.set_value(new_value)
				
				if isinstance(new_value, (Float, Integer)):
					new_value_string = new_value.get_value()
				else:
					new_value_string = new_value

				parsed_line = f"{identifier} = {new_value_string};"

			global_variables_instance.set_parsed_line(parsed_line)
			global_variables_instance.set_variable(datatype.get_name(), datatype)
			return datatype
		
		@self.pg.production('statement : variable_declaration SEMICOLON')
		@self.pg.production('statement : expression SEMICOLON')
		@self.pg.production('statement : statement statement')
		@self.pg.production('statement : print SEMICOLON')
		def statement(statement_declaration):
			if isinstance(statement_declaration[0], (Float, Integer)):
				return statement_declaration[0]
			
			try:
				if statement_declaration[1].gettokentype() == "SEMICOLON":
					return statement_declaration[0]
			except:
				print('Error trying to check if statement has semicolon')

			return [statement_declaration[0]] + statement_declaration[1]
			

		@self.pg.production('function : type IDENTIFIER LEFT_PARENTHESIS params RIGHT_PARENTHESIS LEFT_BRACE program RIGHT_BRACE')
		@self.pg.production('function : type IDENTIFIER LEFT_PARENTHESIS RIGHT_PARENTHESIS LEFT_BRACE program RIGHT_BRACE')
		def function(function_declaration):
			global_variables_instance = GlobalVariablesSingleton()
			datatype = function_declaration[0]
			if isinstance(datatype, (Integer, Float, Void)):
					datatype_name = datatype.get_type()
			else:
				try:
					datatype_name = function_declaration[0].getstr()
				except:
					datatype_name = "unknown"

			identifier = function_declaration[1].getstr()
			left_parenthesis = function_declaration[2].getstr()

			if len(function_declaration) == 8:
				params_list = function_declaration[3]
				param_list_string = str(params_list)
				right_parenthesis = function_declaration[4].getstr()
				left_brace = function_declaration[5].getstr()
				program_definition = function_declaration[6]
				program_definition_string = f"[{','.join([str(element) for element in program_definition])}]"
				right_brace = function_declaration[7].getstr() 
				parsed_line = f"{datatype_name} {identifier} {left_parenthesis} {param_list_string} {right_parenthesis} {left_brace} {program_definition_string} {right_brace}"
				global_variables_instance.set_parsed_line(parsed_line)
				return FunctionDefinition(self.builder, self.module, self.base_func, identifier, params_list, program_definition)
			
			if len(function_declaration) == 7:
				right_parenthesis = function_declaration[3].getstr()
				left_brace = function_declaration[4].getstr()
				program_definition = function_declaration[5]
				program_definition_string = f"[{','.join([str(element) for element in program_definition])}]"
				right_brace = function_declaration[6].getstr()
				parsed_line = f"{datatype_name} {identifier} {left_parenthesis} {right_parenthesis} {left_brace} {program_definition_string} {right_brace}"
				global_variables_instance.set_parsed_line(parsed_line)
				return FunctionDefinition(self.builder, self.module, self.base_func, identifier, [], program_definition)

		@self.pg.production('params :')
		@self.pg.production('params : type IDENTIFIER')
		@self.pg.production('params : type IDENTIFIER COMMA params')
		def params(params_declaration):
			global_variables_instance = GlobalVariablesSingleton()
			if len(params_declaration) == 0:
				return []

			if len(params_declaration) == 1:
				datatype = params_declaration[0]
				if isinstance(datatype, (Integer, Float, Void)):
					datatype_name = datatype.get_type()
				else:
					datatype_name = "unknown"

				try:
					identifier = params_declaration[1].getstr()
				except:
					identifier = params_declaration[1]

				parsed_line = f"{datatype_name} {identifier}"
				global_variables_instance.set_parsed_line(parsed_line)
				return [params_declaration[0].getstr()]
			else:
				datatype = params_declaration[0]
				if isinstance(datatype, (Integer, Float, Void)):
					datatype_name = datatype.get_type()
				else:
					datatype_name = "unknown"

				try:
					identifier = params_declaration[1].getstr()
				except:
					identifier = params_declaration[1]

				params_list = params_declaration[3]
				params_list_string = f"[{','.join([str(param) for param in params_list])}]"
				parsed_line = f"{datatype_name} {identifier}, {params_list_string}"
				global_variables_instance.set_parsed_line(parsed_line)
				return [params_declaration[0].getstr()] + params_declaration[3]
			

		@self.pg.production('expression : expression ADD_OPERATOR expression')
		@self.pg.production('expression : expression SUBSTRACTION_OPERATOR expression')
		@self.pg.production('expression : expression MULTIPLICATION_OPERATOR expression')
		@self.pg.production('expression : expression DIVISION_OPERATOR expression')
		def expression_arithmetic(expression_declaration):
			global_variables_instance = GlobalVariablesSingleton()
			left_operand_expression = expression_declaration[0]
			right_operand_expression = expression_declaration[2]
			operator = expression_declaration[1]
			operator_symbol = operator.getstr()

			if isinstance(left_operand_expression, (Integer, Float)):
				left_variable = left_operand_expression.get_name()
				left_operand = left_operand_expression.get_value()
				if isinstance(left_operand, (Integer, Float)):
					left_operand = left_operand.get_value()
			else:
				left_variable = left_operand_expression
				left_operand = left_operand_expression

			if isinstance(right_operand_expression, (Integer, Float)):
				right_variable = right_operand_expression.get_name()
				right_operand = right_operand_expression.get_value()
				if isinstance(right_operand, (Integer, Float)):
					right_operand = right_operand.get_value()
			else:
				right_variable = left_operand_expression
				right_operand = right_operand_expression
			

			parsed_line = f"{left_variable} {operator_symbol} {right_variable}"
			global_variables_instance.set_parsed_line(parsed_line)

			if operator.gettokentype() == 'ADD_OPERATOR':
				return Sum(self.builder, self.module, self.base_func, left_operand, right_operand)
			
			if operator.gettokentype() == 'SUBSTRACTION_OPERATOR':
				return Substraction(self.builder, self.module, self.base_func, left_operand, right_operand)
			
			if operator.gettokentype() == 'MULTPLICATION_OPERATOR':
				return Multiplication(self.builder, self.module, self.base_func, left_operand, right_operand)
			
			if operator.gettokentype() == 'DIVISION_OPERATOR':
				return Division(self.builder, self.module, self.base_func, left_operand, right_operand)

		@self.pg.production('expression : expression LESS_THAN_OPERATOR expression')
		@self.pg.production('expression : expression LESS_THAN_OR_EQUAL_OPERATOR expression')
		@self.pg.production('expression : expression GREATER_THAN_OPERATOR expression')
		@self.pg.production('expression : expression GREATER_THAN_OR_EQUAL_OPERATOR expression')
		@self.pg.production('expression : expression EQUALITY_OPERATOR expression')
		@self.pg.production('expression : expression INEQUALITY_OPERATOR expression')
		@self.pg.production('expression : expression OR_LOGICAL_OPERATOR expression')
		@self.pg.production('expression : expression AND_LOGICAL_OPERATOR expression')
		@self.pg.production('expression : LEFT_PARENTHESIS expression RIGHT_PARENTHESIS LESS_THAN_OPERATOR LEFT_PARENTHESIS expression RIGHT_PARENTHESIS')
		@self.pg.production('expression : LEFT_PARENTHESIS expression RIGHT_PARENTHESIS LESS_THAN_OR_EQUAL_OPERATOR LEFT_PARENTHESIS expression RIGHT_PARENTHESIS')
		@self.pg.production('expression : LEFT_PARENTHESIS expression RIGHT_PARENTHESIS GREATER_THAN_OPERATOR LEFT_PARENTHESIS expression RIGHT_PARENTHESIS')
		@self.pg.production('expression : LEFT_PARENTHESIS expression RIGHT_PARENTHESIS GREATER_THAN_OR_EQUAL_OPERATOR LEFT_PARENTHESIS expression RIGHT_PARENTHESIS')
		@self.pg.production('expression : LEFT_PARENTHESIS expression RIGHT_PARENTHESIS EQUALITY_OPERATOR LEFT_PARENTHESIS expression RIGHT_PARENTHESIS')
		@self.pg.production('expression : LEFT_PARENTHESIS expression RIGHT_PARENTHESIS INEQUALITY_OPERATOR LEFT_PARENTHESIS expression RIGHT_PARENTHESIS')
		@self.pg.production('expression : LEFT_PARENTHESIS expression RIGHT_PARENTHESIS OR_LOGICAL_OPERATOR LEFT_PARENTHESIS expression RIGHT_PARENTHESIS')
		@self.pg.production('expression : LEFT_PARENTHESIS expression RIGHT_PARENTHESIS AND_LOGICAL_OPERATOR LEFT_PARENTHESIS expression RIGHT_PARENTHESIS')
		def expression_logical_operators(expression_declaration):
			if len(expression_declaration) == 3:
				left_operand_expression = expression_declaration[0]
				right_operand_expression = expression_declaration[2]
				logical_operator = expression_declaration[1]
			elif len(expression_declaration) == 7:
				left_operand_expression = expression_declaration[1]
				right_operand_expression = expression_declaration[5]
				logical_operator = expression_declaration[3]

			if isinstance(left_operand_expression, (Integer, Float)):
				left_operand = left_operand_expression.get_value()
				if isinstance(left_operand, (Integer, Float)):
					left_operand = left_operand.get_value()
			else:
				left_operand = left_operand_expression

			if isinstance(right_operand_expression, (Integer, Float)):
				right_operand = right_operand_expression.get_value()
				if isinstance(right_operand, (Integer, Float)):
					right_operand = right_operand.get_value()
			else:
				right_operand = right_operand_expression

			if logical_operator.gettokentype() == 'LESS_THAN_OPERATOR':
				return LessThan(self.builder, self.module, self.base_func, left_operand, right_operand)
		
			if logical_operator.gettokentype() == 'LESS_THAN_OR_EQUAL_OPERATOR':
				return LessThanOrEqual(self.builder, self.module, self.base_func, left_operand, right_operand)
			
			if logical_operator.gettokentype() == 'GREATER_THAN_OPERATOR':
				return GreaterThan(self.builder, self.module, self.base_func, left_operand, right_operand)
			
			if logical_operator.gettokentype() == 'GREATER_THAN_OR_EQUAL_OPERATOR':
				return GreaterThanOrEqual(self.builder, self.module, self.base_func, left_operand, right_operand)
			
			if logical_operator.gettokentype() == 'EQUALITY_OPERATOR':
				return Equality(self.builder, self.module, self.base_func, left_operand, right_operand)
			
			if logical_operator.gettokentype() == 'INEQUALITY_OPERATOR':
				return Inequality(self.builder, self.module, self.base_func, left_operand, right_operand)
			
			if logical_operator.gettokentype() == 'OR_LOGICAL_OPERATOR':
				return OrLogical(self.builder, self.module, self.base_func, left_operand, right_operand)
			
			if logical_operator.gettokentype() == 'AND_LOGICAL_OPERATOR':
				return AndLogical(self.builder, self.module, self.base_func, left_operand, right_operand)
			
			

		@self.pg.production('expression : INTEGER')
		def integer(expression_declaration):
			variable = expression_declaration[0]
			value = 0
			if isinstance(variable, Integer):
				value = variable.getstr()
			else:
				value = variable.value

			return Integer(self.builder, self.module, self.base_func, "", value)

		@self.pg.production('expression : FLOAT')
		def float(expression_declaration):
			return Float(self.builder, self.module, self.base_func, "", expression_declaration[0].value)
		
		@self.pg.production('expression : IDENTIFIER')
		def expression_variable(expression_declaration):
			global_variables_instance = GlobalVariablesSingleton()
			identifier = str()

			try:
				identifier = expression_declaration[0].getstr()
			except:
				identifier = expression_declaration[0]

			if identifier is None or '':
				raise ValueError('No se pudo obtener el nombre de variable')

			if global_variables_instance.get_variable(identifier) is None:
				raise ValueError(f"Variable {identifier} no ha sido declarada")
			
			return global_variables_instance.get_variable(identifier)
		
		@self.pg.production('statement : IF_KEYWORD LEFT_PARENTHESIS expression RIGHT_PARENTHESIS LEFT_BRACE program RIGHT_BRACE')
		def if_statement(if_statement_declaration):
			global_variables_instance = GlobalVariablesSingleton()

			condition = if_statement_declaration[2]
			condition_string = str(condition)
			left_brace = if_statement_declaration[4].getstr()
			body = if_statement_declaration[5]
			body_string = f"[{','.join([str(element) for element in body])}]"
			right_brace = if_statement_declaration[6].getstr()

			parsed_line = f"if({condition_string}){left_brace}{body_string}{right_brace}"
			global_variables_instance.set_parsed_line(parsed_line)
			return IfElseStatement(self.builder, self.module, self.base_func, condition, body)
		
		@self.pg.production('statement : IF_KEYWORD LEFT_PARENTHESIS expression RIGHT_PARENTHESIS LEFT_BRACE program RIGHT_BRACE ELSE_KEYWORD LEFT_BRACE program RIGHT_BRACE')
		def if_else_statement(if_else_statement_declaration):
			global_variables_instance = GlobalVariablesSingleton()

			condition = if_else_statement_declaration[2]
			condition_string = str(condition)
			left_brace = if_else_statement_declaration[4].getstr()
			if_body = if_else_statement_declaration[5]
			if_body_string = f"[{','.join([str(element) for element in if_body])}]"
			right_brace = if_else_statement_declaration[6].getstr()
			else_body = if_else_statement_declaration[9]
			else_body_string = f"[{','.join([str(element) for element in else_body])}]"

			parsed_line = f"if({condition_string}){left_brace}{if_body_string}{right_brace}else{left_brace}{else_body_string}{right_brace}"
			global_variables_instance.set_parsed_line(parsed_line)
			return IfElseStatement(self.builder, self.module, self.base_func, condition, if_body, else_body)

		@self.pg.production('print : PRINT_FUNCTION LEFT_PARENTHESIS STRING RIGHT_PARENTHESIS SEMICOLON')
		@self.pg.production('print : PRINT_FUNCTION LEFT_PARENTHESIS expression RIGHT_PARENTHESIS SEMICOLON')
		def print_function(print_declaration):
			input_expression = print_declaration[2]
			if isinstance(input_expression, (Integer, Float)):
				input = input_expression.get_value()
				if isinstance(input, (Integer, Float)):
					input = input.get_value()
			else:
				input =  input_expression

			return Printf(self.builder, self.module, input)	
		
		@self.pg.error
		def error_handle(token):
			raise ParsingError(f"Error en el analisis sintactico", token)

	def get_parser(self):
		return self.pg.build()

