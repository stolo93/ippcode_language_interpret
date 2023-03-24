"""!
@package ipp23
@file instruction_factory.py
@author Samuel Stolarik
@date 2023-03-24
"""

from ipp23.instruction import *
from abc import ABC, abstractmethod
import typing


class InstructionFactory(ABC):
    @abstractmethod
    def create_instruction(self, opcode: str, order: int, args: list):
        """
        Create instrution and validate args
        @param opcode
        @param order
        @param args
        @return Instruction Object
        """
        pass

    @abstractmethod
    def _validate_args(self, args: list):
        """
        Perform static validation of arguments given to the instruction
        @param args
        @return bool
        """
        pass

    @abstractmethod
    def _validate_opcode(self, opcode: str):
        """
        Validate opcode given to the instruction
        @param opcode
        @return bool
        """
        pass


# General purpose instructions

class MoveInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return MoveInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class CreteFrameInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return CreteFrameInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class PushFrameInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return PushFrameInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class PopFrameInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return PopsInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class DefVarInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return DefVarInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class Int2CharInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return Int2CharInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class Stri2IntInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return Stri2IntInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class TypeInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return TypeInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


# Flow control instructions

class CallInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return CallInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class ReturnInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return ReturnInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class LabelInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return LabelInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class JumpInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return JumpInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class JumpIfEqInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return JumpIfEqInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class JumpIfNeqInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return JumpIfNeqInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class ExitInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return ExitInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


# String instructions

class ConcatInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return ConcatInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class StrLenInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return StrLenInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class GetCharInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return GetCharInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class SetCharInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return SetCharInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


# Arithmetic instructions

class AddInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return AddInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class SubInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return SubInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class IdivInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return IdivInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


# Relational instructions

class LtInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return LtInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class GtInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return GtInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class EqInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return EqInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


# Logic instructions

class AndInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return AndInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class OrInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return OrInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class NotInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return NotInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


# Stack instructions

class PushsInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return PushsInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class PopsInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return PopsInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


# IO instructions

class ReadInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return ReadInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class WriteInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return WriteInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class DprintInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return DprintInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class BreakInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return DprintInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass