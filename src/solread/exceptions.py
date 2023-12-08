# @2023 Aine Productions.
# Exceptions specific to SOLRead, and functions for calling them, are defined here.
# This file cannot be run directly.

class NoConnectionError(Exception):
    """Cannot connect to a given port.
    """
    pass

class FileError(Exception):
    """File is not intended to be run directly.
    """
    pass

def raiseException(classname):
    """Calls a SOLRead exception with added text.
    """

if __name__ == "__main__":
    raise FileError("this file cannot be run directly")
