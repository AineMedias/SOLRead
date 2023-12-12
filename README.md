# SOLRead, solar cell reader for Python 3.10+
 This project has been made possible by Aine Productions, a group consisting of third-year BSc students at the University of Amsterdam.

 This solar cell reader will allow you to read the UI-characteristic of any solar cell, provided the Arduino is set up correctly.
 Consult this setup by viewing the `solarcellsetup.png` image.

 [Intended setup for optimal SOLRead operation.](solarcellsetup.png)
 The solar cell itself is attached to the `+` and `-` power rails on the right side of the breadboard.


## Setup
 This project requires Poetry, as well as Anaconda and Python 3.10 or greater.
 Poetry is a packaging and dependency management program, which here is used to install all of SOLRead's dependencies.
 To install Poetry, open an Anaconda Prompt and type in `pip install poetry`.
 Note: Some computers may not be able to handle Poetry when going to a different conda environment. To solve this, type in `pip install poetry` while in your current environment.

 Running it now should cause an ImportError to be raised.
 This is normal, because you still need to install the SOLRead project and the dependencies on which it relies.
 Ordinarily, you are used to installing it through pip or pipx, but this time you don't need to do that.
 To install these dependencies, go to the directory in which SOLRead is installed, and type `poetry install`.
 Afterwards, it's recommended that you use the Command Prompt (Anaconda Prompt) to run SOLRead, not a VS Code terminal.

## Commands
 SOLRead defines three commands, `read`, `info` and `list`.
 A guide to these commands can be found by using `solread [command] --help`. 