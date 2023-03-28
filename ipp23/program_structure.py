"""!
@package ipp23
@file program_structure.py
@author Samuel Stolarik
@date 2023-03-27
"""
import io
import sys

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
        self.pc = 0
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
