"""!
@package program
@file type_enums.py
@author Samuel Stolarik
@date 2023-04-02
"""
import enum


class ArgumentType(enum.Enum):
    """
    Instruction argument types
    """
    VAR = 'var'
    CONST_VALUE = 'const'
    LABEL = 'label'
    TYPE = 'type'


class DataType(enum.Enum):
    """
    IPPcode23 data types
    """
    NIL = 'nil'
    INT = 'int'
    STRING = 'string'
    BOOL = 'bool'


class FrameType(enum.Enum):
    """
    Variable frames
    """
    GF = 'gf'
    TF = 'tf'
    LF = 'lf'
