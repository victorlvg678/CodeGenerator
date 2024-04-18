import re

"""
This is the following symbols table:
+----------------------------------------+-------+-------------------------------------------+------------+
| Symbol                                 | Type  | Type in Spanish                           | Examples   |
+----------------------------------------+-------+-------------------------------------------+------------+
| IDENTIFIER                             |  0    | Identificador                             |  foo, bar  |
| INTEGER                                |  1    | Entero                                    |  1, 2, 3   |
| FLOAT                                  |  2    | Real                                      |  1.2, 1.33 |
| STRING                                 |  3    | Cadena                                    |   "foo"    |
| INTEGER_DATATYPE                       |  4    | Tipo<Entero>                              |   int      |
| FLOAT_DATATYPE                         |  5    | Tipo<Real>                                |   float    |
| VOID_DATATYPE                          |  6    | Tipo<Vacio>                               |   void     | 
| ADD_OPERATOR                           |  7    | OperadorAritmetico<Suma>                  |     +      |
| SUBSTRACTION_OPERATOR                  |  8    | OperadorAritmetico<Resta>                 |     -      |
| MULTIPLICATION_OPERATOR                |  9    | OperadorAritmetico<Multiplicacion>        |     *      |
| DIVISION_OPERATOR                      |  10   | OperadorAritmetico<Division>              |     /      |
| LESS_THAN_OPERATOR                     |  11   | OperadorRelacional<MenorQue>              |     <      |
| LESS_THAN_OR_EQUAL_OPERATOR            |  12   | OperadorRelacional<MenorOIgualQue>        |    <=      |
| GREATER_THAN_OPERATOR                  |  13   | OperadorRelacional<MayorQue>              |     >      |
| GREATER_THAN_OR_EQUAL_OPERATOR         |  14   | OperadorRelacional<MayorOIgualQue>        |     >=     |
| EQUALITY_OPERATOR                      |  15   | OperadorRelacional<Igualdad>              |     ==     |
| INEQUALITY_OPERATOR                    |  16   | OperadorRelacional<Desigualdad>           |     !=     |
| OR_LOGICAL_OPERATOR                    |  17   | OperadorLogico<Disyuncion>                |     ||     |
| AND_LOGICAL_OPERATOR                   |  18   | OperadorLogico<Conjuncion>                |     &&     |
| NOT_LOGICAL_OPERATOR                   |  19   | OperadorLogico<Negacion>                  |     !      |
| SEMICOLON                              |  20   | PuntoYComa                                |     ;      |
| COMMA                                  |  21   | Coma                                      |     ,      |
| LEFT_PARENTHESIS                       |  22   | Parentesis<Izquierdo>                     |     (      |
| RIGHT_PARENTHESIS                      |  23   | Parentesis<Derecho>                       |     )      |
| LEFT_BRACE                             |  24   | Corchete<Izquierdo>                       |     {      |
| RIGHT_BRACE                            |  25   | Corchete<Derecho>                         |     }      |
| ASSIGNMENT                             |  26   | Asignacion                                |     =      |
| IF_KEYWORD                             |  27   | PalabraClave<if>                          |     if     |
| WHILE_KEYWORD                          |  28   | PalabraClave<while>                       |    while   |
| RETURN_KEYWORD                         |  29   | PalabraClave<return>                      |    return  |
| ELSE_KEYWORD                           |  30   | PalabraClave<else>                        |    else    |
| NEW_LINE                               |  31   | SaltoDeLinea                              |    CRLF    |
| PRINT_FUNCTION                         |  32   | Function<Imprimir>                        |   printf   |
+----------------------------------------+-------+-------------------------------------------+------------+
"""

