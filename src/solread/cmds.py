# @2023 Aine Productions.
# SOLRead commands are defined here.
# This file cannot be run by itself, use the command line to run these.

import csv
import math
import os.path as path

import click
import matplotlib.pyplot as plt
from rich.console import Console

from solread.mathcore import SolarCell, slexc

try:
    from nsp2visasim import sim_pyvisa as pyvisa
except ModuleNotFoundError:
    import pyvisa

def scribe_data(data_tuple, save_file, rich_console=""):
    """Writes data from a tuple into the specified .csv file.

    Args:
        data_tuple (tuple): The data to be written into a .csv file. Must consist of four integers or array-likes, otherwise TypeError is raised.
        save_file (string): The .csv file to be written into.
        rich_console (class, optional): Name of the Rich console. If a console is specified, changes printed text into rich text. Defaults to an empty string.
    """
    # check and raise for user errors before executing code
    print("Saving data", end="\r")
    if type(data_tuple) != tuple:
        raise TypeError(f"argument 'data_tuple' is not a tuple")
    elif len(data_tuple) != 4:
        raise TypeError(f"4 lists are required, but {len(data_tuple)} lists are given")
    else:
        vol_list, cur_list, errcur_list, errvol_list = data_tuple

    # then, execute code
    if path.isfile(f"{save_file}.csv") == False:
        filename = save_file + ".csv"
    elif path.isfile(f"{save_file}.csv") == True:
        i = 1
        is_taken = True
        while is_taken == True:
            if path.isfile(f"{save_file}-{i}.csv") == False:
                filename = save_file + "-" + str(i) + ".csv"
                is_taken = False
            else:
                i += 1

    with open(filename, "w", newline="") as measurements:
        writer = csv.writer(measurements)
        writer.writerow(["voltage [V]", "error on voltage [V]", "current [A]", "error on current [A]"])
        for a, b, c, d in zip(vol_list, errvol_list, cur_list, errcur_list):
            writer.writerow([a, b, c, d])
        if rich_console != "":
            rich_console.print(f"[green]Data saved to [/][bright_cyan]{filename}[/]")
        else:
            print(f"Data saved to {filename}")

def visualise_data(data, rich_console=""):
    """Inserts given values into a graph, and shows it.

    Args:
        data (tuple): The tuple to retrieve values from. The tuple must consist of four integers, floats or array-likes, otherwise TypeError is raised.
        Lists are specified as follows:
            vol_list: the x-values of the graph.
            cur_list: the y-values of the graph.
            vol_error: the errors on the x-values.
            cur_error: the errors on the y-values.
        rich_console (class, optional): Name of the Rich console. If a console is specified, changes printed text into rich text. Defaults to an empty string.
    """
    # check and raise for user errors before code execution
    if type(data) != tuple:
        raise TypeError(f"argument 'data_tuple' is not a tuple")
    elif len(data) != 4:
        raise TypeError(f"exactly 4 lists are required, but {len(data)} lists are given")
    else:
        vol_list, cur_list, vol_error, cur_error = data
    
    print("Generating graph", end="\r")
    # plt.plot(vol_list, cur_list, 'b.')
    plt.errorbar(vol_list, cur_list, fmt="ro", xerr=vol_error, yerr=cur_error)
    plt.ylabel("current [A]")
    plt.ylim(0)
    plt.xlabel("voltage [V]")
    plt.xlim(0)
    plt.title("UI-characteristic of a red LED diode")
    plt.show()
    
    if rich_console != "":
        rich_console.print("[gray]Generating graph: [/][green]complete")
    else:
        print("Generating graph: complete")

@click.group()
def solread():
    pass

@solread.command("info")
def solinfo():
    """Prints a short summary of what SOLRead is and what it does.
    """
    rich_console = Console()
    rich_console.print("@2023 [red]Aine Productions[/].")
    rich_console.print("[yellow]SOLRead v1.0.0[/], last updated [cyan]December 12th, 2023[/].")
    rich_console.print("Solar cell reader for [yellow]Python 3.10+[/].")
    rich_console.print("Allows users to determine the UI-characteristic of any solar cell.")
    rich_console.print("[blue]Note:[/] Requires correct Arduino setup to work correctly. Consult setup by viewing [yellow]solarcellsetup.png[/].")




@solread.command("list")
@click.option("--search", "-s", type=str, help="Search active connections for a string matching the query.")
def get_connections(search):
    """Retrieve the port names of active connections.
    Port names are retrieves through the use of a pyvisa ResourceManager.

    Optionally, looks for specific strings in the port names if 'search' is specified.

    Additionally specifies whether connections exist or how many there are, and prints the port names if connections exist.
    """
    rich_console = Console()
    rm = pyvisa.ResourceManager("@py")
    if search:
        connections = rm.list_resources(search)
        if len(connections) == 0:
            rich_console.print(f"[red]No connections located[/] that match your query [bright_cyan]{search}[/].")
        else:
            rich_console.print(f"[green]{len(connections)} connection(s)[/] located matching the query [bright_cyan]{search}[/]:")
            for port in range(0, len(connections)):
                print(connections[port])
    else:
        connections = rm.list_resources()
        if len(connections) == 0:
            rich_console.print("No connections located.", style="red")
        else:
            rich_console.print(f"[green]{len(connections)} connection(s)[/] located:")
            for port in range(0, len(connections)):
                print(connections[port])
    rm.close()
    return connections

