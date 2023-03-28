"""!
@package program
@file program.py
@author Samuel Stolarik
@date 2023-03-22
"""
from abc import ABC, abstractmethod
from enum import Enum


class ArgumentType(Enum):
    VAR = 'var'
    CONST_VALUE = 'const'
    LABEL = 'label'


class DataType(Enum):
    NIL = 'nil'
    INT = 'int'
    STRING = 'string'
    BOOL = 'bool'


class FrameType(Enum):
    GF = 'gf'
    TF = 'tf'
    LF = 'lf'


class Argument(ABC):
    def __init__(self, arg_type: ArgumentType):
        self.arg_type = arg_type

    def get_arg_type(self) -> ArgumentType:
        return self.arg_type


class Label(Argument):
    def __init__(self, label: str):
        super().__init__(ArgumentType.LABEL)
        self.label_name = label


class Symbol(Argument, ABC):
    def __init__(self, arg_type: ArgumentType, value=None, value_type: DataType = None):
        super().__init__(arg_type)
        self.value = value
        self.value_type = value_type

    def get_value(self):
        return self.value

    def get_type(self):
        return self.type


class ConstInt(Symbol):
    def __init__(self, value: int):
        super().__init__(ArgumentType.CONST_VALUE, value, DataType.INT)


class ConstBool(Symbol):
    def __init__(self, value: bool):
        super().__init__(ArgumentType.CONST_VALUE, value, DataType.BOOL)


class ConstString(Symbol):
    def __init__(self, value: str):
        super().__init__(ArgumentType.CONST_VALUE, value, DataType.STRING)


class ConstNil(Symbol):
    def __init__(self):
        super().__init__(ArgumentType.CONST_VALUE, 'nil', DataType.NIL)


class Variable(Symbol):
    def __init__(self, name: str, frame: FrameType):
        super().__init__(ArgumentType.VAR)
        self.name = name
        self.frame = frame

    def is_defined(self) -> bool:
        return self.value is None

    def set_value(self, value, value_type: DataType):
        self.value = value
        self.value_type = value_type

    def get_value(self):
        if self.is_defined():
            return self.value
        else:
            # TODO raise undefined var error
            pass

    def get_value_type(self) -> DataType:
        if self.is_defined():
            return self.value_type
        else:
            # TODO raise undefined var error
            pass

    def get_frame(self) -> FrameType:
        return self.frame


class Instruction(ABC):
    """
    @brief Interface for instructions
    """
    def __init__(self, opcode: str, order: int, args: list[Argument]):
        """
        @brief Instruction constructor
        @param opcode:
        @param order:
        @param args:
        """
        self.opcode = opcode
        self.order = order
        self.args = args

    @abstractmethod
    def execute(self):
        pass

    def __repr__(self):
        return str(self.order) + ' ' + self.opcode + ' ' + str(self.args)

    def __lt__(self, other) -> bool:
        return self.order < other.order


# General purpose instructions

class MoveInstruction(Instruction):
    def execute(self):
        pass


class CreteFrameInstruction(Instruction):
    def execute(self):
        pass


class PushFrameInstruction(Instruction):
    def execute(self):
        pass


class PopFrameInstruction(Instruction):
    def execute(self):
        pass


class DefVarInstruction(Instruction):
    def execute(self):
        pass


class Int2CharInstruction(Instruction):
    def execute(self):
        pass


class Stri2IntInstruction(Instruction):
    def execute(self):
        pass


class TypeInstruction(Instruction):
    def execute(self):
        pass


# Flow control instructions

class CallInstruction(Instruction):
    def execute(self):
        pass


class ReturnInstruction(Instruction):
    def execute(self):
        pass


class LabelInstruction(Instruction):
    def execute(self):
        pass


class JumpInstruction(Instruction):
    def execute(self):
        pass


class JumpIfEqInstruction(Instruction):
    def execute(self):
        pass


class JumpIfNeqInstruction(Instruction):
    def execute(self):
        pass


class ExitInstruction(Instruction):
    def execute(self):
        pass


# Flow control instructions
class CallInstruction(Instruction):
    def execute(self):
        pass


class ReturnInstruction(Instruction):
    def execute(self):
        pass


class LabelInstruction(Instruction):
    def execute(self):
        pass


class JumpInstruction(Instruction):
    def execute(self):
        pass


class JumpIfEqInstruction(Instruction):
    def execute(self):
        pass


class JumpIfNeqInstruction(Instruction):
    def execute(self):
        pass

# String instructions

class ConcatInstruction(Instruction):
    def execute(self):
        pass


class StrLenInstruction(Instruction):
    def execute(self):
        pass


class GetCharInstruction(Instruction):
    def execute(self):
        pass


class SetCharInstruction(Instruction):
    def execute(self):
        pass


# Arithmetic instructions

class AddInstruction(Instruction):
    def execute(self):
        pass


class SubInstruction(Instruction):
    def execute(self):
        pass


class IdivInstruction(Instruction):
    def execute(self):
        pass


# Relational instructions

class LtInstruction(Instruction):
    def execute(self):
        pass


class GtInstruction(Instruction):
    def execute(self):
        pass


class EqInstruction(Instruction):
    def execute(self):
        pass


# Logic instructions

class AndInstruction(Instruction):
    def execute(self):
        pass


class OrInstruction(Instruction):
    def execute(self):
        pass


class NotInstruction(Instruction):
    def execute(self):
        pass


# Stack instructions

class PushsInstruction(Instruction):
    def execute(self):
        pass


class PopsInstruction(Instruction):
    def execute(self):
        pass


# IO instructions

class ReadInstruction(Instruction):
    def execute(self):
        pass


class WriteInstruction(Instruction):
    def execute(self):
        pass


class DprintInstruction(Instruction):
    def execute(self):
        pass


class BreakInstruction(Instruction):
    def execute(self):
        pass
