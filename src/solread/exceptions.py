# @2023 Aine Productions.
# SOLRead-specific exception are defined here.
# This file cannot be run directly.

class NoConnectionError(Exception):
    """Cannot connect to a given port.
    """
    pass

class AccessError(TypeError):
    """File is not intended to be accessed.
    """
    pass

class AutoError(TypeError):
    """Automation function receives an argument of inappropriate type.
    """


# of course, an exception is raised if this file is directly run anyway
if __name__ == "__main__":
    raise AccessError("this file cannot be run directly")
