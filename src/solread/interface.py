# @2023 Aine Productions.
# This file cannot be run by itself, use the command line to run these.

try:
    from nsp2visasim import sim_pyvisa as pyvisa
except ModuleNotFoundError:
    import pyvisa

import solread.exceptions as slexc


def uv_con(value, mode=0):
    """Converts a digital value into an analog value or vice versa.
    Also returns the converted value as an integer (if converted to digital) or a float (if converted to analog).

    Args:
        value (int or float): The value to be converted.
        mode (int or string, optional): The mode of conversion. Defaults to 0.
            0 or "analog": digital to analog.
            1 or "digital": analog to digital.
            2 or "auto": automatically chooses one or the other, based on the type of your initial value. 
            Raises AutoError if the value isn't an integer or float.

            Note: If 'mode' is set to anything other than the above values, this program 
            raises ValueError (if 'mode' is an integer) or TypeError (in all other cases).
    """
    match mode:
        case 0 | "analog":
            volts = value * (3.3 / 1023)
            output = float(volts) # output gets converted into a float for smoother operation
        case 1 | "digital":
            units = value / (3.3 / 1023)
            output = round(units) # output gets rounded to prevent errors in ArduinoInterface class methods
        case 2 | "auto":
            if type(value) == float:
                units = value / (3.3 / 1023)
                output = round(units)
            elif type(value) == int:
                volts = value * (3.3 / 1023)
                output = float(volts)
            else:
                raise slexc.AutoError(f"Automatic conversion cannot resolve an argument of type {str(type(value))}. Try again with different values.")
        case _:
            if type(mode) == int:
                raise ValueError(f"argument 'mode' is {mode}, but must be 0, 1 or 2")
            else:
                raise TypeError(f"mode '{mode}' is undefined")
    return output

def listdevices(connection):
    """List all connected devices using an existing Interface.
    As such, if the argument 'connection' isn't an Interface, this function raises a TypeError.

    Args:
        connection (class): an active interface
    """
    if isinstance(connection, ArduinoInterface):
        ports = connection.rm.list_resources()
        print(ports)
    else:
        raise TypeError(f"connection '{connection}' is not an Arduino Interface")


class ArduinoInterface:
    def __init__(self, port):
        """Device for communication with an Arduino through Virtual Instrument Software Architecture (VISA) protocols.
        """
        self.port = port
        self.rm = pyvisa.ResourceManager("@py")
        self.device = self.rm.open_resource(
            self.port, read_termination="\r\n", write_termination="\n"
        )
    
    def set_input_value(self, val, ch):
        """Sets a current on an Arduino channel.

        Args:
            val (int): The current to be put on the channel, in digital ADC units. If val is a float, convert to integer using `uv_con(val, 1)`.
            ch (int): The Arduino channel to set the input value of.
        """
        self.device.query(f"OUT:CH{ch} {val}")

    def get_output_value(self, ch):
        """Retrieves the output value on an Arduino channel.
        This value is returned as an integer in digital units.

        Args:
            ch (int): The Arduino channel to read from.
        """
        if ch == 0:
            output = self.device.query("OUT:CH0?")
        else:
            output = self.device.query(f"MEAS:CH{ch}?")
        return int(output)

if __name__ == "__main__":
    raise slexc.AccessError("this file cannot be run directly")


