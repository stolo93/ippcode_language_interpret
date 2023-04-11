"""!
@package program
@file program.py
@author Samuel Stolarik
@date 2023-03-22
"""

import abc
import sys
import re

from .program import Program
from .argument import Argument
from .exceptions import RuntimeErrorIPP23, ErrorType, ExitProgramException
from .type_enums import DataType


class Instruction(abc.ABC):
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

    @abc.abstractmethod
    def execute(self, program_state: Program):
        pass

    def __repr__(self):
        return str(self.order) + ' ' + self.opcode + ' ' + str(self.args)

    def __lt__(self, other) -> bool:
        return self.order < other.order


# General purpose instructions

class MoveInstruction(Instruction):
    def execute(self, program_state: Program):
        symbol_type = program_state.get_symbol_type(self.args[1])
        symbol_value = program_state.get_symbol_value(self.args[1])
        program_state.set_variable(self.args[0], symbol_value, symbol_type)
        program_state.program_counter += 1


class CreateFrameInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.create_frame()
        program_state.program_counter += 1


class PushFrameInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.push_frame()
        program_state.program_counter += 1


class PopFrameInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.pop_frame()
        program_state.program_counter += 1


class DefVarInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.declare_variable(self.args[0])
        program_state.program_counter += 1


class Int2CharInstruction(Instruction):
    def execute(self, program_state: Program):
        int_value = program_state.get_symbol_value(self.args[1])

        try:
            char_value = chr(int_value)
        except (ValueError, TypeError):
            raise RuntimeErrorIPP23(f'Error: Invalid ordinal value for Int2Char instruction, {int_value}', ErrorType.ERR_STRING)

        program_state.set_variable(self.args[0], char_value, DataType.STRING)
        program_state.program_counter += 1


class Stri2IntInstruction(Instruction):
    def execute(self, program_state: Program):
        if program_state.get_symbol_type(self.args[2]) != DataType.INT:
            raise RuntimeErrorIPP23('Error: Index to string is not an integer', ErrorType.ERR_OPERAND_TYPE)
        if program_state.get_symbol_type(self.args[1]) != DataType.STRING:
            raise RuntimeErrorIPP23('Error: Invalid argument type for Stri2Int, string expected', ErrorType.ERR_OPERAND_TYPE)

        string_index = self.args[2].get_value()
        string_value = self.args[1].get_value()

        if string_index >= len(string_value) or string_index < 0:
            raise RuntimeErrorIPP23('Error: Index out of bounds', ErrorType.ERR_STRING)

        char_value = string_value[string_index]
        try:
            int_value = ord(char_value)
        except TypeError:
            raise RuntimeErrorIPP23('Error: Invalid value for conversion to ordinal', ErrorType.ERR_STRING)

        program_state.set_variable(self.args[0], int_value, DataType.INT)
        program_state.program_counter += 1


class TypeInstruction(Instruction):
    def execute(self, program_state: Program):
        try:
            symbol_type = program_state.get_symbol_type(self.args[1])
            symbol_type = symbol_type.value

        # In case of an uninitialized variable
        except RuntimeErrorIPP23 as e:
            # In case variable is defined but uninitialized
            if e.exit_code == ErrorType.ERR_VAR_NOT_INIT.value:
                symbol_type = ''
            else:
                raise e

        program_state.set_variable(self.args[0], symbol_type, DataType.STRING)
        program_state.program_counter += 1


# Flow control instructions

class CallInstruction(Instruction):
    def execute(self, program_state: Program):
        # Save incremented program counter onto call stack
        program_state.call_stack_push(program_state.program_counter + 1)
        program_state.program_counter = program_state.get_label_address(self.args[0])


class ReturnInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.program_counter = program_state.call_stack_pop()


class LabelInstruction(Instruction):
    def execute(self, program_state: Program):
        label_address = program_state.program_counter + 1
        program_state.create_label(self.args[0], label_address)
        program_state.program_counter += 1


class JumpInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.program_counter = program_state.get_label_address(self.args[0])


