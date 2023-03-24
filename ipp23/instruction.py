"""!
@package program
@file program.py
@author Samuel Stolarik
@date 2023-03-22
"""
from abc import ABC, abstractmethod
from enum import Enum
import xml.etree.ElementTree as etree


class ArgumentType(Enum):
    """
    Instruction argument types
    """
    VAR = 'var'
    CONST_VALUE = 'const'
    LABEL = 'label'


class DataType(Enum):
    """
    IPPcode23 data types
    """
    NIL = 'nil'
    INT = 'int'
    STRING = 'string'
    BOOL = 'bool'


class FrameType(Enum):
    """
    Variable frames
    """
    GF = 'gf'
    TF = 'tf'
    LF = 'lf'


class Argument(ABC):
    """
    Instruction argument
    """
    def __init__(self, arg_type: ArgumentType):
        self.arg_type = arg_type

    def get_arg_type(self) -> ArgumentType:
        """
        Get argument type
        @return: ArgumentType
        """
        return self.arg_type

    @staticmethod
    def create_argument(arg_element: etree.Element):
        """
        Create correct argument type from @p arg_element
        @param arg_element: xml element representation of the argument
        @return: Correct argument object
        """
        arg_value = arg_element.text
        if arg_value is None:
            arg_value = ''
        arg_type = arg_element.attrib.get('type')
        # Choose correct argument type to create
        match arg_type:
            case DataType.NIL.value:
                arg_obj = ConstNil()

            case DataType.BOOL.value:
                if arg_value == 'true':
                    value = True
                elif arg_value == 'false':
                    value = False
                else:
                    # TODO value error
                    pass

                arg_obj = ConstBool(value)

            case DataType.INT.value:
                try:
                    value = int(arg_value)
                except ValueError as e:
                    # TODO handle error
                    pass
                finally:
                    value = 0

                arg_obj = ConstInt(value)

            case DataType.STRING.value:
                arg_obj = ConstString(str(arg_value))

            case ArgumentType.VAR.value:
                at_pos = arg_value.find('@')
                if at_pos == -1:
                    # TODO raise value error, missing frame delimeter @
                    pass

                match arg_value[:at_pos].upper():
                    case 'GF':
                        frame = FrameType.GF
                    case 'TF':
                        frame = FrameType.TF
                    case 'LF':
                        frame = FrameType.LF
                    case default:
                        # TODO raise value error
                        frame = FrameType.GF

                arg_obj = Variable(arg_value[at_pos+1:], frame)

            case ArgumentType.LABEL.value:
                if arg_value == '':
                    # TODO raise value error
                    pass

                arg_obj = Label(str(arg_value))
            case default:
                # TODO raise incorrect type
                arg_obj = ConstNil()

        return arg_obj


class Label(Argument):
    """
    Label type
    """
    def __init__(self, label: str):
        super().__init__(ArgumentType.LABEL)
        self.label_name = label

    def __repr__(self):
        return self.arg_type.value + ':' + str(self.label_name)


class Symbol(Argument, ABC):
    """
    Symbol argument type
    May be immediate value or variable
    """
    def __init__(self, arg_type: ArgumentType, value=None, value_type: DataType = None):
        super().__init__(arg_type)
        self.value = value
        self.value_type = value_type

    def get_value(self):
        """
        Get value of argument
        @return: value held in argument
        """
        return self.value

    def get_type(self):
        """
        Get argument data type
        @return: data type of the value held in argument
        """
        return self.value_type

    def __repr__(self):
        return self.value_type.value + ':' + str(self.value)


class ConstInt(Symbol):
    """
    Integer immediate value
    """
    def __init__(self, value: int):
        super().__init__(ArgumentType.CONST_VALUE, value, DataType.INT)


class ConstBool(Symbol):
    """
    Bool immediate value
    """
    def __init__(self, value: bool):
        super().__init__(ArgumentType.CONST_VALUE, value, DataType.BOOL)


class ConstString(Symbol):
    """
    String immediate value
    """
    def __init__(self, value: str):
        super().__init__(ArgumentType.CONST_VALUE, value, DataType.STRING)


class ConstNil(Symbol):
    """
    Nil argument
    """
    def __init__(self):
        super().__init__(ArgumentType.CONST_VALUE, 'nil', DataType.NIL)


class Variable(Symbol):
    """
    Variable type
    Has information about name, frame, value and type
    """
    def __init__(self, name: str, frame: FrameType):
        super().__init__(ArgumentType.VAR)
        self.name = name
        self.frame = frame

    def is_defined(self) -> bool:
        """
        Get information, whether this variable was already initialized
        @return: bool
        """
        return self.value is None

    def set_value(self, value, value_type: DataType):
        """
        Set variable value
        @param value: value
        @param value_type: data type of value
        @return: void
        """
        self.value = value
        self.value_type = value_type

    def get_value(self):
        """
        Get the value, which is held by this variable
        @raise Undefined var error in case the variable hasn't been assigned value before
        @return: value
        """
        if self.is_defined():
            return self.value
        else:
            # TODO raise undefined var error
            pass

    def get_value_type(self) -> DataType:
        """
        Get type of value held in this variable
        @raise Undefined var error in case the variable hasn't been assigned value before
        @return: DataType
        """
        if self.is_defined():
            return self.value_type
        else:
            # TODO raise undefined var error
            pass

    def get_frame(self) -> FrameType:
        """
        Get information about the frame which holds this variable
        @return: FrameType
        """
        return self.frame

    def __repr__(self):
        return self.frame.value + ':' + self.name + ':' + str(self.value_type) + ':' + str(self.value)


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
