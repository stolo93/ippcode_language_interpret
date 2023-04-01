"""!
@package ipp23
@file program_structure.py
@author Samuel Stolarik
@date 2023-03-27
"""
import io
import sys
import copy

from ipp23.instruction import *
from ipp23.exceptions import *


class Frame:
    """
    Local frame for variables
    """
    def __init__(self):
        self.variables = {}

    def define_variable(self, var: Variable) -> None:
        """
        Make entry for @p var in this frame
        @raise SemanticError
        @param var: Variable
        @return: None
        """
        if self.exists(var):
            raise SemanticErrorIPP23('Error: Variable redefinition', ErrorType.ERR_SEMANTICS)

        self.variables[var.name] = var

    def set_variable(self, var: Variable, value, value_type: DataType) -> None:
        """
        Set variable value
        @raise RuntimeError
        @param var: Variable which should be set
        @param value: New value
        @param value_type: Type of value
        @return: None
        """
        if not self.exists(var):
            raise RuntimeErrorIPP23(f'Error: Variable {var.name} does not exist', ErrorType.ERR_NO_EXIST_VAR)

        self.variables[var.name].set_value(value, value_type)

    def get_value(self, var: Variable):
        """
        Get value of @p var
        @raise RuntimeError
        @param var: Variable
        @return: Value
        """
        if not self.is_initialized(var):
            raise RuntimeErrorIPP23(f'Error: Variable {var.name} not initialized, can not get value', ErrorType.ERR_UNDEF_VAR)

        return self.variables[var.name].get_value()

    def get_type(self, var: Variable):
        """
        Get type of @p var
        @raise RuntimeError
        @param var: Variable
        @return: Type
        """
        if not self.is_initialized(var):
            raise RuntimeErrorIPP23(f'Error: Variable {var.name} not initialized, can not get type', ErrorType.ERR_UNDEF_VAR)

        return self.variables[var.name].get_type()

    def is_initialized(self, var: Variable) -> bool:
        """
        Is variable initialized, meaning it was already assigned value
        @raise RuntimeError
        @param var: Variable
        @return: bool
        """
        if not self.exists(var):
            raise RuntimeErrorIPP23(f'Error: Variable {var.name} does not exist', ErrorType.ERR_NO_EXIST_VAR)

        return self.variables[var.name].is_initialized()

    def exists(self, var: Variable) -> bool:
        """
        Get information about existence of @p var
        @param var: Variable
        @return: bool
        """
        if not self.variables.get(var.name) is None:
            return True
        else:
            return False

    def delete_var(self, var: Variable) -> None:
        """
        Delete @p var from frame
        If variable does not exist, does nothing
        @param var: Variable
        @return: None
        """
        if self.exists(var):
            self.variables.pop(var.name)

    def clear(self) -> None:
        """
        Delete all variables
        @return: None
        """
        self.variables.clear()


class Program:
    """
    Class storing all data about currently interpreted program
    """
    def __init__(self, file_in: io.TextIOWrapper = sys.stdin):
        # Program counter
        self.program_counter = 0
        # Input for program
        self.file_in = file_in
        # Labels
        self.labels = {}
        # Global frame (initialized since the beginning)
        self.global_frame = Frame()
        # Temporary frame (has to be created with)
        self.temporary_frame = Frame()
        self.temporary_frame_valid = False
        # Stack of local frame
        self.local_frames: list[Frame] = []
        # Data stack (stack of symbols)
        self.data_stack: list[Symbol] = []

    def set_program_counter(self, new_pc: int) -> None:
        """
        Set program counter to @p new_pc
        @raise SemanticError
        @param new_pc: New value
        @return: None
        """
        if new_pc < 0:
            raise SemanticErrorIPP23(f'Error: Invalid program counter value {new_pc}', ErrorType.ERR_SEMANTICS)

        self.program_counter = new_pc

    def get_program_counter(self) -> int:
        """
        Get current value of program counter
        @return: Current program value
        """
        return self.program_counter

    def get_line(self) -> str:
        """
        Get one line from input to the interpreted program
        @return: One line from input
        """
        return self.file_in.readline()

    def create_label(self, label: Label, address: int) -> None:
        """
        Create label at address
        @raise SemanticError
        @param label
        @param address
        @return: None
        """
        if self.labels.get(label.label_name) is None:
            self.labels[label.label_name] = address
        else:
            raise SemanticErrorIPP23(f'Error: Label {label.label_name} already used', ErrorType.ERR_SEMANTICS)

    def get_label_address(self, label: Label) -> int:
        """
        Return address at which @p label is located
        @raise SemanticError
        @param label: Label
        @return: Address
        """
        address = self.labels.get(label.label_name)
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

    def get_variable_value(self, var: Variable):
        """
        Get variable value
        @param var: Variable
        @return: Value stored at @p var
        """
        frame = self.get_frame(var.get_frame())
        return frame.get_value(var)

    def get_variable_type(self, var: Variable) -> DataType:
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

    def create_frame(self) -> None:
        """
        Create new temporary frame
        If temporary frame already exists it will be overwritten
        @return: None
        """
        self.temporary_frame.clear()
        self.temporary_frame_valid = True

    def push_frame(self) -> None:
        """
        Move temporary frame on top of local frames stack
        @raise RuntimeError
        @return: None
        """
        if not self.temporary_frame_valid:
            raise RuntimeErrorIPP23('Error: Temporary frame does not exist, it can not be pushed', ErrorType.ERR_NO_EXIST_FRAME)

        self.local_frames.append(copy.deepcopy(self.temporary_frame))
        self.temporary_frame_valid = False

    def pop_frame(self) -> None:
        """
        Move the top of local frames stack to temporary frame
        @raise RuntimeError
        @return: None
        """
        # No local frame
        if not self.local_frames:
            raise RuntimeErrorIPP23('Error: Temporary frame does not exist, it can not be pushed', ErrorType.ERR_NO_EXIST_FRAME)

        self.temporary_frame = copy.deepcopy(self.local_frames.pop())
        self.temporary_frame_valid = True

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
                frame = self.global_frame

            case FrameType.LF:
                # No local frame
                if not self.local_frames:
                    raise RuntimeErrorIPP23('Error: Temporary frame does not exist, it can not be pushed', ErrorType.ERR_NO_EXIST_FRAME)

                frame = self.local_frames[len(self.local_frames)-1]

            case FrameType.TF:
                # Temporary frame does not exist
                if not self.temporary_frame_valid:
                    raise RuntimeErrorIPP23('Error: Temporary frame does not exist, it can not be pushed', ErrorType.ERR_NO_EXIST_FRAME)

                frame = self.temporary_frame

            case default:
                raise GenericErrorIPP23(f'Error: Incorrect frame type {frame_type}', ErrorType.ERR_SEMANTICS)
        return frame