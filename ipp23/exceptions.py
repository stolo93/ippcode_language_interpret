"""!
@package ipp23
@file exception
@author Samuel Stolarik
@date 2023-04-01
"""
from enum import Enum


class ErrorType(Enum):
    ERR_CLI_ARGS = 10
    ERR_INP_FILE = 11
    ERR_OUT_FILE = 12
    ERR_INTERNAL = 99
    ERR_XML_FORMAT = 31
    ERR_XML_STRUCT = 32
    ERR_SEMANTICS = 52
    ERR_OPERAND_TYPE = 53
    ERR_OPERAND_VALUE = 57
    ERR_NO_EXIST_VAR = 54
    ERR_NO_EXIST_FRAME = 55
    ERR_UNDEF_VAR = 56
    ERR_STRING = 58


class GenericErrorIPP23(Exception):
    def __init__(self, message: str, error_type: ErrorType):
        super().__init__(message)
        self.exit_code = error_type.value


class RuntimeErrorIPP23(Exception):
    def __init__(self, message: str, error_type: ErrorType):
        super().__init__(message)
        self.exit_code = error_type.value


class SemanticErrorIPP23(Exception):
    def __init__(self, message: str, error_type: ErrorType):
        super().__init__(message)
        self.exit_code = error_type.value


class XMLErrorIPP23(Exception):
    def __init__(self, message: str, error_type: ErrorType):
        super().__init__(message)
        self.exit_code = error_type.value