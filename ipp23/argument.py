
"""!
@package program
@file argument.py
@author Samuel Stolarik
@date 2023-04-02
"""
import abc
import xml.etree.ElementTree as Etree

from .type_enums import DataType, ArgumentType, FrameType
from .exceptions import RuntimeErrorIPP23, ErrorType


class Argument(abc.ABC):
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
    def create_argument(arg_element: Etree.Element):
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
                    raise ValueError(f'Error: Incorrect value for type bool, {arg_value}')

                arg_obj = ConstBool(value)

            case DataType.INT.value:
                value = int(arg_value)
                arg_obj = ConstInt(value)

            case DataType.STRING.value:
                arg_obj = ConstString(str(arg_value))

            case ArgumentType.VAR.value:
                at_pos = arg_value.find('@')
                if at_pos == -1:
                    raise ValueError(f'Error: Incorrect variable {arg_value}')

                match arg_value[:at_pos].upper():
                    case 'GF':
                        frame = FrameType.GF
                    case 'TF':
                        frame = FrameType.TF
                    case 'LF':
                        frame = FrameType.LF
                    case _:
                        ValueError(f'Error: Incorrect frame type {arg_value}')
                        return

                arg_obj = Variable(arg_value[at_pos+1:], frame)

            case ArgumentType.LABEL.value:
                if arg_value == '':
                    raise ValueError(f'Error: Empty label name')

                arg_obj = Label(str(arg_value))

            case ArgumentType.TYPE.value:
                match arg_value.lower():
                    case DataType.INT.value:
                        arg_value = DataType.INT
                    case DataType.BOOL.value:
                        arg_value = DataType.BOOL
                    case DataType.STRING.value:
                        arg_value = DataType.STRING
                    case _:
                        raise ValueError(f'Error: Incorrect type name, {arg_value}')

                arg_obj = Type(arg_value)

            case _:
                raise ValueError(f'Error: Incorrect argument type error, {arg_type}')

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


class Type(Argument):
    """
    Type argument
    """
    def __init__(self, type_name: DataType):
        super().__init__(ArgumentType.TYPE)
        self.type_name = type_name

    def __repr__(self):
        return self.arg_type.value + ':' + self.type_name.value


class Symbol(Argument, abc.ABC):
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

    def is_initialized(self) -> bool:
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
        if not self.is_initialized():
            raise RuntimeErrorIPP23('Error: Variable not initialized, cannot access value', ErrorType.ERR_UNDEF_VAR)

        return self.value

    def get_value_type(self) -> DataType:
        """
        Get type of value held in this variable
        @raise Undefined var error in case the variable hasn't been assigned value before
        @return: DataType
        """
        if not self.is_initialized():
            raise RuntimeErrorIPP23('Error: Variable not initialized, cannot access type', ErrorType.ERR_UNDEF_VAR)

        return self.value_type

    def get_frame(self) -> FrameType:
        """
        Get information about the frame which holds this variable
        @return: FrameType
        """
        return self.frame

    def __repr__(self):
        return self.frame.value + ':' + self.name + ':' + str(self.value_type) + ':' + str(self.value)
