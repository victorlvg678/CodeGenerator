from codegen import CodeGen
class GlobalVariablesSingleton:
    _instance = None
    _lexical_analysis_failed = True
    _final_tokens = []
    _final_tokens_in_spanish = []
    _variables = {}
    _parsed_lines = []
    _codegen = CodeGen()
    _is_ir_generated = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GlobalVariablesSingleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


    def set_lexical_analysis_failed(self, lexical_analysis_failed):
        self._lexical_analysis_failed = lexical_analysis_failed

    def set_final_tokens(self, final_tokens):
        self._final_tokens = final_tokens

    def set_final_tokens_in_spanish(self, final_tokens_in_spanish):
        self._final_tokens_in_spanish = final_tokens_in_spanish

    def set_variables(self, variables):
        self._variables = variables

    def set_variable(self, name, value):
        self._variables[name] = value

    def set_parsed_lines(self, parsed_lines):
        self._parsed_lines = parsed_lines

    def set_parsed_line(self, line):
        if self._parsed_lines is None:
            self._parsed_lines = []

        self._parsed_lines.append(line)

    def set_codegen(self, codegen):
        self._codegen = codegen

    def set_is_ir_generated(self, value):
        self._is_ir_generated = value
  
    def get_lexical_analysis_failed(self):
        return self._lexical_analysis_failed

    def get_final_tokens(self):
        return self._final_tokens

    def get_final_tokens_in_spanish(self):
        return self._final_tokens_in_spanish

    def get_variables(self):
        return self._variables
    
    def get_variable(self, name):
        return self._variables.get(name)
    
    def get_parsed_lines(self):
        return self._parsed_lines
    
    def get_codegen(self):
        return self._codegen
    
    def get_codegen_module(self):
        if self.get_codegen is None:
            self._codegen = CodeGen()

        return self._codegen.module
    
    def get_codegen_builder(self):
        if self.get_codegen is None:
            self._codegen = CodeGen()

        return self._codegen.builder
    
    def get_codegen_base_func(self):
        if self.get_codegen is None:
            self._codegen = CodeGen()

        return self._codegen.base_func
    
    def get_codegen_printf(self):
        if self.get_codegen is None:
            self._codegen = CodeGen()

        return self._codegen.printf
    
    def get_is_ir_generated(self):
        return self._is_ir_generated
    
