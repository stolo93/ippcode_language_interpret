"""!
@package ipp23
@file frame.py
@author Samuel Stolarik
@date 2023-04-02
"""

from .argument import Variable
from .exceptions import RuntimeErrorIPP23, SemanticErrorIPP23, ErrorType
from .type_enums import DataType


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
            raise RuntimeErrorIPP23(f'Error: Variable {var.name} not initialized, can not get value', ErrorType.ERR_VAR_NOT_INIT)

        return self.variables[var.name].get_value()

    def get_type(self, var: Variable):
        """
        Get type of @p var
        @raise RuntimeError
        @param var: Variable
        @return: Type
        """
        if not self.is_initialized(var):
            raise RuntimeErrorIPP23(f'Error: Variable {var.name} not initialized, can not get type', ErrorType.ERR_VAR_NOT_INIT)

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

    def __repr__(self):
        return str(self.variables)
