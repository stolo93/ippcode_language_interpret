"""!
@package ipp23
@file instruction_factory.py
@author Samuel Stolarik
@date 2023-03-24
"""

import abc

import ipp23.instruction as instr


class InstructionFactory(abc.ABC):
    @abc.abstractmethod
    def create_instruction(self, opcode: str, order: int, args: list):
        """
        Create instrution and validate args
        @param opcode
        @param order
        @param args
        @return Instruction Object
        """
        pass

    @abc.abstractmethod
    def _validate_args(self, args: list):
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


# General purpose instructions

class MoveInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.MoveInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class CreateFrameInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.CreateFrameInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class PushFrameInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.PushFrameInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class PopFrameInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.PopFrameInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class DefVarInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.DefVarInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class Int2CharInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.Int2CharInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class Stri2IntInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.Stri2IntInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class TypeInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.TypeInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


# Flow control instructions

class CallInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.CallInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class ReturnInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.ReturnInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class LabelInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.LabelInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class JumpInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.JumpInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class JumpIfEqInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.JumpIfEqInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class JumpIfNeqInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.JumpIfNeqInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class ExitInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.ExitInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


# String instructions

class ConcatInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.ConcatInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class StrLenInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.StrLenInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class GetCharInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.GetCharInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class SetCharInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.SetCharInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


# Arithmetic instructions

class AddInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.AddInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class SubInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.SubInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class MulInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.MulInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class IdivInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.IdivInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


# Relational instructions

class LtInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.LtInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class GtInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.GtInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class EqInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.EqInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


# Logic instructions

class AndInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.AndInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class OrInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.OrInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class NotInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.NotInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


# Stack instructions

class PushsInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.PushsInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class PopsInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.PopsInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


# IO instructions

class ReadInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.ReadInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class WriteInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.WriteInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class DprintInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.DprintInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass


class BreakInstructionFactory(InstructionFactory):
    def create_instruction(self, opcode: str, order: int, args: list):
        self._validate_opcode(opcode)
        self._validate_args(args)
        return instr.BreakInstruction(opcode, order, args)

    def _validate_args(self, args: list):
        pass

    def _validate_opcode(self, opcode: str):
        pass
