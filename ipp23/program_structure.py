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


class Program:
    """
    Class storing all data about currently interpreted program
    """
    def __init__(self, input_data: list = None):
        self.pc = 0

        if input_data is None:
            self.input_valid = False
            self.input_lines = []
        else:
            self.input_valid = True
            self.input_lines = input_data
        self.input_cur_line = 0

        self.labels = {}

        self.global_frame = Frame()
        self.temporary_frame = Frame()
        self.temporary_frame_valid = False

        self.local_frames = []