class JumpIfEqInstruction(Instruction):
    def execute(self, program_state: Program):
        data_type1 = program_state.get_symbol_type(self.args[1])
        data_type2 = program_state.get_symbol_type(self.args[2])

        if data_type1 == data_type2:
            pass
        elif data_type1 == DataType.NIL or data_type2 == DataType.NIL:
            pass
        else:
            raise RuntimeErrorIPP23(f'Error: Operands incorrect types for comparison: {data_type1} and {data_type2}', ErrorType.ERR_OPERAND_TYPE)

        # If values of arguments are equal
        if program_state.get_symbol_value(self.args[1]) == program_state.get_symbol_value(self.args[2]):
            program_state.program_counter = program_state.get_label_address(self.args[0])
        else:
            program_state.program_counter += 1


class JumpIfNeqInstruction(Instruction):
    def execute(self, program_state: Program):
        data_type1 = program_state.get_symbol_type(self.args[1])
        data_type2 = program_state.get_symbol_type(self.args[2])
        should_jump = False

        if data_type1 == data_type2:
            pass
        elif data_type1 == DataType.NIL or data_type2 == DataType.NIL:
            pass
        else:
            raise RuntimeErrorIPP23(f'Error: Operands incorrect types for comparison: {data_type1} and {data_type2}', ErrorType.ERR_OPERAND_TYPE)

        # If values of arguments are not equal
        if program_state.get_symbol_value(self.args[1]) != program_state.get_symbol_value(self.args[2]):
            program_state.program_counter = program_state.get_label_address(self.args[0])
        else:
            program_state.program_counter += 1


class ExitInstruction(Instruction):
    def execute(self, program_state: Program):
        argument_type = program_state.get_symbol_type(self.args[0])
        if argument_type != DataType.INT:
            raise RuntimeErrorIPP23(f'Error: Exit code expects type int, got {argument_type}', ErrorType.ERR_OPERAND_TYPE)

        exit_code = program_state.get_symbol_value(self.args[0])
        if exit_code not in range(0, 50):
            raise RuntimeErrorIPP23(f'Error: Exit code expected in interval 0 - 49, got {exit_code}', ErrorType.ERR_OPERAND_VALUE)

        # Exit program correctly
        raise ExitProgramException('Goodbye', exit_code)


# String instructions

class ConcatInstruction(Instruction):
    def execute(self, program_state: Program):
        arg1_type = program_state.get_symbol_type(self.args[1])
        arg2_type = program_state.get_symbol_type(self.args[2])
        if not (arg1_type == DataType.STRING and arg2_type == DataType.STRING):
            raise RuntimeErrorIPP23(f'Error: Invalid types {arg1_type} and {arg2_type}, expected strings', ErrorType.ERR_OPERAND_TYPE)

        arg1_value = program_state.get_symbol_value(self.args[1])
        arg2_value = program_state.get_symbol_value(self.args[2])
        result = arg1_value + arg2_value

        program_state.set_variable(self.args[0], result, DataType.STRING)
        program_state.program_counter += 1


class StrLenInstruction(Instruction):
    def execute(self, program_state: Program):
        arg1_type = program_state.get_symbol_type(self.args[1])
        if arg1_type != DataType.STRING:
            raise RuntimeErrorIPP23(f'Error: Expected argument type: string, got {arg1_type}', ErrorType.ERR_OPERAND_TYPE)

        arg1_value = program_state.get_symbol_value(self.args[1])
        program_state.set_variable(self.args[0], len(arg1_value), DataType.INT)
        program_state.program_counter += 1


class GetCharInstruction(Instruction):
    def execute(self, program_state: Program):
        arg1_type = program_state.get_symbol_type(self.args[1])
        arg2_type = program_state.get_symbol_type(self.args[2])
        if not (arg1_type == DataType.STRING and arg2_type == DataType.INT):
            raise RuntimeErrorIPP23(f'Error: Expected argument types are string and int, got {arg1_type} and {arg2_type}', ErrorType.ERR_OPERAND_TYPE)

        arg1_value = program_state.get_symbol_value(self.args[1])
        arg2_value = program_state.get_symbol_value(self.args[2])

        if arg2_value not in range(0, len(arg1_value)):
            raise RuntimeErrorIPP23(f'Error: Index out of bounds', ErrorType.ERR_STRING)

        result = arg2_value[arg1_value]
        program_state.set_variable(self.args[0], result, DataType.STRING)

        program_state.program_counter += 1


