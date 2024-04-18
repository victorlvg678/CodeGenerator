from llvmlite import ir
class Integer():
    def __init__(self, builder, module, base_func, name, value):
        self.builder = builder
        self.module = module
        self.base_func = base_func
        self.name = name
        self.value = value

    def set_name(self, name):
        self.name = name

    def set_value(self, value):
        self.value = value

    def set_builder(self, builder):
        self.builder = builder

    def set_module(self, module):
        self.module = module

    def set_base_func(self, base_func):
        self.base_func = base_func

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value

    def get_type(self):
        return "int"
    
    def get_builder(self):
        return self.builder
    
    def get_module(self):
        return self.module
    
    def get_base_func(self):
        return self.base_func

    def __str__(self):
        return f"Integer(name=\"{self.name}\", value=\"{self.value}\")"
    
    def eval(self):
        if self.name:
            variable = self.builder.alloca(ir.InType(32), name = self.name)
            self.builder.store(ir.InType(32)(self.value), variable)

        eval_result = ir.Constant(ir.InType(32), int(self.value))
        return eval_result


class Float():
    def __init__(self, builder, module, base_func, name, value):
        self.builder = builder
        self.module = module
        self.base_func = base_func
        self.name = name
        self.value = value

    def set_name(self, name):
        self.name = name

    def set_value(self, value):
        self.value = value

    def set_builder(self, builder):
        self.builder = builder

    def set_module(self, module):
        self.module = module

    def set_base_func(self, base_func):
        self.base_func = base_func

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value

    def get_type(self):
        return "float"
    
    def get_builder(self):
        return self.builder
    
    def get_module(self):
        return self.module

    def get_base_func(self):
        return self.base_func

    def __str__(self):
        return f"Float(name=\"{self.name}\", value=\"{self.value}\")"

    def eval(self):
        if self.name:
            variable = self.builder.alloca(ir.FloatType(32), name = self.name)
            self.builder.store(ir.FloatType(32)(self.value), variable)

        eval_result = ir.Constant(ir.FloatType(32), float(self.value))
        return eval_result


class Void():
    def __init__(self, builder, module, base_func, name):
        self.builder = builder
        self.module = module
        self.base_func = base_func
        self.name = name

    def set_name(self, name):
        self.name = name

    def set_builder(self, builder):
        self.builder = builder

    def set_module(self, module):
        self.module = module

    def set_base_func(self, base_func):
        self.base_func = base_func

    def get_name(self):
        return self.name

    def get_type(self):
        return "void"
    
    def get_builder(self):
        return self.builder
    
    def get_module(self):
        return self.module
    
    def get_base_func(self):
        return self.base_func

    def __str__(self):
        return f"Void(name=\"{self.name}\", value=\"{self.value}\")"

    def eval(self):
        eval_result = ir.Constant(ir.IntType(8), int(0))
        return eval_result


class BinaryOperation():
    def __init__(self, builder, module, base_func, left_operand, right_operand):
        self.builder = builder
        self.module = module
        self.base_func = base_func
        self.left_operand = left_operand
        self.right_operand = right_operand


class Sum(BinaryOperation):
    def __init__(self, builder, module, base_func, left_operand, right_operand):
        super().__init__(builder, module, base_func, left_operand, right_operand)

    def __str__(self):
        return f"Sum(left_operand=\"{self.left_operand}\", right_operand=\"{self.right_operand}\")"

    def eval(self):
        eval_result = self.builder.add(self.left.eval(), self.right_eval())
        return eval_result


class Substraction(BinaryOperation):
    def __init__(self, builder, module, base_func, left_operand, right_operand):
        super().__init__(builder, module, base_func, left_operand, right_operand)

    def __str__(self):
        return f"Substraction(left_operand=\"{self.left_operand}\", right_operand=\"{self.right_operand}\")"

    def eval(self):
        eval_result = self.builder.sub(self.left.eval(), self.right_eval())
        return eval_result


class Multiplication(BinaryOperation):
    def __init__(self, builder, module, base_func, left_operand, right_operand):
        super().__init__(builder, module, base_func, left_operand, right_operand)

    def __str__(self):
        return f"Multiplication(left_operand=\"{self.left_operand}\", right_operand=\"{self.right_operand}\")"

    def eval(self):
        eval_result = self.builder.mul(self.left.eval(), self.right_eval())
        return eval_result


class Division(BinaryOperation):
    def __init__(self, builder, module, base_func, left_operand, right_operand):
        super().__init__(builder, module, base_func, left_operand, right_operand)

    def __str__(self):
        return f"Division(left_operand=\"{self.left_operand}\", right_operand=\"{self.right_operand}\")"

    def eval(self):
        eval_result = self.builder.sdiv(self.left.eval(), self.right_eval())
        return eval_result

class LessThan(BinaryOperation):
    def __init__(self, builder, module, base_func, left_operand, right_operand):
        super().__init__(builder, module, base_func, left_operand, right_operand)

    def __str__(self):
        return f"LessThan(left_operand=\"{self.left_operand}\", right_operand=\"{self.right_operand}\")"

    def eval(self):
        eval_result = self.builder.icmp_signed("<", self.left.eval(), self.right_eval())
        return eval_result

