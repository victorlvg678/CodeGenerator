import re

class LexerError():
    def __init__(self, message, source_position = None):
        self.message = message
        self.source_position = source_position
        self.index_number = 0
        self.line_number = 0
        self.column_number = 0
        self.get_source_position_elements()

    def get_message(self):
        return self.message
    
    def set_message(self, message):
        self.message = message

    def get_position(self):
        return self.position
    
    def set_position(self, source_position):
        self.source_position = source_position

    def get_index_number(self):
        return self.index_number
    
    def get_line_number(self):
        return self.line_number
    
    def get_column_number(self):
        return self.column_number


    def get_source_position_elements(self):
        source_position_string = str(self.source_position)
        elements = re.split("[^0-9]+", source_position_string)
        elements = ' '.join(elements).split()
        
        if len(elements) == 3:
            self.index_number = elements[0]
            self.line_number = elements[1]
            self.column_number = elements[2]

    def __str__(self):
        if self.source_position == None:
            return self.message
        
        return f"{self.message} en ({self.get_source_position_elements_as_string()})"
    
    def get_source_position_elements_as_string(self):
        return "Linea: {:4} - Columna: {:4} - Indice: {:4}".format(str(self.line_number), str(self.column_number), str(self.index_number))
    
class ParserError():
    def __init__(self, message, source_position = None):
        self.message = message
        self.source_position = source_position
        self.index_number = 0
        self.line_number = 0
        self.column_number = 0
        self.get_source_position_elements()

    def get_message(self):
        return self.message
    
    def set_message(self, message):
        self.message = message

    def get_position(self):
        return self.position
    
    def set_position(self, source_position):
        self.source_position = source_position

    def get_index_number(self):
        return self.index_number
    
    def get_line_number(self):
        return self.line_number
    
    def get_column_number(self):
        return self.column_number


    def get_source_position_elements(self):
        source_position_string = str(self.source_position)
        elements = re.split("[^0-9]+", source_position_string)
        elements = ' '.join(elements).split()
        
        if len(elements) == 3:
            self.index_number = elements[0]
            self.line_number = elements[1]
            self.column_number = elements[2]

    def __str__(self):
        if self.source_position == None:
            return self.message
        
        return f"{self.message} en ({self.get_source_position_elements_as_string()})"
    
    def get_source_position_elements_as_string(self):
        return "Linea: {:4} - Columna: {:4} - Indice: {:4}".format(str(self.line_number), str(self.column_number), str(self.index_number))