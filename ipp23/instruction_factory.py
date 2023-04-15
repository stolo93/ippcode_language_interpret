"""!
@package ipp23
@file instruction_factory.py
@author Samuel Stolarik
@date 2023-03-24
"""

import abc

import ipp23.instruction as instr
from .argument import Argument
from .exceptions import GenericErrorIPP23, ErrorType
from .type_enums import ArgumentType


class InstructionFactory(abc.ABC):
    @abc.abstractmethod
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        """
        Create instrution and validate args
        @param opcode
        @param order
        @param args
        @return Instruction Object
        """
        pass

    @abc.abstractmethod
    def _validate_args(self, args: list[Argument]):
        """
        Perform static validation of arguments given to the instruction
        @param args
        @return bool
        """
        pass

    @abc.abstractmethod
    def _validate_opcode(self, opcode: str):
        """
        Validate opcode given to the instruction
        @param opcode
        @return bool
        """
        pass

    @staticmethod
    def _is_var(arg: Argument):
        """
        Is argument a variable
        @param arg:
        @return:
        """
        return arg.get_arg_type() == ArgumentType.VAR

    @staticmethod
    def _is_constant(arg: Argument):
        """
        Is argument a constant value
        @param arg:
        @return:
        """
        return arg.get_arg_type() == ArgumentType.CONST_VALUE

    @staticmethod
    def _is_label(arg: Argument):
        """
        Is argument a label
        @param arg:
        @return:
        """
        return arg.get_arg_type() == ArgumentType.LABEL

    @staticmethod
    def _is_symbol(arg: Argument):
        """
        Is argument a symbol
        @param arg:
        @return:
        """
        return InstructionFactory._is_var(arg) or InstructionFactory._is_constant(arg)

    @staticmethod
    def _is_type(arg: Argument):
        """
        Is argument a type
        @param arg:
        @return:
        """
        return arg.get_arg_type() == ArgumentType.TYPE


# General purpose instructions

class MoveInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.MoveInstruction(opcode, order, args)

    def _validate_args(self, args: list[Argument]):
        if len(args) != 2:
            raise GenericErrorIPP23('Error: Invalid number of arguments', ErrorType.ERR_SYNTAX)
        if not (InstructionFactory._is_var(args[0]) and InstructionFactory._is_symbol(args[1])):
            raise GenericErrorIPP23('Error: Invalid syntax, wrong argument types in input file', ErrorType.ERR_SYNTAX)

    def _validate_opcode(self, opcode: str):
        if opcode.upper() != 'MOVE':
            raise GenericErrorIPP23(f'Error: Invalid invalid opcode: {opcode}', ErrorType.ERR_OPCODE)


class CreateFrameInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.CreateFrameInstruction(opcode, order, args)

    def _validate_args(self, args: list[Argument]):
        if len(args) != 0:
            raise GenericErrorIPP23('Error: Invalid number of arguments', ErrorType.ERR_SYNTAX)

    def _validate_opcode(self, opcode: str):
        if opcode.upper() != 'CREATEFRAME':
            raise GenericErrorIPP23(f'Error: Invalid invalid opcode: {opcode}', ErrorType.ERR_OPCODE)


class PushFrameInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.PushFrameInstruction(opcode, order, args)

    def _validate_args(self, args: list[Argument]):
        if len(args) != 0:
            raise GenericErrorIPP23('Error: Invalid number of arguments', ErrorType.ERR_SYNTAX)

    def _validate_opcode(self, opcode: str):
        if opcode.upper() != 'PUSHFRAME':
            raise GenericErrorIPP23(f'Error: Invalid invalid opcode: {opcode}', ErrorType.ERR_OPCODE)


class PopFrameInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.PopFrameInstruction(opcode, order, args)

    def _validate_args(self, args: list[Argument]):
        if len(args) != 0:
            raise GenericErrorIPP23('Error: Invalid number of arguments', ErrorType.ERR_SYNTAX)

    def _validate_opcode(self, opcode: str):
        if opcode.upper() != 'POPFRAME':
            raise GenericErrorIPP23(f'Error: Invalid invalid opcode: {opcode}', ErrorType.ERR_OPCODE)


class DefVarInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.DefVarInstruction(opcode, order, args)

    def _validate_args(self, args: list[Argument]):
        if len(args) != 1:
            raise GenericErrorIPP23('Error: Invalid number of arguments', ErrorType.ERR_SYNTAX)
        if not InstructionFactory._is_var(args[0]):
            raise GenericErrorIPP23('Error: Invalid syntax, wrong argument types in input file', ErrorType.ERR_SYNTAX)

    def _validate_opcode(self, opcode: str):
        if opcode.upper() != 'DEFVAR':
            raise GenericErrorIPP23(f'Error: Invalid invalid opcode: {opcode}', ErrorType.ERR_OPCODE)


class Int2CharInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.Int2CharInstruction(opcode, order, args)

    def _validate_args(self, args: list[Argument]):
        if len(args) != 2:
            raise GenericErrorIPP23('Error: Invalid number of arguments', ErrorType.ERR_SYNTAX)
        if not (InstructionFactory._is_var(args[0]) and InstructionFactory._is_symbol(args[1])):
            raise GenericErrorIPP23('Error: Invalid syntax, wrong argument types in input file', ErrorType.ERR_SYNTAX)

    def _validate_opcode(self, opcode: str):
        if opcode.upper() != 'INT2CHAR':
            raise GenericErrorIPP23(f'Error: Invalid invalid opcode: {opcode}', ErrorType.ERR_OPCODE)


class Stri2IntInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.Stri2IntInstruction(opcode, order, args)

    def _validate_args(self, args: list[Argument]):
        if len(args) != 3:
            raise GenericErrorIPP23('Error: Invalid number of arguments', ErrorType.ERR_SYNTAX)
        if not (InstructionFactory._is_var(args[0]) and InstructionFactory._is_symbol(args[1]) and InstructionFactory._is_symbol(args[2])):
            raise GenericErrorIPP23('Error: Invalid syntax, wrong argument types in input file', ErrorType.ERR_SYNTAX)

    def _validate_opcode(self, opcode: str):
        if opcode.upper() != 'STRI2INT':
            raise GenericErrorIPP23(f'Error: Invalid invalid opcode: {opcode}', ErrorType.ERR_OPCODE)


class TypeInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.TypeInstruction(opcode, order, args)

    def _validate_args(self, args: list[Argument]):
        if len(args) != 2:
            raise GenericErrorIPP23('Error: Invalid number of arguments', ErrorType.ERR_SYNTAX)
        if not (InstructionFactory._is_var(args[0]) and InstructionFactory._is_symbol(args[1])):
            raise GenericErrorIPP23('Error: Invalid syntax, wrong argument types in input file', ErrorType.ERR_SYNTAX)

    def _validate_opcode(self, opcode: str):
        if opcode.upper() != 'TYPE':
            raise GenericErrorIPP23(f'Error: Invalid invalid opcode: {opcode}', ErrorType.ERR_OPCODE)


# Flow control instructions

class CallInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.CallInstruction(opcode, order, args)

    def _validate_args(self, args: list[Argument]):
        if len(args) != 1:
            raise GenericErrorIPP23('Error: Invalid number of arguments', ErrorType.ERR_SYNTAX)
        if not InstructionFactory._is_label(args[0]):
            raise GenericErrorIPP23('Error: Invalid syntax, wrong argument types in input file', ErrorType.ERR_SYNTAX)

    def _validate_opcode(self, opcode: str):
        if opcode.upper() != 'CALL':
            raise GenericErrorIPP23(f'Error: Invalid invalid opcode: {opcode}', ErrorType.ERR_OPCODE)


class ReturnInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.ReturnInstruction(opcode, order, args)

    def _validate_args(self, args: list[Argument]):
        if len(args) != 0:
            raise GenericErrorIPP23('Error: Invalid number of arguments', ErrorType.ERR_SYNTAX)

    def _validate_opcode(self, opcode: str):
        if opcode.upper() != 'RETURN':
            raise GenericErrorIPP23(f'Error: Invalid invalid opcode: {opcode}', ErrorType.ERR_OPCODE)


class LabelInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.LabelInstruction(opcode, order, args)

    def _validate_args(self, args: list[Argument]):
        if len(args) != 1:
            raise GenericErrorIPP23('Error: Invalid number of arguments', ErrorType.ERR_SYNTAX)
        if not InstructionFactory._is_label(args[0]):
            raise GenericErrorIPP23('Error: Invalid syntax, wrong argument types in input file', ErrorType.ERR_SYNTAX)

    def _validate_opcode(self, opcode: str):
        if opcode.upper() != 'LABEL':
            raise GenericErrorIPP23(f'Error: Invalid invalid opcode: {opcode}', ErrorType.ERR_OPCODE)


class JumpInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.JumpInstruction(opcode, order, args)

    def _validate_args(self, args: list[Argument]):
        if len(args) != 1:
            raise GenericErrorIPP23('Error: Invalid number of arguments', ErrorType.ERR_SYNTAX)
        if not InstructionFactory._is_label(args[0]):
            raise GenericErrorIPP23('Error: Invalid syntax, wrong argument types in input file', ErrorType.ERR_SYNTAX)

    def _validate_opcode(self, opcode: str):
        if opcode.upper() != 'JUMP':
            raise GenericErrorIPP23(f'Error: Invalid invalid opcode: {opcode}', ErrorType.ERR_OPCODE)


class JumpIfEqInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.JumpIfEqInstruction(opcode, order, args)

    def _validate_args(self, args: list[Argument]):
        if len(args) != 3:
            raise GenericErrorIPP23('Error: Invalid number of arguments', ErrorType.ERR_SYNTAX)
        if not (InstructionFactory._is_label(args[0]) and InstructionFactory._is_symbol(args[1]) and InstructionFactory._is_symbol(args[2])):
            raise GenericErrorIPP23('Error: Invalid syntax, wrong argument types in input file', ErrorType.ERR_SYNTAX)

    def _validate_opcode(self, opcode: str):
        if opcode.upper() != 'JUMPIFEQ':
            raise GenericErrorIPP23(f'Error: Invalid invalid opcode: {opcode}', ErrorType.ERR_OPCODE)


class JumpIfNeqInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.JumpIfNeqInstruction(opcode, order, args)

    def _validate_args(self, args: list[Argument]):
        if len(args) != 3:
            raise GenericErrorIPP23('Error: Invalid number of arguments', ErrorType.ERR_SYNTAX)
        if not (InstructionFactory._is_label(args[0]) and InstructionFactory._is_symbol(args[1]) and InstructionFactory._is_symbol(args[2])):
            raise GenericErrorIPP23('Error: Invalid syntax, wrong argument types in input file', ErrorType.ERR_SYNTAX)

    def _validate_opcode(self, opcode: str):
        if opcode.upper() != 'JUMPIFNEQ':
            raise GenericErrorIPP23(f'Error: Invalid invalid opcode: {opcode}', ErrorType.ERR_OPCODE)


class ExitInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.ExitInstruction(opcode, order, args)

    def _validate_args(self, args: list[Argument]):
        if len(args) != 1:
            raise GenericErrorIPP23('Error: Invalid number of arguments', ErrorType.ERR_SYNTAX)
        if not InstructionFactory._is_symbol(args[0]):
            raise GenericErrorIPP23('Error: Invalid syntax, wrong argument types in input file', ErrorType.ERR_SYNTAX)

    def _validate_opcode(self, opcode: str):
        if opcode.upper() != 'EXIT':
            raise GenericErrorIPP23(f'Error: Invalid invalid opcode: {opcode}', ErrorType.ERR_OPCODE)


# String instructions

class ConcatInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.ConcatInstruction(opcode, order, args)

    def _validate_args(self, args: list[Argument]):
        if len(args) != 3:
            raise GenericErrorIPP23('Error: Invalid number of arguments', ErrorType.ERR_SYNTAX)
        if not (InstructionFactory._is_var(args[0]) and InstructionFactory._is_symbol(args[1]) and InstructionFactory._is_symbol(args[2])):
            raise GenericErrorIPP23('Error: Invalid syntax, wrong argument types in input file', ErrorType.ERR_SYNTAX)

    def _validate_opcode(self, opcode: str):
        if opcode.upper() != 'CONCAT':
            raise GenericErrorIPP23(f'Error: Invalid invalid opcode: {opcode}', ErrorType.ERR_OPCODE)


class StrLenInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.StrLenInstruction(opcode, order, args)

    def _validate_args(self, args: list[Argument]):
        if len(args) != 2:
            raise GenericErrorIPP23('Error: Invalid number of arguments', ErrorType.ERR_SYNTAX)
        if not (InstructionFactory._is_var(args[0]) and InstructionFactory._is_symbol(args[1])):
            raise GenericErrorIPP23('Error: Invalid syntax, wrong argument types in input file', ErrorType.ERR_SYNTAX)

    def _validate_opcode(self, opcode: str):
        if opcode.upper() != 'STRLEN':
            raise GenericErrorIPP23(f'Error: Invalid invalid opcode: {opcode}', ErrorType.ERR_OPCODE)


class GetCharInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.GetCharInstruction(opcode, order, args)

    def _validate_args(self, args: list[Argument]):
        if len(args) != 3:
            raise GenericErrorIPP23('Error: Invalid number of arguments', ErrorType.ERR_SYNTAX)
        if not (InstructionFactory._is_var(args[0]) and InstructionFactory._is_symbol(args[1]) and InstructionFactory._is_symbol(args[2])):
            raise GenericErrorIPP23('Error: Invalid syntax, wrong argument types in input file', ErrorType.ERR_SYNTAX)

    def _validate_opcode(self, opcode: str):
        if opcode.upper() != 'GETCHAR':
            raise GenericErrorIPP23(f'Error: Invalid invalid opcode: {opcode}', ErrorType.ERR_OPCODE)


class SetCharInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.SetCharInstruction(opcode, order, args)

    def _validate_args(self, args: list[Argument]):
        if len(args) != 3:
            raise GenericErrorIPP23('Error: Invalid number of arguments', ErrorType.ERR_SYNTAX)
        if not (InstructionFactory._is_var(args[0]) and InstructionFactory._is_symbol(args[1]) and InstructionFactory._is_symbol(args[2])):
            raise GenericErrorIPP23('Error: Invalid syntax, wrong argument types in input file', ErrorType.ERR_SYNTAX)

    def _validate_opcode(self, opcode: str):
        if opcode.upper() != 'SETCHAR':
            raise GenericErrorIPP23(f'Error: Invalid invalid opcode: {opcode}', ErrorType.ERR_OPCODE)


# Arithmetic instructions

class AddInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.AddInstruction(opcode, order, args)

    def _validate_args(self, args: list[Argument]):
        if len(args) != 3:
            raise GenericErrorIPP23('Error: Invalid number of arguments', ErrorType.ERR_SYNTAX)
        if not (InstructionFactory._is_var(args[0]) and InstructionFactory._is_symbol(args[1]) and InstructionFactory._is_symbol(args[2])):
            raise GenericErrorIPP23('Error: Invalid syntax, wrong argument types in input file', ErrorType.ERR_SYNTAX)

    def _validate_opcode(self, opcode: str):
        if opcode.upper() != 'ADD':
            raise GenericErrorIPP23(f'Error: Invalid invalid opcode: {opcode}', ErrorType.ERR_OPCODE)


class SubInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.SubInstruction(opcode, order, args)

    def _validate_args(self, args: list[Argument]):
        if len(args) != 3:
            raise GenericErrorIPP23('Error: Invalid number of arguments', ErrorType.ERR_SYNTAX)
        if not (InstructionFactory._is_var(args[0]) and InstructionFactory._is_symbol(args[1]) and InstructionFactory._is_symbol(args[2])):
            raise GenericErrorIPP23('Error: Invalid syntax, wrong argument types in input file', ErrorType.ERR_SYNTAX)

    def _validate_opcode(self, opcode: str):
        if opcode.upper() != 'SUB':
            raise GenericErrorIPP23(f'Error: Invalid invalid opcode: {opcode}', ErrorType.ERR_OPCODE)


class MulInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.MulInstruction(opcode, order, args)

    def _validate_args(self, args: list[Argument]):
        if len(args) != 3:
            raise GenericErrorIPP23('Error: Invalid number of arguments', ErrorType.ERR_SYNTAX)
        if not (InstructionFactory._is_var(args[0]) and InstructionFactory._is_symbol(args[1]) and InstructionFactory._is_symbol(args[2])):
            raise GenericErrorIPP23('Error: Invalid syntax, wrong argument types in input file', ErrorType.ERR_SYNTAX)

    def _validate_opcode(self, opcode: str):
        if opcode.upper() != 'MUL':
            raise GenericErrorIPP23(f'Error: Invalid invalid opcode: {opcode}', ErrorType.ERR_OPCODE)


class IdivInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.IdivInstruction(opcode, order, args)

    def _validate_args(self, args: list[Argument]):
        if len(args) != 3:
            raise GenericErrorIPP23('Error: Invalid number of arguments', ErrorType.ERR_SYNTAX)
        if not (InstructionFactory._is_var(args[0]) and InstructionFactory._is_symbol(args[1]) and InstructionFactory._is_symbol(args[2])):
            raise GenericErrorIPP23('Error: Invalid syntax, wrong argument types in input file', ErrorType.ERR_SYNTAX)

    def _validate_opcode(self, opcode: str):
        if opcode.upper() != 'IDIV':
            raise GenericErrorIPP23(f'Error: Invalid invalid opcode: {opcode}', ErrorType.ERR_OPCODE)


