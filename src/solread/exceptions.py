# @2023 Aine Productions.
# Exceptions specific to SOLRead, and functions for calling them, are defined here.
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

def raiseException(classname, exc_text=None):
    """Calls a SOLRead exception but with more polish.

    Args:
        classname (class): The SOLRead exception to be called.
    """
    except_type = str(classname)

    match classname:
        case "NoConnectionError":
            print(f"NoConnectionError: no connection can be made to this port: {exc_text}")


# 
if __name__ == "__main__":
    raise AccessError("this file cannot be run directly")