class TokenInSpanish():
    def __init__(self, token_type, value, source_position):
        self.token_type = token_type
        self.source_position = source_position
        self.line_number = 0
        self.column_number = 0
        self.index_number = 0
        self.value = value
        self.get_token_type_in_spanish_and_type_number()
        self.get_source_position_elements()

    def get_token_type_in_spanish_and_type_number(self):
        if self.token_type == "IDENTIFIER":
            self.token_type_in_spanish = "Identificador"
            self.type_number = 0
            return
        
        if self.token_type == "INTEGER":
            self.token_type_in_spanish = "Entero"
            self.type_number = 1
            return
        
        if self.token_type == "FLOAT":
            self.token_type_in_spanish = "Real"
            self.type_number = 2
            return
        
        if self.token_type == "STRING":
            self.token_type_in_spanish = "Cadena"
            self.type_number = 3
            return
        
        if self.token_type == "INTEGER_DATATYPE":
            self.token_type_in_spanish = "Tipo<Entero>"
            self.type_number = 4
            return
        
        if self.token_type == "FLOAT_DATATYPE":
            self.token_type_in_spanish = "Tipo<Real>"
            self.type_number = 5
            return
        
        if self.token_type == "VOID_DATATYPE":
            self.token_type_in_spanish = "Tipo<Vacio>"
            self.type_number = 6
            return
        
        if self.token_type == "ADD_OPERATOR":
            self.token_type_in_spanish = "OperadorAritmetico<Suma>"
            self.type_number = 7
            return
        
        if self.token_type == 'SUBSTRACTION_OPERATOR':
            self.token_type_in_spanish = "OperadorAritmetico<Resta>"
            self.type_number = 8
            return
        
        if self.token_type == 'MULTIPLICATION_OPERATOR':
            self.token_type_in_spanish = "OperadorAritmetico<Multiplicacion>"
            self.type_number = 9
            return
        
        if self.token_type == 'DIVISION_OPERATOR':
            self.token_type_in_spanish = "OperadorAritmetico<Division>"
            self.type_number = 10
            return
        
        if self.token_type == 'LESS_THAN_OPERATOR':
            self.token_type_in_spanish = "OperadorRelacional<MenorQue>"
            self.type_number = 11
            return
        
        if self.token_type == 'LESS_THAN_OR_EQUAL_OPERATOR':
            self.token_type_in_spanish = "OperadorRelacional<MenorOIgualQue>"
            self.type_number = 12
            return
        
        if self.token_type == 'GREATER_THAN_OPERATOR':
            self.token_type_in_spanish = "OperadorRelacional<MayorQue>"
            self.type_number = 13
            return
        
        if self.token_type == 'GREATER_THAN_OR_EQUAL_OPERATOR':
            self.token_type_in_spanish = "OperadorRelacional<MayorOIgualQue>"
            self.type_number = 14
            return
        
        if self.token_type == 'EQUALITY_OPERATOR':
            self.token_type_in_spanish = "OperadorRelacional<Igualdad>"
            self.type_number = 15
            return
        
        if self.token_type == 'INEQUALITY_OPERATOR':
            self.token_type_in_spanish = "OperadorRelacional<Desigualdad>"
            self.type_number = 16
            return
        
        if self.token_type == 'OR_LOGICAL_OPERATOR':
            self.token_type_in_spanish = "OperadorLogico<Disyuncion>"
            self.type_number = 17
            return

        if self.token_type == 'AND_LOGICAL_OPERATOR':
            self.token_type_in_spanish = "OperadorLogico<Conjuncion>"
            self.type_number = 18
            return
        
        if self.token_type == 'NOT_LOGICAL_OPERATOR':
            self.token_type_in_spanish = "OperadorLogico<Negacion>"
            self.type_number = 19
            return
        
        if self.token_type == 'SEMICOLON':
            self.token_type_in_spanish = "PuntoYComa"
            self.type_number = 20
            return
        
        if self.token_type == 'COMMA':
            self.token_type_in_spanish = "Coma"
            self.type_number = 21
            return
        
        if self.token_type == 'LEFT_PARENTHESIS':
            self.token_type_in_spanish = "Parentesis<Izquierdo>"
            self.type_number = 22
            return
        
        if self.token_type == 'RIGHT_PARENTHESIS':
            self.token_type_in_spanish = "Parentesis<Derecho>"
            self.type_number = 23
            return
        
        if self.token_type == 'LEFT_BRACE':
            self.token_type_in_spanish = "Corchete<Izquierdo>"
            self.type_number = 24
            return
        
        if self.token_type == 'RIGHT_BRACE':
            self.token_type_in_spanish = "Corchete<Derecho>"
            self.type_number = 25
            return
        
        if self.token_type == 'ASSIGNMENT':
            self.token_type_in_spanish = "Asignacion"
            self.type_number = 26
            return
        
        if self.token_type == 'IF_KEYWORD':
            self.token_type_in_spanish = "PalabraClave<if>"
            self.type_number = 27
            return
        
        if self.token_type == 'WHILE_KEYWORD':
            self.token_type_in_spanish = "PalabraClave<while>"
            self.type_number = 28
            return
        
        if self.token_type == 'RETURN_KEYWORD':
            self.token_type_in_spanish = "PalabraClave<return>"
            self.type_number = 29
            return
        
        if self.token_type == 'ELSE_KEYWORD':
            self.token_type_in_spanish = "PalabraClave<else>"
            self.type_number = 30
            return 
                
        if self.token_type == "NEW_LINE":
            self.token_type_in_spanish = "SaltoDeLinea"
            self.type_number = 31
            return
        
        if self.token_type == "PRINT_FUNCTION":
            self.token_type_in_spanish = "Funcion<Imprimir>"
            self.type_number = 32
            return

        self.token_type_in_spanish = "Desconocido"
        self.type_number = -1        

    def get_source_position_elements(self):
        source_position_string = str(self.source_position)
        elements = re.split("[^0-9]+", source_position_string)
        elements = ' '.join(elements).split()
        
        if len(elements) == 3:
            self.index_number = elements[0]
            self.line_number = elements[1]
            self.column_number = elements[2]


    def set_token_type(self, token_type):
        self.token_type = token_type

    def set_source_position(self, source_position):
        self.source_position = source_position

    def get_token_type_in_spanish(self):
        return self.token_type_in_spanish
    
    def get_token_type_number(self):
        return self.type_number
    
    def get_source_position(self):
        return self.source_position
    
    def get_index_number(self):
        return self.index_number
    
    def get_line_number(self):
        return self.line_number
    
    def get_column_number(self):
        return self.column_number

    def __str__(self):
        return "Token: {:40} - Lexema: {:10} - Tipo: {:4} - {:47}".format(str(self.token_type_in_spanish), str(self.value), str(self.type_number), self.get_source_position_elements_as_string())
    
    def get_source_position_elements_as_string(self):
        return "Linea: {:4} - Columna: {:4} - Indice: {:4}".format(str(self.line_number), str(self.column_number), str(self.index_number))