class SetCharInstruction(Instruction):
    def execute(self, program_state: Program):
        arg0_type = program_state.get_symbol_type(self.args[0])
        arg1_type = program_state.get_symbol_type(self.args[1])
        arg2_type = program_state.get_symbol_type(self.args[2])
        if not (arg0_type == DataType.STRING and arg1_type == DataType.INT and arg2_type == DataType.STRING):
            raise RuntimeErrorIPP23(f'Error: Expected argument types are string, int, string, got {arg0_type}, {arg1_type}, {arg2_type}', ErrorType.ERR_OPERAND_TYPE)

        arg0_value = program_state.get_symbol_value(self.args[0])
        arg1_value = program_state.get_symbol_value(self.args[1])
        arg2_value = program_state.get_symbol_value(self.args[2])

        if arg1_value not in range(0, len(arg0_value)):
            raise RuntimeErrorIPP23('Error: Index out of bounds', ErrorType.ERR_STRING)
        if len(arg2_value) == 0:
            raise RuntimeErrorIPP23('Error: Empty source string', ErrorType.ERR_STRING)

        # Copy string and set character at index to the first char from the third argument
        result = arg0_value[:]
        result[arg1_value] = arg2_value[0]

        program_state.set_variable(self.args[0], result, DataType.STRING)

        program_state.program_counter += 1


# Arithmetic instructions

class AddInstruction(Instruction):
    def execute(self, program_state: Program):
        arg1_type = program_state.get_symbol_type(self.args[1])
        arg2_type = program_state.get_symbol_type(self.args[2])
        if not (arg1_type == DataType.INT and arg2_type == DataType.INT):
            raise RuntimeErrorIPP23(f'Error: Expected argument types int and int, got {arg1_type} and {arg2_type}', ErrorType.ERR_OPERAND_TYPE)

        arg1_value = program_state.get_symbol_value(self.args[1])
        arg2_value = program_state.get_symbol_value(self.args[2])

        result = arg1_value + arg2_value

        program_state.set_variable(self.args[0], result, DataType.INT)
        program_state.program_counter += 1


class SubInstruction(Instruction):
    def execute(self, program_state: Program):
        arg1_type = program_state.get_symbol_type(self.args[1])
        arg2_type = program_state.get_symbol_type(self.args[2])
        if not (arg1_type == DataType.INT and arg2_type == DataType.INT):
            raise RuntimeErrorIPP23(f'Error: Expected argument types int and int, got {arg1_type} and {arg2_type}', ErrorType.ERR_OPERAND_TYPE)

        arg1_value = program_state.get_symbol_value(self.args[1])
        arg2_value = program_state.get_symbol_value(self.args[2])

        result = arg1_value - arg2_value

        program_state.set_variable(self.args[0], result, DataType.INT)
        program_state.program_counter += 1


class MulInstruction(Instruction):
    def execute(self, program_state: Program):
        arg1_type = program_state.get_symbol_type(self.args[1])
        arg2_type = program_state.get_symbol_type(self.args[2])
        if not (arg1_type == DataType.INT and arg2_type == DataType.INT):
            raise RuntimeErrorIPP23(f'Error: Expected argument types int and int, got {arg1_type} and {arg2_type}', ErrorType.ERR_OPERAND_TYPE)

        arg1_value = program_state.get_symbol_value(self.args[1])
        arg2_value = program_state.get_symbol_value(self.args[2])

        result = arg1_value * arg2_value

        program_state.set_variable(self.args[0], result, DataType.INT)
        program_state.program_counter += 1


