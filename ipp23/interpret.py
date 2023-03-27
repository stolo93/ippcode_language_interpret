"""!
@package ipp23
@file interpret.py
@author Samuel Stolarik
@date 2023-03-24
"""

import typing
import xml.etree.ElementTree as etree

from ipp23.instruction_factory import *
from ipp23.instruction import *


class Interpret:
    """
    IPPcode23 intepret
    """
    def __init__(self):
        self.instructions = []

    def load(self, input_xml: list) -> None:
        """
        Load all instructions
        @param input_xml: list of xml lines
        @return None
        """
        program_root = etree.fromstringlist(input_xml)
        for instr in program_root:
            attributes = instr.attrib

            # Get opcode, order and correct instruction factory
            try:
                opcode = attributes['opcode']
                order = int(attributes['order'])
            except KeyError as e:
                print(f'Error: Missing attribute opcode or order in a instruction. {e}')
                raise e

            try:
                factory = Interpret._get_instruction_factory(opcode)
            except ValueError as e:
                print(f'Error: Invalid opcode: {opcode}. {e}')
                raise e

            # Get all instruction arguments
            args_dict = {}
            args = []
            # Firstly, load arguments into dictionary in order to be able to retrieve them in order
            for arg in instr:
                args_dict[arg.tag] = arg

            for i in range(1, 4):
                arg = args_dict.get('arg'+str(i))
                if arg is None:
                    break
                args.append(Argument.create_argument(arg))
            # Insert instruction
            self.instructions.append(factory.create_instruction(opcode, order, args))
        self.instructions.sort()

    def execute(self):
        """
        Execute all instructions
        @return: void
        """
        for instruction in self.instructions:
            print(instruction)

    @staticmethod
    def _get_instruction_factory(opcode: str):
        """
        Parse instruction opcode and return correct factory for it
        @param opcode
        @return InstructionFactory Object
        """
        match opcode.upper():
            case 'MOVE':
                factory = MoveInstructionFactory()
            case 'CREATEFRAME':
                factory = CreteFrameInstructionFactory()
            case 'PUSHFRAME':
                factory = PushFrameInstructionFactory()
            case 'POPFRAME':
                factory = PopFrameInstructionFactory()
            case 'DEFVAR':
                factory = DefVarInstructionFactory()
            case 'INT2CHAR':
                factory = Int2CharInstructionFactory()
            case 'STRI2INT':
                factory = Stri2IntInstructionFactory()
            case 'TYPE':
                factory = TypeInstructionFactory()
            case 'CALL':
                factory = CallInstructionFactory()
            case 'RETURN':
                factory = ReturnInstructionFactory()
            case 'LABEL':
                factory = LabelInstructionFactory()
            case 'JUMP':
                factory = JumpInstructionFactory()
            case 'JUMPIFEQ':
                factory = JumpIfEqInstructionFactory()
            case 'JUMPIFNEQ':
                factory = JumpIfNeqInstructionFactory()
            case 'EXIT':
                factory = ExitInstructionFactory()
            case 'CONCAT':
                factory = ConcatInstructionFactory()
            case 'STRLEN':
                factory = StrLenInstructionFactory()
            case 'GETCHAR':
                factory = GetCharInstructionFactory()
            case 'SETCHAR':
                factory = SetCharInstructionFactory()
            case 'ADD':
                factory = AddInstructionFactory()
            case 'SUB':
                factory = SubInstructionFactory()
            case 'IDIV':
                factory = IdivInstructionFactory()
            case 'LT':
                factory = LtInstructionFactory()
            case 'GT':
                factory = GtInstructionFactory()
            case 'EQ':
                factory = EqInstructionFactory()
            case 'AND':
                factory = AndInstructionFactory()
            case 'OR':
                factory = OrInstructionFactory()
            case 'NOT':
                factory = NotInstructionFactory()
            case 'PUSHS':
                factory = PushsInstructionFactory()
            case 'POPS':
                factory = PopsInstructionFactory()
            case 'READ':
                factory = ReadInstructionFactory()
            case 'WRITE':
                factory = WriteInstructionFactory()
            case 'DPRINT':
                factory = DprintInstructionFactory()
            case 'BREAK':
                factory = BreakInstructionFactory()
            case default:
                raise ValueError(f'No such instruction {opcode}')
        return factory
