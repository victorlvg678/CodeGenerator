from lexer_implementation import Lexer
from parser_implementation import Parser
from rply.errors import LexingError, ParsingError
from errors import LexerError, ParserError
from tokens import TokenInSpanish
import tkinter as tk
import tkinter.filedialog as filedialog
import os
from global_variables import GlobalVariablesSingleton

tokens = None

def lexical_analysis():
	clear_lexical_analysis()
	text_input = lexical_analysis_input.get("1.0", tk.END)
	prev_token = None
	pending_tokens = True
	lexical_analysis_failed = True
	final_tokens = []
	final_tokens_in_spanish = []
	global_variables_instance = GlobalVariablesSingleton()
	global_variables_instance.set_lexical_analysis_failed(lexical_analysis_failed)
	global_variables_instance.set_final_tokens(final_tokens)
	global_variables_instance.set_final_tokens_in_spanish(final_tokens_in_spanish)
	
	try:
		lexer = Lexer().get_lexer()
	except:
		lexical_analysis_output.insert(tk.END, f'Error durante inicialización de analizador léxico\n')

	try:
		tokens = lexer.lex(text_input)
	except LexingError:
		lexical_analysis_output.insert(tk.END, f'Error en el proceso análisis léxico\n')

	while pending_tokens:
		try:
			for token in tokens:
				token_in_spanish = TokenInSpanish(token.gettokentype(), token.getstr(), token.getsourcepos())
				prev_token = token
				print(token)
				lexical_analysis_output.insert(tk.END, f'{token_in_spanish}\n')
				final_tokens_in_spanish.append(token_in_spanish)
				global_variables_instance.set_final_tokens_in_spanish(final_tokens_in_spanish)

			pending_tokens = False
			lexical_analysis_failed = False

		except LexingError as token_error:
			lexical_analysis_failed = True
			if prev_token is not None:
				prev_token_in_spanish = TokenInSpanish(prev_token.gettokentype(), prev_token.getstr(), prev_token.getsourcepos())
				lexer_error = LexerError(f"Error despues de token (Token: \"{prev_token_in_spanish.get_token_type_in_spanish()}\" - Tipo: {prev_token_in_spanish.get_token_type_number()} - {prev_token_in_spanish.get_source_position_elements_as_string()})", token_error.getsourcepos())
				lexical_analysis_output.insert(tk.END, f'{lexer_error}\n')
			else:
				lexer_error = LexerError(f"Error", token_error.getsourcepos())
				lexical_analysis_output.insert(tk.END, f'{lexer_error}\n')

			line_number = int(lexer_error.get_line_number())
			lines = text_input.split("\n")
			for index in range(0, line_number):
				lines[index] = "\n"
			text_input = "\n".join(lines)
			tokens = lexer.lex(text_input)

	global_variables_instance.set_lexical_analysis_failed(lexical_analysis_failed)

def syntax_analysis():
	clear_syntax_analysis()
	global_variables_instance = GlobalVariablesSingleton()
	if global_variables_instance.get_lexical_analysis_failed():
		syntax_analysis_output.insert(tk.END, f'Analis lexico ha fallado. No se puede realizar analisis sintactico.\n')
		return
	
	text_input = lexical_analysis_input.get("1.0", tk.END)

	try:
		lexer = Lexer().get_lexer()
	except:
		syntax_analysis_output.insert(tk.END, f'Error durante inicialización de analizador léxico\n')

	try:
		global_variables_instance.set_final_tokens(lexer.lex(text_input))
	except LexingError:
		syntax_analysis_output.insert(tk.END, f'Error en el proceso análisis léxico\n')

	try:
		module = global_variables_instance.get_codegen_module()
		builder = global_variables_instance.get_codegen_builder()
		base_func = global_variables_instance.get_codegen_base_func()
		printf = global_variables_instance.get_codegen_printf()
		pg = Parser(module, builder, base_func, printf)
		pg.parse()
		parser = pg.get_parser()
		parse_elements = parser.parse(global_variables_instance.get_final_tokens())
		for parsed_line in global_variables_instance.get_parsed_lines():
			syntax_analysis_output.insert(tk.END, f'(\"{parsed_line}\", VALIDO)\n')

	except ParsingError as parsing_error:
		parser_error = ParserError(f"{parsing_error.message}", parsing_error.getsourcepos())
		syntax_analysis_output.insert(tk.END, f'{parser_error}\n')

