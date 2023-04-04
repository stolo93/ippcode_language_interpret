"""!
@file interpret.py
@author Samuel Stolarik
@date 2023-04-04
"""
import argparse
import sys
from contextlib import contextmanager

from ipp23.interpret import Interpret
from ipp23.exceptions import GenericErrorIPP23, RuntimeErrorIPP23, SemanticErrorIPP23, XMLErrorIPP23, ExitProgramException, ErrorType


@contextmanager
def open_file_or_stdin(file):
    """
    Context manager for either @p file or sys.stdin
    @param file:
    @return:
    """
    if file != sys.stdin:
        try:
            with open(file, 'r') as f:
                yield f
        except FileNotFoundError:
            raise GenericErrorIPP23(f'Error: file {file} not found', ErrorType.ERR_INP_FILE)

    else:
        yield sys.stdin


def parse_args():
    """
    Parse command line arguments
    if --help, print help message and exit program
    supports:
    --help
    --source
    --file
    @raise GenericError
    @return: arguments parsed
    """
    parser = argparse.ArgumentParser(prog='interpret.py', description='Interpret for IPPcode 23', epilog='Author: Samuel Stolarik', add_help=False)

    parser.add_argument('--help', '-h', action='store_true', default=None, help='Show help message and exit')
    parser.add_argument('--source', '-s', action='store', default=sys.stdin, help='Source file with IPPcode23')
    parser.add_argument('--input', '-i', action='store', default=sys.stdin, help='Input file for the interpreted program')

    args, unknown = parser.parse_known_args()

    if unknown:
        raise GenericErrorIPP23(f"Error: unknown arguments: {' '.join(unknown)}", ErrorType.ERR_CLI_ARGS)

    if args.source == sys.stdin and args.input == sys.stdin:
        raise GenericErrorIPP23(f'Error: Only one argument can be provided', ErrorType.ERR_CLI_ARGS)

    if args.source == sys.stdin and args.input == sys.stdin and args.help is None:
        raise GenericErrorIPP23(f'Error: Exactly one argument must be provided', ErrorType.ERR_CLI_ARGS)

    if args.help:
        if args.source is not None or args.input is not None:
            raise GenericErrorIPP23(f'Error: Only one argument can be provided', ErrorType.ERR_CLI_ARGS)
        parser.print_help()
        sys.exit(0)

    return args


def main():
    try:
        args = parse_args()
    except GenericErrorIPP23 as e:
        print(e, file=sys.stderr)
        sys.exit(e.exit_code)

    try:
        with open_file_or_stdin(args.source) as source_file, open_file_or_stdin(args.input) as input_file:
            itp = Interpret()
            itp.load(source_file)
            itp.initialize(input_file)
            itp.execute()
    except (GenericErrorIPP23, XMLErrorIPP23, SemanticErrorIPP23, RuntimeErrorIPP23, ExitProgramException) as e:
        print(e, file=sys.stderr)
        sys.exit(e.exit_code)


if __name__ == '__main__':
    main()