@solread.command("read")
@click.argument("port", type=str)
@click.option("--resvalue", "-r", default=1.65, type=click.FloatRange(0.004, 3.3), help="Put this current on the resistor.", show_default=True)
@click.option("--counts", "-c", default=5, type=click.IntRange(2, math.inf), help="Read the solar cell this amount of times.", show_default=True)
@click.option("--start", "-s", default=0, type=click.FloatRange(0, 3.296), help="Start scans at this value.", show_default=True)
@click.option("--end", "-e", default=3.3, type=click.FloatRange(0.004, 3.3), help="End scans at this value.", show_default=True)
@click.option("--graph/--no-graph", "-g/-ng", default=None, help="Choose whether to generate a graph or not.", show_default=True)
@click.option("--filesave", "-f", default="", type=str, help="Choose whether to save data to a .csv file or not.", show_default=True)
def readsol(port, resvalue, counts, start, end, graph, filesave):
    """
    Starts the read of a solar cell from the command line interface.
    The scan is performed through the exec_experiment() class method.

    Prints the retrieved voltage and current values as a pandas DataFrame.
    If specified, uses all value lists to make a .csv file with the scribe_data() function instead and/or make a graph with the visualise_data() function. \f

    Args:
        port (str): The port to initiate a scan from. readsol() looks for a port matching that name, and raises a NoConnectionError if it can't find one.
        counts (int, optional): The amount of scans that take place. More repeats decrease errors on values. Defaults to 5.
        start (int, optional): The scan start point. Defaults to 0 [range = {0, 3.296}]
        end (int, optional): The scan end point. Defaults to 3.3 [range = {0.003, 3.3}]
        graph (any, optional): If this argument is called using "-g" (or isn't None), also creates a graph.
        filesave (string, optional): Where to save the scan results. This function will write data to filesave.csv.
    """

    rich_console = Console()

    # first, look for a port matching the port query
    rich_console.print("[gray]Finding port...[/]", end="\r")
    rm = pyvisa.ResourceManager("@py")
    available_ports = rm.list_resources(port)

    if len(available_ports) == 0:
        rich_console.print("[bold red]Finding port: failed[/]")
        raise slexc.NoConnectionError(f"no connections detected matching string '{port}'")
    elif len(available_ports) > 1:
        rich_console.print("Finding port: [green]complete[/]", style="bold")
        # if detecting multiple suitable ports, prints the names of each port and lets the user choose between them
        rich_console.print(f"[blue]Note:[/] Multiple connections detected matching string [bright_cyan]{port}[/]")
        for options in range(0, len(available_ports)):
            print(f"{(options + 1)}: {available_ports[options]}")
        input_option = int(input("Select port option (leave empty for option 1): "))

        if input_option == "":
            port_option = available_ports[0]
        elif input_option > (len(available_ports) + 1):
            raise IndexError(f"port option {input_option} is not included as an option")

        else:
            port_option = available_ports[(input_option - 1)]
    else:
        rich_console.print("Finding port: [green]complete[/]", style="bold")
        port_option = available_ports[0]


    # check and correct for user errors before executing the code
    rich_console.print("[gray]Error checking...[/]", end="\r")
    try:
        cell = SolarCell(port_option)
    except Exception as e:
        rich_console.print("[bold red]Error checking: failed[/]")
        print(f"Cannot connect to port '{port_option}': {str(e)}")
        return
    else:
        rich_console.print("Error checking: [green]complete[/]")
    if ".csv" in filesave:
        save_file = filesave.replace(".csv", "")
    else:
        save_file = filesave

    # then, begin the experiment
    rich_console.print(f"Executing scan with following values:")
    rich_console.print(f"port = [cyan]{port_option}[/], resistor current = [cyan]{resvalue}[/] V, counts = [cyan]{counts}[/], scan range = [cyan]{start}[/] to [cyan]{end}[/] V")
    currents, cur_errors, voltages, vol_errors = cell.exec_experiment(counts, start, end, resvalue)

    rich_console.print(f"Executing scan: [green]complete[/]")
    if graph:
        visualise_data((voltages, currents, vol_errors, cur_errors), rich_console)

    if filesave:
        scribe_data((voltages, currents, vol_errors, cur_errors), save_file, rich_console)

    rich_console.print("Scanning complete!", style="green")
    rm.close()


# of course, an exception is raised if this file is directly run anyway
if __name__ == "__main__":
    raise slexc.AccessError("This file cannot be run directly. Use the command line interface to run these.")
