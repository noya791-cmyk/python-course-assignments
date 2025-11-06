# PCR Reaction Calculator

This program creates a simple GUI (Graphical User Interface) for calculating the volumes of reagents required for a standard PCR reaction.

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

The following prompt was provided to GitHub Copilot / ChatGPT to generate the code:
Write code that uses the GUI to calculate volumes for a standard PCR reaction -
the function will calculate how much of each reagent should be added according to the following ratios:

Component | Volume (µL) | Notes
2× Green Master Mix | 7.5 µL | Always half the final volume because this is a 2× concentration solution
Primer Forward (10 µM) | 0.5 µL | Final concentration 0.33 µM
Primer Reverse (10 µM) | 0.5 µL | Final concentration 0.33 µM
Template DNA | 1 µL | Depending on the concentration of your DNA (usually 10–100 ng)
Water (ddH₂O / nuclease-free) | 5.5 µL | To make up the volume to 15 µL

