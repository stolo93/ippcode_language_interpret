"""!
@package program
@file program.py
@author Samuel Stolarik
@date 2023-03-22
"""

import abc


from .program import Program
from .argument import Argument


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
        program_state.program_counter += 1
        print(self)


class CreateFrameInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.program_counter += 1
        print(self)


class PushFrameInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.program_counter += 1
        print(self)


class PopFrameInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.program_counter += 1
        print(self)


class DefVarInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.program_counter += 1
        print(self)


class Int2CharInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.program_counter += 1
        print(self)


class Stri2IntInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.program_counter += 1
        print(self)


class TypeInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.program_counter += 1
        print(self)


# Flow control instructions

class CallInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.program_counter += 1
        print(self)


class ReturnInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.program_counter += 1
        print(self)


class LabelInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.program_counter += 1
        print(self)


class JumpInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.program_counter += 1
        print(self)


class JumpIfEqInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.program_counter += 1
        print(self)


class JumpIfNeqInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.program_counter += 1
        print(self)


class ExitInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.program_counter += 1
        print(self)


# String instructions

class ConcatInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.program_counter += 1
        print(self)


class StrLenInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.program_counter += 1
        print(self)


class GetCharInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.program_counter += 1
        print(self)


class SetCharInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.program_counter += 1
        print(self)


# Arithmetic instructions

class AddInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.program_counter += 1
        print(self)


class SubInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.program_counter += 1
        print(self)


class IdivInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.program_counter += 1
        print(self)


# Relational instructions

class LtInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.program_counter += 1
        print(self)


class GtInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.program_counter += 1
        print(self)


class EqInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.program_counter += 1
        print(self)


# Logic instructions

class AndInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.program_counter += 1
        print(self)


class OrInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.program_counter += 1
        print(self)


class NotInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.program_counter += 1
        print(self)


# Stack instructions

class PushsInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.program_counter += 1
        print(self)


class PopsInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.program_counter += 1
        print(self)


# IO instructions

class ReadInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.program_counter += 1
        print(self)


class WriteInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.program_counter += 1
        print(self)


class DprintInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.program_counter += 1
        print(self)


class BreakInstruction(Instruction):
    def execute(self, program_state: Program):
        program_state.program_counter += 1
        print(self)