class LessThanOrEqual(BinaryOperation):
    def __init__(self, builder, module, base_func, left_operand, right_operand):
        super().__init__(builder, module, base_func, left_operand, right_operand)

    def __str__(self):
        return f"LessThanOrEqual(left_operand=\"{self.left_operand}\", right_operand=\"{self.right_operand}\")"

    def eval(self):
        eval_result = self.builder.icmp_signed("<=", self.left.eval(), self.right_eval())
        return eval_result


class GreaterThan(BinaryOperation):
    def __init__(self, builder, module, base_func, left_operand, right_operand):
        super().__init__(builder, module, base_func, left_operand, right_operand)

    def __str__(self):
        return f"GreaterThan(left_operand=\"{self.left_operand}\", right_operand=\"{self.right_operand}\")"

    def eval(self):
        eval_result = self.builder.icmp_signed(">", self.left.eval(), self.right_eval())
        return eval_result


class GreaterThanOrEqual(BinaryOperation):
    def __init__(self, builder, module, base_func, left_operand, right_operand):
        super().__init__(builder, module, base_func, left_operand, right_operand)

    def __str__(self):
        return f"GreaterThanOrEqual(left_operand=\"{self.left_operand}\", right_operand=\"{self.right_operand}\")"

    def eval(self):
        eval_result = self.builder.icmp_signed(">=", self.left.eval(), self.right_eval())
        return eval_result


class Equality(BinaryOperation):
    def __init__(self, builder, module, base_func, left_operand, right_operand):
        super().__init__(builder, module, base_func, left_operand, right_operand)

    def __str__(self):
        return f"Equality(left_operand=\"{self.left_operand}\", right_operand=\"{self.right_operand}\")"

    def eval(self):
        eval_result = self.builder.icmp_signed("==", self.left.eval(), self.right_eval())
        return eval_result


class Inequality(BinaryOperation):
    def __init__(self, builder, module, base_func, left_operand, right_operand):
        super().__init__(builder, module, base_func, left_operand, right_operand)

    def __str__(self):
        return f"Inequality(left_operand=\"{self.left_operand}\", right_operand=\"{self.right_operand}\")"

    def eval(self):
        eval_result = self.builder.icmp_signed("!=", self.left.eval(), self.right_eval())
        return eval_result

class AndLogical(BinaryOperation):
    def __init__(self, builder, module, base_func, left_operand, right_operand):
        super().__init__(builder, module, base_func, left_operand, right_operand)

    def __str__(self):
        return f"AndLogical(left_operand=\"{self.left_operand}\", right_operand=\"{self.right_operand}\")"

    def eval(self):
        eval_result = self.builder.and_(self.left.eval(), self.right_eval())
        return eval_result
    
class OrLogical(BinaryOperation):
    def __init__(self, builder, module, base_func, left_operand, right_operand):
        super().__init__(builder, module, base_func, left_operand, right_operand)

    def __str__(self):
        return f"OrLogical(left_operand=\"{self.left_operand}\", right_operand=\"{self.right_operand}\")"

    def eval(self):
        eval_result = self.builder.or_(self.left.eval(), self.right_eval())
        return eval_result


class FunctionDefinition:
    def __init__(self, builder, module, base_func, name, params, body):
        self.builder = builder
        self.module = module
        self.name = name
        self.params = params
        self.body = body
        self._function = None
        self.base_func = base_func

    def __str__(self):
        params_str = ', '.join(self.params) if self.params else ''
        return f"FunctionDefinition(name={self.name}, params=[{params_str}], body={self.body})"

    def eval(self):
        func_type = ir.FunctionType(ir.VoidType(), [ir.IntType(32)] * len(self.params))

        function = ir.Function(self.module, func_type, name=self.name)
        self._function = function

        for arg, arg_name in zip(function.args, self.params):
            arg.name = arg_name

        entry_block = self.base_func.append_basic_block(name = self.name)
        builder = ir.IRBuilder(entry_block)

        self.body.set_builder(builder)
        self.body.set_module(self.module)
        self.body.set_base_func(self.base_func)
        new_block = self.base_func.append_basic_block(entry_block)
        self.base_func.switch_to_block(new_block)

        self.body.eval()

        ir_pass_manager = ir.PassManager()
        ir_pass_manager.verify()

        return function
        

class Printf():
    def __init__(self, builder, module, base_func, printf, value):
        self.builder = builder
        self.module = module
        self.base_func = base_func
        self.printf = printf
        self.value = value

    def eval(self):
        value = self.value.eval()
        voidptr_ty = ir.IntType(8).as_pointer()
        fmt = "%i \n\0"
        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)), bytearray(fmt.encode("utf8")))
        global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name = "fstr")
        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt
        fmt_arg = self.builder.bitcast(global_fmt, voidptr_ty)
        self.builder.call(self.printf, [fmt_arg, value])

class IfElseStatement():
    def __init__(self, builder, module, base_func, condition, if_body, else_body=None):
        self.builder = builder
        self.module = module
        self.base_func = base_func
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body

    def __str__(self):
        if self.else_body is not None:
            return f"IfElseStatement(condition={self.condition}, if_body={self.if_body}, else_body={self.else_body})"
        else:
            return f"IfElseStatement(condition={self.condition}, if_body={self.if_body})"
        
    def eval(self):
        if self.else_body is not None:
            with self.builder.if_then(self.condition) as then:
                with then:
                    print(self.if_body)
                    return None
        else:
            with self.builder.if_else(self.condition) as (then, otherwise):
                with then:
                    print(self.if_body)
                    return None
                with otherwise:
                    print(self.else_body)
                    return None
        return None