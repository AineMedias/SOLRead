# @2023 Aine Productions.
# This file cannot be run by itself.
# Math Core of SOLRead, responsible for handling the math behind the calculations.

from solread.interface import ArduinoInterface


class SolarCell():
    """Defines a solar cell.
    """
    def __init__(self, port):
        self.port = port
        if self.port == "":
            raise TypeError("argument 'port' is not defined")
        else:
            self.connection = ArduinoInterface(self.port)

    def scan(self, start, end):
        """Scans the solar cell once.
        Returns two tuples, essentially lists, containing acquired voltage values and current values respectively.

        Args:
            start (float): The start point of your scan.
            end (float): The end point of your scan.
        """
