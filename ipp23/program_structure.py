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


class Frame:
    """
    Local frame for variables
    @todo error handling
    """
    def __init__(self):
        self.variables = {}

    def define_variable(self, var: Variable):
        """
        Make entry for @p var in this frame
        @raise If @p var already exists redefinition error will be raised
        @param var: Variable
        @return: void
        """
        if self.is_defined(var):
            # TODO raise redefinition error
            pass
        else:
            self.variables[var.name] = var

    def set_variable(self, var: Variable, value, value_type: DataType):
        """
        Set variable value
        @raise Undefined var error
        @param var: Variable which should be set
        @param value: New value
        @param value_type: Type of value
        @return: void
        """
        if not self.is_defined(var):
            # TODO raise not declared error
            return
        self.variables[var.name].set_value(value, value_type)

    def get_value(self, var: Variable):
        """
        Get value of @p var
        @raise Undefined variable error
        @param var: Variable
        @return: Value or None in case of uninitialized variable
        """
        if not self.is_defined(var):
            # TODO raise not declared error
            return
        return self.variables[var.name].get_value()

    def get_type(self, var: Variable):
        """
        Get type of @p var
        @raise Undefined variable error
        @param var: Variable
        @return: Type or None in case of uninitialized variable
        """
        if not self.is_defined(var):
            # TODO raise not declared error
            return
        return self.variables[var.name].get_type()

    def is_initialized(self, var: Variable) -> bool:
        """
        Is variable initialized, meaning it was already assigned value
        @raise Undefined var error
        @param var: Variable
        @return: bool
        """
        if not self.is_defined(var):
            # TODO raise undefined var error
            return False

        return self.variables[var.name].is_initialized()

    def is_defined(self, var: Variable) -> bool:
        """
        Get information about existence of @p var
        @param var: Variable
        @return: bool
        """
        if not self.variables.get(var.name) is None:
            return True
        else:
            return False

    def delete_var(self, var: Variable):
        """
        Delete @p var from frame
        If variable does not exist, does nothing
        @param var: Variable
        @return: void
        """
        if self.is_defined(var):
            self.variables.pop(var.name)

    def clear(self):
        """
        Delete all variables
        @return: void
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
        @raise Value error, if @p new_pc is a negative value
        @param new_pc: New value
        @return: None
        """
        if new_pc < 0:
            # TODO raise value error
            pass
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
        @raise Value error if the label is already used
        @param label
        @param address
        @return: None
        """
        if self.labels.get(label.label_name) is None:
            self.labels[label.label_name] = address
        else:
            # TODO raise already used
            pass

    def get_label_address(self, label: Label) -> int:
        """
        Return address at which @p label is located
        @raise Value error if label is not defined
        @param label: Label
        @return: Address
        """
        address = self.labels.get(label.label_name)
        if address is None:
            # TODO raise not defined error
            pass

        return address

    def declare_variable(self, var: Variable) -> None:
        """
        Declare variable without defining the value
        @raise Variable already defined
        @param var: Variable
        @return: None
        """
        frame = self.get_frame(var.get_frame())
        # TODO try
        frame.define_variable(var)

    def set_variable(self, var: Variable, value, value_type: DataType) -> None:
        """
        Set value for variable
        @raise Undefined variable error
        @param var: Variable
        @param value: New value for @p var
        @param value_type: Data type of @p value
        @return: None
        """
        # TODO try
        frame = self.get_frame(var.get_frame())
        frame.set_variable(var, value, value_type)

    def get_variable_value(self, var: Variable):
        """
        Get variable value
        @raise
        @param var: Variable
        @return: Value stored at @p var
        """
        # TODO try
        frame = self.get_frame(var.get_frame())
        return frame.get_value(var)

    def get_variable_type(self, var: Variable) -> DataType:
        """
        Get variable data type
        @raise
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
        @return:
        """
        self.temporary_frame.clear()
        self.temporary_frame_valid = True

    def push_frame(self) -> None:
        """
        Move temporary frame on top of local frames stack
        @raise FrameError in case temporary frame does not exist
        @return: None
        """
        if self.temporary_frame_valid:
            self.local_frames.append(copy.deepcopy(self.temporary_frame))
            self.temporary_frame_valid = False
        else:
            # TODO raise undefined frame error 55
            pass

    def pop_frame(self) -> None:
        """
        Move the top of local frames stack to temporary frame
        @raise FrameError in case no local frame exists
        @return: None
        """
        # No local frame
        if not self.local_frames:
            # TODO raise undefined local frame 55
            pass
        else:
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
                    # TODO raise local frame not valid
                    pass
                else:
                    frame = self.local_frames[len(self.local_frames)-1]

            case FrameType.TF:
                if self.temporary_frame_valid:
                    frame = self.temporary_frame
                else:
                    # TODO raise temporary frame not valid
                    pass

            case default:
                # TODO raise invalid frame type
                frame = self.global_frame
        return frame