class IdivInstruction(Instruction):
    def execute(self, program_state: Program):
        arg1_type = program_state.get_symbol_type(self.args[1])
        arg2_type = program_state.get_symbol_type(self.args[2])
        if not (arg1_type == DataType.INT and arg2_type == DataType.INT):
            raise RuntimeErrorIPP23(f'Error: Expected argument types int and int, got {arg1_type} and {arg2_type}', ErrorType.ERR_OPERAND_TYPE)

        arg1_value = program_state.get_symbol_value(self.args[1])
        arg2_value = program_state.get_symbol_value(self.args[2])

        if arg2_value == 0:
            raise RuntimeErrorIPP23('Error: Division by zero', ErrorType.ERR_OPERAND_VALUE)

        result = arg1_value // arg2_value

        program_state.set_variable(self.args[0], result, DataType.INT)
        program_state.program_counter += 1


# Relational instructions

class LtInstruction(Instruction):
    def execute(self, program_state: Program):
        arg1_type = program_state.get_symbol_type(self.args[1])
        arg2_type = program_state.get_symbol_type(self.args[2])

        if not arg1_type == arg2_type:
            raise RuntimeErrorIPP23(f'Error: Relational operator expects same type arguments, got {arg1_type} and {arg2_type}', ErrorType.ERR_OPERAND_TYPE)
        if arg1_type == DataType.NIL:
            raise RuntimeErrorIPP23(f'Error: Relational operator expects non nil arguments', ErrorType.ERR_OPERAND_TYPE)

        arg1_value = program_state.get_symbol_value(self.args[1])
        arg2_value = program_state.get_symbol_value(self.args[2])

        result = arg1_value < arg2_value

        program_state.set_variable(self.args[0], result, DataType.BOOL)

        program_state.program_counter += 1


class GtInstruction(Instruction):
    def execute(self, program_state: Program):
        arg1_type = program_state.get_symbol_type(self.args[1])
        arg2_type = program_state.get_symbol_type(self.args[2])

        if not arg1_type == arg2_type:
            raise RuntimeErrorIPP23(f'Error: Relational operator expects same type arguments, got {arg1_type} and {arg2_type}', ErrorType.ERR_OPERAND_TYPE)
        if arg1_type == DataType.NIL:
            raise RuntimeErrorIPP23(f'Error: Relational operator expects non nil arguments', ErrorType.ERR_OPERAND_TYPE)

        arg1_value = program_state.get_symbol_value(self.args[1])
        arg2_value = program_state.get_symbol_value(self.args[2])

        result = arg1_value > arg2_value

        program_state.set_variable(self.args[0], result, DataType.BOOL)

        program_state.program_counter += 1


class EqInstruction(Instruction):
    def execute(self, program_state: Program):
        arg1_type = program_state.get_symbol_type(self.args[1])
        arg2_type = program_state.get_symbol_type(self.args[2])

        if not arg1_type == arg2_type:
            raise RuntimeErrorIPP23(f'Error: Relational operator expects same type arguments, got {arg1_type} and {arg2_type}', ErrorType.ERR_OPERAND_TYPE)

        arg1_value = program_state.get_symbol_value(self.args[1])
        arg2_value = program_state.get_symbol_value(self.args[2])

        result = arg1_value == arg2_value

        program_state.set_variable(self.args[0], result, DataType.BOOL)

        program_state.program_counter += 1


# Logic instructions

class AndInstruction(Instruction):
    def execute(self, program_state: Program):
        arg1_type = program_state.get_symbol_type(self.args[1])
        arg2_type = program_state.get_symbol_type(self.args[2])

        if not (arg1_type == DataType.BOOL and arg2_type == DataType.BOOL):
            raise RuntimeErrorIPP23(f'Error: Relational operator expects argument type bool, got {arg1_type} and {arg2_type}', ErrorType.ERR_OPERAND_TYPE)

        arg1_value = program_state.get_symbol_value(self.args[1])
        arg2_value = program_state.get_symbol_value(self.args[2])

        result = arg1_value and arg2_value

        program_state.set_variable(self.args[0], result, DataType.BOOL)

        program_state.program_counter += 1


