"""!
@package ipp23
@file program_structure.py
@author Samuel Stolarik
@date 2023-03-27
"""


class Frame:
    """
    Local frame for variables
    @todo error handling
    """
    def __init__(self):
        self.variables = {}

    def define_variable(self, name: str):
        if self.__is_defined(name):
            # TODO Error: variable already defined
            pass
        else:
            self.variables[name] = (None, None)

    def set_variable(self, name: str, value, var_type: str):
        if self.__is_defined(name):
            self.variables[name] = (value, var_type)
        else:
            # TODO Error: undefined variable
            pass

    def get_value(self, name: str):
        if self.__is_defined(name):
            return self.variables[name][0]
        else:
            # TODO Error: undefined variable
            pass

    def get_type(self, name: str):
        if self.__is_defined(name):
            return self.variables[name][1]
        else:
            # TODO Error: undefined variable
            pass

    def __is_defined(self, name: str):
        if self.variables.get(name) is None:
            return False
        else:
            return True