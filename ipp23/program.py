"""!
@package ipp23
@file program.py
@author Samuel Stolarik
@date 2023-03-27
"""
import io
import sys
import copy

from .exceptions import RuntimeErrorIPP23, SemanticErrorIPP23, GenericErrorIPP23, ErrorType
from .frame import Frame
from .type_enums import DataType, FrameType, ArgumentType
from .argument import Symbol, Label, Variable


class Program:
    """
    Class storing all data about currently interpreted program
    """
    def __init__(self, file_in: io.TextIOBase = sys.stdin):
        # Program counter
        self._program_counter = 0
        # Input for program
        self._file_in = file_in
        # Labels
        self._labels = {}
        # Global frame (initialized since the beginning)
        self._global_frame = Frame()
        # Temporary frame (has to be created with)
        self._temporary_frame = Frame()
        self._temporary_frame_valid = False
        # Stack of local frame
        self._local_frames: list[Frame] = []
        # Data stack (stack of symbols)
        self._data_stack: list[Symbol] = []
        # Call stack
        self._call_stack: list[int] = []

    @property
    def program_counter(self) -> int:
        """
        Get current value of program counter
        @return: Current program value
        """
        return self._program_counter

    @program_counter.setter
    def program_counter(self, new_pc: int) -> None:
        """
        Set program counter to @p new_pc
        @raise SemanticError
        @param new_pc: New value
        @return: None
        """
        if new_pc < 0:
            raise SemanticErrorIPP23(f'Error: Invalid program counter value {new_pc}', ErrorType.ERR_SEMANTICS)

        self._program_counter = new_pc

    def get_line(self) -> str:
        """
        Get one line from input to the interpreted program, not containing terminating new line
        Acts as if input() was used
        @return: One line from input
        """
        line = self._file_in.readline()
        if line == '':
            return line

        elif line[-1] == '\n':
            line = line[:-1]

        return line

    def create_label(self, label: Label, address: int) -> None:
        """
        Create label at address
        @raise SemanticError
        @param label
        @param address
        @return: None
        """
        stored_address = self._labels.get(label.label_name)
        if stored_address is None:
            # Label does not exist, create it
            self._labels[label.label_name] = address
        elif stored_address == address:
            # Stored address is the same as new address
            return
        else:
            # Trying to add same label with different address
            raise SemanticErrorIPP23(f'Error: Label {label.label_name} already used', ErrorType.ERR_SEMANTICS)

    def get_label_address(self, label: Label) -> int:
        """
        Return address at which @p label is located
        @raise SemanticError
        @param label: Label
        @return: Address
        """
        address = self._labels.get(label.label_name)
        if address is None:
            raise SemanticErrorIPP23(f'Error: Label {label.label_name} does not exist', ErrorType.ERR_SEMANTICS)

        return address

    def declare_variable(self, var: Variable) -> None:
        """
        Declare variable without defining the value
        @param var: Variable
        @return: None
        """
        frame = self.get_frame(var.get_frame())
        frame.define_variable(var)

    def set_variable(self, var: Variable, value, value_type: DataType) -> None:
        """
        Set value for variable
        @param var: Variable
        @param value: New value for @p var
        @param value_type: Data type of @p value
        @return: None
        """
        frame = self.get_frame(var.get_frame())
        frame.set_variable(var, value, value_type)

    def _get_variable_value(self, var: Variable):
        """
        Get variable value
        @param var: Variable
        @return: Value stored at @p var
        """
        frame = self.get_frame(var.get_frame())
        return frame.get_value(var)

    def _get_variable_type(self, var: Variable) -> DataType:
        """
        Get variable data type
        @param var: Variable
        @return: DataType
        """
        frame = self.get_frame(var.get_frame())
        return frame.get_type(var)

    def del_variable(self, var: Variable) -> None:
        """
        Delete variable
        If it does not exist, nothing happens
        @param var: Variable
        @return: None
        """
        frame = self.get_frame(var.get_frame())
        frame.delete_var(var)

    def variable_is_initialized(self, var: Variable) -> bool:
        """
        Get information whether a variable is initialized
        @param var: Variable
        @return: bool
        """
        frame = self.get_frame(var.get_frame())
        return frame.is_initialized(var)

    def variable_exists(self, var: Variable) -> bool:
        """
        Get information about the existence of a variable
        @param var:
        @return:
        """
        frame = self.get_frame(var.get_frame())
        return frame.exists(var)

    def get_symbol_value(self, symbol: Symbol):
        if symbol.get_arg_type() == ArgumentType.VAR:
            # Variable
            return self._get_variable_value(symbol)
        else:
            # Constant
            return symbol.get_value()

    def get_symbol_type(self, symbol: Symbol):
        if symbol.get_arg_type() == ArgumentType.VAR:
            # Variable
            return self._get_variable_type(symbol)
        else:
            # Constant
            return symbol.get_type()

    def create_frame(self) -> None:
        """
        Create new temporary frame
        If temporary frame already exists it will be overwritten
        @return: None
        """
        self._temporary_frame.clear()
        self._temporary_frame_valid = True

    def push_frame(self) -> None:
        """
        Move temporary frame on top of local frames stack
        @raise RuntimeError
        @return: None
        """
        if not self._temporary_frame_valid:
            raise RuntimeErrorIPP23('Error: Temporary frame does not exist, it can not be pushed', ErrorType.ERR_NO_EXIST_FRAME)

        self._local_frames.append(copy.deepcopy(self._temporary_frame))
        self._temporary_frame_valid = False

    def pop_frame(self) -> None:
        """
        Move the top of local frames stack to temporary frame
        @raise RuntimeError
        @return: None
        """
        # No local frame
        if not self._local_frames:
            raise RuntimeErrorIPP23('Error: Temporary frame does not exist, it can not be popped', ErrorType.ERR_NO_EXIST_FRAME)

        self._temporary_frame = copy.deepcopy(self._local_frames.pop())
        self._temporary_frame_valid = True

    def get_frame(self, frame_type: FrameType) -> Frame:
        """
        Get the correct frame depending on the @p frame_type
        Meaning, either the global frame, temporary frame or the top of local frames stack
        @raise FrameError in case local or temporary frame should be returned but does not exist
        @param frame_type: FrameType
        @return: Frame
        """
        match frame_type:
            case FrameType.GF:
                frame = self._global_frame

            case FrameType.LF:
                # No local frame
                if not self._local_frames:
                    raise RuntimeErrorIPP23('Error: Temporary frame does not exist', ErrorType.ERR_NO_EXIST_FRAME)

                frame = self._local_frames[len(self._local_frames) - 1]

            case FrameType.TF:
                # Temporary frame does not exist
                if not self._temporary_frame_valid:
                    raise RuntimeErrorIPP23('Error: Temporary frame does not exist', ErrorType.ERR_NO_EXIST_FRAME)

                frame = self._temporary_frame

            case _:
                raise GenericErrorIPP23(f'Error: Incorrect frame type {frame_type}', ErrorType.ERR_SEMANTICS)
        return frame

    def call_stack_pop(self) -> int:
        """
        Get the address from the top of the call stack
        @raise RuntimeError
        @return: int
        """
        if not self._call_stack:
            raise RuntimeErrorIPP23('Error: Accessing an empty call stack', ErrorType.ERR_VAR_NOT_INIT)
        return self._call_stack.pop()

    def call_stack_push(self, address: int) -> None:
        """
        Push @p address to call stack
        @raise RuntimeError
        @param address: int
        @return: None
        """
        if address < 0:
            raise RuntimeErrorIPP23(f'Error: Invalid address: {address}', ErrorType.ERR_SEMANTICS)
        self._call_stack.append(address)

    def data_stack_pop(self) -> Symbol:
        if not self._data_stack:
            raise RuntimeErrorIPP23('Error: Accessing an empty data stack', ErrorType.ERR_VAR_NOT_INIT)
        return self._data_stack.pop()

    def data_stack_push(self, symbol: Symbol) -> None:
        self._data_stack.append(symbol)

    def __repr__(self):
        program_counter = f'Program counter: {self.program_counter}\n'
        labels = 'Labels:\n' + str(self._labels) + '\n'
        global_frame = 'Global frame:\n' + str(self._global_frame) + '\n'
        temporary_frame = 'Temporary frame:\n'
        if self._temporary_frame_valid:
            temporary_frame += str(self._temporary_frame)
        temporary_frame += '\n'

        local_frames = 'Local frames: \n'
        for frame, i in enumerate(self._local_frames):
            local_frames += f'Frame {i}:\n' + str(frame) + '\n'

        data_stack = 'Data stack: \n'
        for data in self._data_stack:
            data_stack += str(data) + '\n'

        call_stack = 'Call stack: \n' + str(self._call_stack)

        return program_counter + labels + global_frame + temporary_frame + local_frames + data_stack + call_stack + '\n'