class OrInstruction(Instruction):
    def execute(self, program_state: Program):
        arg1_type = program_state.get_symbol_type(self.args[1])
        arg2_type = program_state.get_symbol_type(self.args[2])

        if not (arg1_type == DataType.BOOL and arg2_type == DataType.BOOL):
            raise RuntimeErrorIPP23(f'Error: Relational operator expects argument type bool, got {arg1_type} and {arg2_type}', ErrorType.ERR_OPERAND_TYPE)

        arg1_value = program_state.get_symbol_value(self.args[1])
        arg2_value = program_state.get_symbol_value(self.args[2])

        result = arg1_value or arg2_value

        program_state.set_variable(self.args[0], result, DataType.BOOL)

        program_state.program_counter += 1


class NotInstruction(Instruction):
    def execute(self, program_state: Program):
        arg1_type = program_state.get_symbol_type(self.args[1])

        if not arg1_type == DataType.BOOL:
            raise RuntimeErrorIPP23(f'Error: Relational operator expects argument type bool, got {arg1_type}', ErrorType.ERR_OPERAND_TYPE)

        arg1_value = program_state.get_symbol_value(self.args[1])

        result = not arg1_value

        program_state.set_variable(self.args[0], result, DataType.BOOL)

        program_state.program_counter += 1


# Stack instructions

class PushsInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.data_stack_push(self.args[0])

        program_state.program_counter += 1


class PopsInstruction(Instruction):
    def execute(self, program_state: Program):
        symbol = program_state.data_stack_pop()
        program_state.set_variable(self.args[0], symbol.get_value(), symbol.get_type())

        program_state.program_counter += 1


# IO instructions

class ReadInstruction(Instruction):
    def execute(self, program_state: Program):
        data_type_read = self.args[1].type_name
        input_read = program_state.get_line()

        match data_type_read:
            case DataType.INT:
                try:
                    num_base = self._get_number_base(input_read)
                    result = int(input_read, base=num_base)
                    result_type = DataType.INT
                except ValueError:
                    result = 'nil'
                    result_type = DataType.NIL

            case DataType.STRING:
                result = str(input_read)
                result_type = DataType.STRING

            case DataType.BOOL:
                if input_read.upper() == 'TRUE':
                    # 'true' is cast to True, case-insensitive
                    result = True
                else:
                    # Everything else is cast to False
                    result = False
                result_type = DataType.BOOL
            case _:
                raise RuntimeErrorIPP23(f'Error: Read expects types int, bool or string, got {data_type_read}', ErrorType.ERR_OPERAND_TYPE)

        program_state.set_variable(self.args[0], result, result_type)

        program_state.program_counter += 1

    @staticmethod
    def _get_number_base(number_str: str) -> int:
        """
        Get number base
        @raise Value error
        @param number_str
        @return: base
        """
        decimal_regex = r'[1-9][0-9]*(_[0-9]+)*|0'
        hexadecimal_regex = r'0[xX][0-9a-fA-F]+(_[0-9a-fA-F]+)*'
        octal_regex = r'0[oO]?[0-7]+(_[0-7]+)*'
        binary_regex = r'0[bB][01]+(_[01]+)*'

        if re.fullmatch(decimal_regex, number_str):
            return 10
        elif re.fullmatch(hexadecimal_regex, number_str):
            return 16
        elif re.fullmatch(octal_regex, number_str):
            return 8
        elif re.fullmatch(binary_regex, number_str):
            return 2
        else:
            raise ValueError(f"Invalid number format: {number_str}")


class WriteInstruction(Instruction):
    def execute(self, program_state: Program):
        arg0_type = program_state.get_symbol_type(self.args[0])
        arg0_value = program_state.get_symbol_value(self.args[0])

        if arg0_type == DataType.BOOL:
            # Different formatting for type bool
            if arg0_value:
                print('true', end='')
            else:
                print('false', end='')

        elif arg0_type == DataType.NIL:
            print('', end='')

        else:
            print(arg0_value, end='')

        program_state.program_counter += 1


class DprintInstruction(Instruction):
    def execute(self, program_state: Program):
        value = program_state.get_symbol_value(self.args[0])
        print(value, file=sys.stderr)
        program_state.program_counter += 1


class BreakInstruction(Instruction):
    def execute(self, program_state: Program):
        print(program_state, file=sys.stderr)
        program_state.program_counter += 1