def generate_intermediate_code():
	clear_intermediate_code()
	global_variables_instance = GlobalVariablesSingleton()
	code = global_variables_instance.get_codegen()
	if not global_variables_instance.get_is_ir_generated():
		code.create_ir()
		global_variables_instance.set_is_ir_generated(True)

	intermediate_code_output.insert(tk.END, f'{code.output_ir()}\n')

def load_file():
	filepath = filedialog.askopenfilename(initialdir = os.getcwd(), title = "Seleccionar archivo", filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")))

	if filepath is None:
		return
	
	with open(filepath, 'r') as file:
		content = file.read()
		lexical_analysis_input.delete("1.0", tk.END)
		lexical_analysis_input.insert(tk.END, content)

	clear_syntax_analysis()
	clear_lexical_analysis()

def clear_lexical_analysis():
	global_variables_instance = GlobalVariablesSingleton()
	lexical_analysis_output.delete("1.0", tk.END)
	global_variables_instance.set_final_tokens_in_spanish([])
	global_variables_instance.set_lexical_analysis_failed(True)

def clear_syntax_analysis():
	global_variables_instance = GlobalVariablesSingleton()
	syntax_analysis_output.delete("1.0", tk.END)
	global_variables_instance.set_final_tokens([])
	global_variables_instance.set_parsed_lines([])
	global_variables_instance.set_variables({})

def clear_intermediate_code():
	global_variables_instance = GlobalVariablesSingleton()
	intermediate_code_output.delete("1.0", tk.END)
	


window = tk.Tk()
window.title("Subproducto integrador 2: Analizador Sintactico")
window.config(bg = "#0054E3")

lexical_analysis_input = tk.Text(window, height = 10, width = 120)
lexical_analysis_input.grid(row = 0, column = 0, padx = 0, pady = 5)
lexical_analysis_input.config(bg = "#C4C4C4")
 
file_dialog_button = tk.Button(window, text = "Cargar Archivo", command = load_file)
file_dialog_button.grid(row = 0, column = 1, padx = 0, pady = 0)
file_dialog_button.config(bg = "#784CFF")

lexical_analysis_button = tk.Button(window, text = "Analisis lexico", command = lexical_analysis)
lexical_analysis_button.grid(row = 0, column = 2, padx = 5, pady = 0)
lexical_analysis_button.config(bg = "#029800")

lexical_analysis_clear_button = tk.Button(window, text = "Borrar", command = clear_lexical_analysis)
lexical_analysis_clear_button.grid(row = 0, column = 3, padx = 5, pady = 0)

lexical_analysis_output = tk.Text(window, height = 10, width = 160)
lexical_analysis_output.grid(row = 1, column = 0, padx = 0, pady = 5, columnspan = 4)
lexical_analysis_output.config(bg = "#C4C4C4")

syntax_analysis_button = tk.Button(window, text = "Analisis Sintactico", command = syntax_analysis)
syntax_analysis_button.grid(row = 2, column = 1, padx = 0, pady = 0)
syntax_analysis_button.config(bg = "#029800")

syntax_analysis_clear_button = tk.Button(window, text = "Borrar", command = clear_syntax_analysis)
syntax_analysis_clear_button.grid(row = 2, column = 2, padx = 0, pady = 0)

syntax_analysis_output = tk.Text(window, height = 10, width = 120)
syntax_analysis_output.grid(row = 2, column = 0, padx = 0, pady = 5)
syntax_analysis_output.config(bg = "#C4C4C4")

intermediate_code_output = tk.Text(window, height = 10, width = 120)
intermediate_code_output.grid(row = 3, column = 0, padx = 0, pady = 5)
intermediate_code_output.config(bg = "#C4C4C4")

intermediate_code_button = tk.Button(window, text = "Generar codigo intermedio", command = generate_intermediate_code)
intermediate_code_button.grid(row = 3, column = 1, padx = 5, pady = 0)
intermediate_code_button.config(bg = "#029800")

intermediate_code_clear_button = tk.Button(window, text = "Borrar", command = clear_intermediate_code)
intermediate_code_clear_button.grid(row = 3, column = 2, padx = 5, pady = 0)

window.mainloop()


