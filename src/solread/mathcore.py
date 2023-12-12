# @2023 Aine Productions.
# This file cannot be run by itself.
# Math Core of SOLRead, responsible for handling the math behind the calculations.

import numpy

from solread.interface import ArduinoInterface, slexc, uv_con


class SolarCell():
    """Defines a solar cell.
    """
    def __init__(self, port):
        self.port = port
        if self.port == "":
            raise TypeError("argument 'port' is not defined")
        else:
            self.connection = ArduinoInterface(self.port)

    def scan(self, start=0, end=1023, grounding=511):
        """Scans the solar cell once with start and end values, as well as resistance values on the MOSFET.
        Returns two tuples, essentially lists, containing acquired voltage values and current values respectively.
        Note: Incorrect Arduino setups may lead to errors. Consult the README file before proceeding.

        Args:
            start (float): The start point of your scan. Defaults to 0.
            end (float): The end point of your scan. Defaults to 1023.
            grounding (int): The digital value of the resistance on the MOSFET. Defaults to 511.
        """
        # check for user errors before executing code
        if start == end:
            raise ValueError("arguments 'start' and 'end' cannot be the same value")
        elif start > end:
            # if start is larger than end, the two values get swapped
            start_value = end
            end_value = start
        else:
            start_value = start
            end_value = end
        if end_value > 1023:
            raise ValueError(f"end value ({end_value}) exceeds overflow limit")
        if grounding <= 0:
            raise ValueError("argument 'grounding' must be a nonzero positive integer")
        elif (grounding % 1) != 0:
            res_value = round(grounding) # grounding gets rounded if it's not an integer
        elif grounding > 1023:
            raise ValueError(f"value of argument 'grounding' ({grounding}) exceeds overflow limit")
        else:
            res_value = grounding


        # begin code execution
        vol_array = []
        cur_array = []
        scan_range = range(start_value, (end_value + 1))

        for i in scan_range:
            volt = i
            self.connection.set_input_value(volt, 0)
            vol_1 = 3 * uv_con(self.connection.get_output_value(1))
            vol_2 = uv_con(self.connection.get_output_value(2))
            
            current = vol_2 / 4.7 + vol_1 / 1e+6
            vol_array.append(vol_1)
            cur_array.append(current)

            # at the end of measurements, reset values
            if i == end_value:
                self.connection.set_input_value(0, 1)
        return vol_array, cur_array
    
    def exec_experiment(self, repeats, start=None, end=None, resvalue=None):
        """Repeat the scan a number of times, equal to repeats.
        Takes the average and standard deviation of the voltage and current values obtained from each scan.

        Args:
            repeats (int): the amount of times the solar cell is scanned.
            start (float): the start value of the scan.
            end (float): the end point of the scan.
            resvalue (float): the voltage on the variable resistor. Higher values for `resvalue` mean higher resistance.
        """
        avg_volarray = []
        avg_curarray = []
        vol_2darray = []
        cur_2darray = []
        vol_error = []
        cur_error = []

        start_value = uv_con(start, 1)
        end_value = uv_con(end, 1)
        resistance = uv_con(resvalue, 1)

        for i in range(0, repeats):
            vol_array, cur_array = self.scan(start_value, end_value, resistance)
            vol_2darray.append(vol_array)
            cur_2darray.append(cur_array)
        data_points = abs(end_value - start_value) + 1

        for n in range(0, data_points):
            value_array = []
            value_array2 = []
            for lists in range(0, (repeats - 1)):
                value_array.append(cur_2darray[lists][n])
                value_array2.append(vol_2darray[lists][n])

            avg_curarray.append(numpy.mean(value_array))
            avg_volarray.append(numpy.mean(value_array2))
            cur_error.append(numpy.std(value_array) / (repeats**0.5))
            vol_error.append(numpy.std(value_array2) / (repeats**0.5))
        
        return avg_curarray, cur_error, avg_volarray, vol_error
    
if __name__ == "__main__":
    raise slexc.AccessError("this file cannot be run by itself")

            

