"""!
@package ipp23
@file interpret.py
@author Samuel Stolarik
@date 2023-03-24
"""

import xml.etree.ElementTree as Etree
import io
import sys
import typing

import ipp23.instruction_factory as isf
from .exceptions import XMLErrorIPP23, ErrorType
from .program import Program
from .argument import Argument
from .instruction import Instruction


class Interpret:
    """
    IPPcode23 intepret
    """
    def __init__(self):
        self.instructions: typing.List[Instruction] = []
        self.program_state: Program = None

    def load(self, input_xml: io.TextIOBase = sys.stdin) -> None:
        """
        Load all instructions
        @raise XMLError
        @param input_xml: list of xml lines
        @return None
        """
        try:
            xml = Etree.parse(input_xml)
        except Etree.ParseError:
            raise XMLErrorIPP23('Error: XML parsing failed', ErrorType.ERR_XML_FORMAT)

        program_root = xml.getroot()
        for instr in program_root:
            if instr.tag != 'instruction':
                raise XMLErrorIPP23(f'Error: Invalid element, {instr.tag}', ErrorType.ERR_XML_STRUCT)

            attributes = instr.attrib

            for key in attributes:
                if key not in ['opcode', 'order']:
                    raise XMLErrorIPP23(f'Error: Invalid attribute, {key}', ErrorType.ERR_XML_STRUCT)

            # Get opcode, order and correct instruction factory
            try:
                opcode = attributes['opcode']
                # Instruction indices start at 1, therefore I subtract 1 for better list indexing
                order = int(attributes['order'])
            except KeyError:
                raise XMLErrorIPP23('Error: Missing attributes in input XML', ErrorType.ERR_XML_STRUCT)
            except ValueError:
                raise XMLErrorIPP23(f"Error: Invalid instruction order attribute, {attributes['order']}", ErrorType.ERR_XML_STRUCT)

            order -= 1  # For internal indexing purposes
            factory = Interpret._get_instruction_factory(opcode)

            # Get all instruction arguments
            args_dict = {}
            args = []
            # Firstly, load arguments into dictionary in order to be able to retrieve them in order
            for arg in instr:
                args_dict[arg.tag] = arg

            was_none = False
            for i in range(1, 4):
                arg = args_dict.get('arg'+str(i))
                if was_none and arg is not None:
                    raise XMLErrorIPP23('Error: Instruction arguments are not numbered sequentially', ErrorType.ERR_XML_STRUCT)
                if arg is None:
                    was_none = True
                    continue
                args.append(Argument.create_argument(arg))

            # Insert instruction
            self.instructions.append(factory.create_instruction(opcode, order, args))

        self.instructions.sort()
        self._check_instructions()

    def initialize(self, program_input: io.TextIOBase = sys.stdin):
        self.program_state = Program(program_input)

    def execute(self) -> None:
        """
        Execute instructions
        @return: None
        """
        self.program_state.program_counter = 0
        # Create labels
        for instruction in self.instructions:
            if instruction.opcode.upper() == 'LABEL':
                # Label instruction increments program counter
                instruction.execute(self.program_state)
            else:
                self.program_state.program_counter += 1

        # Execute all instructions normally
        self.program_state.program_counter = 0
        program_length = len(self.instructions)
        while self.program_state.program_counter < program_length:
            current_instruction = self.instructions[self.program_state.program_counter]
            current_instruction.execute(self.program_state)

    @staticmethod
    def _get_instruction_factory(opcode: str):
        """
        Parse instruction opcode and return correct factory for it
        @raise ValueError
        @param opcode
        @return InstructionFactory Object
        """
        match opcode.upper():
            case 'MOVE':
                factory = isf.MoveInstructionFactory()
            case 'CREATEFRAME':
                factory = isf.CreateFrameInstructionFactory()
            case 'PUSHFRAME':
                factory = isf.PushFrameInstructionFactory()
            case 'POPFRAME':
                factory = isf.PopFrameInstructionFactory()
            case 'DEFVAR':
                factory = isf.DefVarInstructionFactory()
            case 'INT2CHAR':
                factory = isf.Int2CharInstructionFactory()
            case 'STRI2INT':
                factory = isf.Stri2IntInstructionFactory()
            case 'TYPE':
                factory = isf.TypeInstructionFactory()
            case 'CALL':
                factory = isf.CallInstructionFactory()
            case 'RETURN':
                factory = isf.ReturnInstructionFactory()
            case 'LABEL':
                factory = isf.LabelInstructionFactory()
            case 'JUMP':
                factory = isf.JumpInstructionFactory()
            case 'JUMPIFEQ':
                factory = isf.JumpIfEqInstructionFactory()
            case 'JUMPIFNEQ':
                factory = isf.JumpIfNeqInstructionFactory()
            case 'EXIT':
                factory = isf.ExitInstructionFactory()
            case 'CONCAT':
                factory = isf.ConcatInstructionFactory()
            case 'STRLEN':
                factory = isf.StrLenInstructionFactory()
            case 'GETCHAR':
                factory = isf.GetCharInstructionFactory()
            case 'SETCHAR':
                factory = isf.SetCharInstructionFactory()
            case 'ADD':
                factory = isf.AddInstructionFactory()
            case 'SUB':
                factory = isf.SubInstructionFactory()
            case 'MUL':
                factory = isf.MulInstructionFactory()
            case 'IDIV':
                factory = isf.IdivInstructionFactory()
            case 'LT':
                factory = isf.LtInstructionFactory()
            case 'GT':
                factory = isf.GtInstructionFactory()
            case 'EQ':
                factory = isf.EqInstructionFactory()
            case 'AND':
                factory = isf.AndInstructionFactory()
            case 'OR':
                factory = isf.OrInstructionFactory()
            case 'NOT':
                factory = isf.NotInstructionFactory()
            case 'PUSHS':
                factory = isf.PushsInstructionFactory()
            case 'POPS':
                factory = isf.PopsInstructionFactory()
            case 'READ':
                factory = isf.ReadInstructionFactory()
            case 'WRITE':
                factory = isf.WriteInstructionFactory()
            case 'DPRINT':
                factory = isf.DprintInstructionFactory()
            case 'BREAK':
                factory = isf.BreakInstructionFactory()
            case _:
                raise XMLErrorIPP23(f'No such instruction {opcode}', ErrorType.ERR_XML_STRUCT)
        return factory

    def _check_instructions(self) -> None:
        """
        Check if all instructions in self instructions have the correct order
        Expects that instructions are already sorted
        @raise XMLError
        @return: None
        """
        if not self.instructions:
            return
        # Check for negative order
        if self.instructions[0].order < 0:
            raise XMLErrorIPP23('Error: Instruction order does not start correctly', ErrorType.ERR_XML_STRUCT)

        # Check for duplicate order
        for i in range(1, len(self.instructions)):
            if self.instructions[i].order == self.instructions[i-1].order:
                raise XMLErrorIPP23('Error: Duplicate order', ErrorType.ERR_XML_STRUCT)
