# PCR Reaction Calculator

This repository contains two versions of the PCR Reaction Calculator:
1. A GUI version (`pcr_calculator_gui.py`) with a graphical interface
2. A CLI version (`pcr_calculator_cli.py`) for command-line usage, and user interactive.

## 🧬 Description

### GUI Version
The GUI version provides a graphical interface built using **Tkinter** for calculating PCR reaction volumes. Simply input the number of reactions and click calculate.

### CLI Version
The command-line version can be used in two ways:
1. With command-line argument: `python pcr_calculator_cli.py --value <number_of_reactions>`
2. Interactive mode: Run without arguments and enter the number when prompted

Both versions include a 10% safety factor for pipetting errors.

## 🧬 Usage Examples

### GUI Version
```bash
python pcr_calculator_gui.py
```

### CLI Version
With argument:
```bash
python pcr_calculator_cli.py --value 3
```

Interactive mode:
```bash
python pcr_calculator_cli.py
Enter number of reactions: 3
```

## 🧬 Description

This script provides a **PCR reaction calculator** — a common and repetitive task in many biology labs.  
Although calculating PCR mix volumes manually is quite simple, it can be much more efficient to have a platform that performs the calculation automatically instead of checking each component individually.  

In my own lab work, I usually use the same master mix for most reactions, but conceptually, this calculator could be extended to include different PCR mix types or reagent sets.

The GUI was built using **Tkinter** and allows the user to input the number of reactions they plan to run.  
The calculator then automatically computes the total volume for each reagent, including a 10% extra volume for pipetting error.

---

## ⚗️ Components and Ratios

| Component                 | Volume per reaction (µL) | Notes |
|----------------------------|--------------------------|-------|
| 2× Green Master Mix        | 7.5                      | Always half the final volume because this is a 2× concentration solution |
| Primer Forward (10 µM)     | 0.5                      | Final concentration 0.33 µM |
| Primer Reverse (10 µM)     | 0.5                      | Final concentration 0.33 µM |
| Template DNA               | 1.0                      | Depending on DNA concentration (usually 10–100 ng) |
| Water (ddH₂O / nuclease-free) | 5.5                  | To make up the total volume to 15 µL |

---

## 🧑‍💻 Code prompt used for generation

The following prompt was provided to GitHub Copilot / ChatGPT to generate the code.

First prompt:
```
Write code that uses the GUI to calculate volumes for a standard PCR reaction -
the function will calculate how much of each reagent should be added according to the following ratios:

Component | Volume (µL) | Notes
2× Green Master Mix - 7.5 µL . Always half the final volume because this is a 2× concentration solution
Primer Forward (10 µM) - 0.5 µL . Final concentration 0.33 µM
Primer Reverse (10 µM) - 0.5 µL . Final concentration 0.33 µM
Template DNA - 1 µL . Depending on the concentration of your DNA (usually 10–100 ng)
Water (ddH₂O / nuclease-free)- 5.5 µL . To make up the volume to 15 µL

https://www.thermofisher.com/order/catalog/product/K1081
```

Second prompt:
```
Please create the same pcr application without GUI.
You should get the input as command line argument --value, then print the results.
In case no arguemnt was recived, ask the user to enter input as input().
Also, update the read me with the new application.
```

Third prompt:
```
Please extract the common logic between those 2 files.
In one its inside calculate func, and anthoer with calculate_pcr_volumes

Name the new library pcr_calculator
```