# Relational instructions

class LtInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.LtInstruction(opcode, order, args)

    def _validate_args(self, args: list[Argument]):
        if len(args) != 3:
            raise GenericErrorIPP23('Error: Invalid number of arguments', ErrorType.ERR_SYNTAX)
        if not (InstructionFactory._is_var(args[0]) and InstructionFactory._is_symbol(args[1]) and InstructionFactory._is_symbol(args[2])):
            raise GenericErrorIPP23('Error: Invalid syntax, wrong argument types in input file', ErrorType.ERR_SYNTAX)

    def _validate_opcode(self, opcode: str):
        if opcode.upper() != 'LT':
            raise GenericErrorIPP23(f'Error: Invalid invalid opcode: {opcode}', ErrorType.ERR_OPCODE)


class GtInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.GtInstruction(opcode, order, args)

    def _validate_args(self, args: list[Argument]):
        if len(args) != 3:
            raise GenericErrorIPP23('Error: Invalid number of arguments', ErrorType.ERR_SYNTAX)
        if not (InstructionFactory._is_var(args[0]) and InstructionFactory._is_symbol(args[1]) and InstructionFactory._is_symbol(args[2])):
            raise GenericErrorIPP23('Error: Invalid syntax, wrong argument types in input file', ErrorType.ERR_SYNTAX)

    def _validate_opcode(self, opcode: str):
        if opcode.upper() != 'GT':
            raise GenericErrorIPP23(f'Error: Invalid invalid opcode: {opcode}', ErrorType.ERR_OPCODE)


class EqInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.EqInstruction(opcode, order, args)

    def _validate_args(self, args: list[Argument]):
        if len(args) != 3:
            raise GenericErrorIPP23('Error: Invalid number of arguments', ErrorType.ERR_SYNTAX)
        if not (InstructionFactory._is_var(args[0]) and InstructionFactory._is_symbol(args[1]) and InstructionFactory._is_symbol(args[2])):
            raise GenericErrorIPP23('Error: Invalid syntax, wrong argument types in input file', ErrorType.ERR_SYNTAX)

    def _validate_opcode(self, opcode: str):
        if opcode.upper() != 'EQ':
            raise GenericErrorIPP23(f'Error: Invalid invalid opcode: {opcode}', ErrorType.ERR_OPCODE)


# Logic instructions

class AndInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.AndInstruction(opcode, order, args)

    def _validate_args(self, args: list[Argument]):
        if len(args) != 3:
            raise GenericErrorIPP23('Error: Invalid number of arguments', ErrorType.ERR_SYNTAX)
        if not (InstructionFactory._is_var(args[0]) and InstructionFactory._is_symbol(args[1]) and InstructionFactory._is_symbol(args[2])):
            raise GenericErrorIPP23('Error: Invalid syntax, wrong argument types in input file', ErrorType.ERR_SYNTAX)

    def _validate_opcode(self, opcode: str):
        if opcode.upper() != 'AND':
            raise GenericErrorIPP23(f'Error: Invalid invalid opcode: {opcode}', ErrorType.ERR_OPCODE)


class OrInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.OrInstruction(opcode, order, args)

    def _validate_args(self, args: list[Argument]):
        if len(args) != 3:
            raise GenericErrorIPP23('Error: Invalid number of arguments', ErrorType.ERR_SYNTAX)
        if not (InstructionFactory._is_var(args[0]) and InstructionFactory._is_symbol(args[1]) and InstructionFactory._is_symbol(args[2])):
            raise GenericErrorIPP23('Error: Invalid syntax, wrong argument types in input file', ErrorType.ERR_SYNTAX)

    def _validate_opcode(self, opcode: str):
        if opcode.upper() != 'OR':
            raise GenericErrorIPP23(f'Error: Invalid invalid opcode: {opcode}', ErrorType.ERR_OPCODE)


class NotInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.NotInstruction(opcode, order, args)

    def _validate_args(self, args: list[Argument]):
        if len(args) != 2:
            raise GenericErrorIPP23('Error: Invalid number of arguments', ErrorType.ERR_SYNTAX)
        if not (InstructionFactory._is_var(args[0]) and InstructionFactory._is_symbol(args[1])):
            raise GenericErrorIPP23('Error: Invalid syntax, wrong argument types in input file', ErrorType.ERR_SYNTAX)

    def _validate_opcode(self, opcode: str):
        if opcode.upper() != 'NOT':
            raise GenericErrorIPP23(f'Error: Invalid invalid opcode: {opcode}', ErrorType.ERR_OPCODE)


# Stack instructions

class PushsInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.PushsInstruction(opcode, order, args)

    def _validate_args(self, args: list[Argument]):
        if len(args) != 1:
            raise GenericErrorIPP23('Error: Invalid number of arguments', ErrorType.ERR_SYNTAX)
        if not InstructionFactory._is_symbol(args[0]):
            raise GenericErrorIPP23('Error: Invalid syntax, wrong argument types in input file', ErrorType.ERR_SYNTAX)

    def _validate_opcode(self, opcode: str):
        if opcode.upper() != 'PUSHS':
            raise GenericErrorIPP23(f'Error: Invalid invalid opcode: {opcode}', ErrorType.ERR_OPCODE)


class PopsInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.PopsInstruction(opcode, order, args)

    def _validate_args(self, args: list[Argument]):
        if len(args) != 1:
            raise GenericErrorIPP23('Error: Invalid number of arguments', ErrorType.ERR_SYNTAX)
        if not InstructionFactory._is_var(args[0]):
            raise GenericErrorIPP23('Error: Invalid syntax, wrong argument types in input file', ErrorType.ERR_SYNTAX)

    def _validate_opcode(self, opcode: str):
        if opcode.upper() != 'POPS':
            raise GenericErrorIPP23(f'Error: Invalid invalid opcode: {opcode}', ErrorType.ERR_OPCODE)


# IO instructions

class ReadInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.ReadInstruction(opcode, order, args)

    def _validate_args(self, args: list[Argument]):
        if len(args) != 2:
            raise GenericErrorIPP23('Error: Invalid number of arguments', ErrorType.ERR_SYNTAX)
        if not (InstructionFactory._is_var(args[0]) and InstructionFactory._is_type(args[1])):
            raise GenericErrorIPP23('Error: Invalid syntax, wrong argument types in input file', ErrorType.ERR_SYNTAX)

    def _validate_opcode(self, opcode: str):
        if opcode.upper() != 'READ':
            raise GenericErrorIPP23(f'Error: Invalid invalid opcode: {opcode}', ErrorType.ERR_OPCODE)


class WriteInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.WriteInstruction(opcode, order, args)

    def _validate_args(self, args: list[Argument]):
        if len(args) != 1:
            raise GenericErrorIPP23('Error: Invalid number of arguments', ErrorType.ERR_SYNTAX)
        if not InstructionFactory._is_symbol(args[0]):
            raise GenericErrorIPP23('Error: Invalid syntax, wrong argument types in input file', ErrorType.ERR_SYNTAX)

    def _validate_opcode(self, opcode: str):
        if opcode.upper() != 'WRITE':
            raise GenericErrorIPP23(f'Error: Invalid invalid opcode: {opcode}', ErrorType.ERR_OPCODE)


class DprintInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.DprintInstruction(opcode, order, args)

    def _validate_args(self, args: list[Argument]):
        if len(args) != 1:
            raise GenericErrorIPP23('Error: Invalid number of arguments', ErrorType.ERR_SYNTAX)
        if not InstructionFactory._is_symbol(args[0]):
            raise GenericErrorIPP23('Error: Invalid syntax, wrong argument types in input file', ErrorType.ERR_SYNTAX)

    def _validate_opcode(self, opcode: str):
        if opcode.upper() != 'DPRINT':
            raise GenericErrorIPP23(f'Error: Invalid invalid opcode: {opcode}', ErrorType.ERR_OPCODE)


class BreakInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list[Argument]):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.BreakInstruction(opcode, order, args)

    def _validate_args(self, args: list[Argument]):
        if len(args) != 0:
            raise GenericErrorIPP23('Error: Invalid number of arguments', ErrorType.ERR_SYNTAX)

    def _validate_opcode(self, opcode: str):
        if opcode.upper() != 'BREAK':
            raise GenericErrorIPP23(f'Error: Invalid invalid opcode: {opcode}', ErrorType.ERR_OPCODE)
