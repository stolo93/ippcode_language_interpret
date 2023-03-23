"""!
@package program
@file program.py
@author Samuel Stolarik
@date 2023-03-22
"""
import typing
from abc import ABC, abstractmethod
import xml.etree.ElementTree


class Instruction(ABC):
    """
    @brief Interface for instructions
    """
    def __init__(self, opcode: str, order: int, args: list):
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
