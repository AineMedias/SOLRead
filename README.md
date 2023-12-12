# SOLRead, solar cell reader for Python 3.10+
 This project has been made possible by Aine Productions, a group consisting of third-year BSc students at the University of Amsterdam.

 This solar cell reader will allow you to read the UI-characteristic of any solar cell, provided the Arduino is set up correctly.
 Consult this setup by viewing the `solarcellsetup.png` image.

 [Intended setup for optimal SOLRead operation.](solarcellsetup.png)
 The solar cell itself is attached to the `+` and `-` power rails on the right side of the breadboard.


## Setup
 This project requires Poetry, as well as Anaconda and Python 3.10 or greater.
 Poetry is a packaging and dependency management program, which here is used to install all of SOLRead's dependencies.
 To install Poetry, open an Anaconda Prompt and type in `pip install poetry`. Afterwards, create a new conda environment using `conda create -n [name] python=3.12`, where `[name]` is the name of your environment.
 Note: Some computers may not be able to handle Poetry when going to a different conda environment. To solve this, type in `pip install poetry` while in your current environment.

 Furthermore, it's recommended that you use the Command Prompt (Anaconda Prompt) to run SOLRead, not a VS Code terminal.

 Using `solread` in your new environment should cause an error:

 ```
 (base) C:\Users\13983164>conda activate solread

 (solread) C:\Users\13983164>solread
 'solread' is not recognized as an internal or external command,
 operable program or batch file.
 ```

 This is normal, because you still need to install the SOLRead project and the dependencies on which it relies.
 Ordinarily, you are used to installing these through pip or pipx, but you cannot install the project this way.
 To install these dependencies as well as the project itself, go to the directory where SOLRead is located.
 Typically, it should be located in a GitHub folder: `C:Users\...\Documents\GitHub\SOLRead`, so type `cd Documents\GitHub\SOLRead` in your command prompt to access the folder it's in.
 Then, once you're in that folder, type `poetry install`.

 Doing that should result in this:
 ```
 (solread) C:\Users\13983164\Documents\GitHub\SOLRead>poetry install
 Installing dependencies from lock file

 Package operations: 26 installs, 0 updates, 0 removals

  • Installing mdurl (0.1.2)
  • Installing numpy (1.26.2)
  • Installing six (1.16.0)
  • Installing typing-extensions (4.8.0)
  • Installing contourpy (1.2.0)
  • Installing cycler (0.12.1)
  • Installing fonttools (4.46.0)
  • Installing ifaddr (0.2.0)
  • Installing kiwisolver (1.4.5)
  • Installing markdown-it-py (3.0.0)
  • Installing packaging (23.2)
  • Installing pillow (10.1.0)
  • Installing pygments (2.17.2)
  • Installing pyparsing (3.1.1)
  • Installing python-dateutil (2.8.2)
  • Installing pytz (2023.3.post1)
  • Installing pyvisa (1.14.1)
  • Installing tzdata (2023.3)
  • Installing matplotlib (3.8.2)
  • Installing nsp2visasim (1.3.1)
  • Installing pandas (2.1.4)
  • Installing psutil (5.9.6)
  • Installing pyserial (3.5)
  • Installing pyvisa-py (0.7.1)
  • Installing rich (13.7.0)
  • Installing zeroconf (0.128.4)

 Installing the current project: solread (1.0.0a)
 ```

 If you've got the above, you're good to go and should be able to run SOLRead! 

## Commands
 SOLRead defines three commands, `solread read`, `solread info` and `solread list`.
 A guide to these commands can be found by using `solread [command] --help`. 