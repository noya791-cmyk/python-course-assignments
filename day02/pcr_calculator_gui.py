import tkinter as tk
from tkinter import ttk, messagebox
from pcr_calculator import PCRCalculator

class PCRCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PCR Reaction Calculator")
        self.root.geometry("600x700")
        
        # Set up the main frame with padding
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(self.main_frame, text="PCR Reaction Calculator", 
                                font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Preset selection
        ttk.Label(self.main_frame, text="Polymerase preset:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.preset_var = tk.StringVar(value="Green")
        preset_options = ["Green"] + list(PCRCalculator.PRESETS.keys())
        preset_combo = ttk.Combobox(self.main_frame, textvariable=self.preset_var, 
                                    values=preset_options, state="readonly")
        preset_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Number of reactions input
        ttk.Label(self.main_frame, text="Number of reactions:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.num_reactions = tk.StringVar(value="1")
        ttk.Entry(self.main_frame, textvariable=self.num_reactions).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Separator
        ttk.Separator(self.main_frame, orient="horizontal").grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Advanced options frame
        advanced_frame = ttk.LabelFrame(self.main_frame, text="Advanced Options", padding="10")
        advanced_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        advanced_frame.columnconfigure(1, weight=1)
        
        # Primer concentration
        ttk.Label(advanced_frame, text="Primer concentration (µM):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.primer_conc = tk.StringVar(value="")
        ttk.Entry(advanced_frame, textvariable=self.primer_conc).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Label(advanced_frame, text="(leave empty for preset default)", font=("Arial", 8)).grid(row=0, column=2, sticky=tk.W)
        
        # Reaction volume
        ttk.Label(advanced_frame, text="Total reaction volume (µL):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.reaction_vol = tk.StringVar(value="")
        ttk.Entry(advanced_frame, textvariable=self.reaction_vol).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Label(advanced_frame, text="(leave empty for preset default)", font=("Arial", 8)).grid(row=1, column=2, sticky=tk.W)
        
        # Template DNA calculation
        ttk.Label(advanced_frame, text="Template DNA (ng to add):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.template_ng = tk.StringVar(value="")
        ttk.Entry(advanced_frame, textvariable=self.template_ng).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Label(advanced_frame, text="(e.g., 50 ng)", font=("Arial", 8)).grid(row=2, column=2, sticky=tk.W)
        
        # Template DNA concentration
        ttk.Label(advanced_frame, text="Template DNA concentration (ng/µL):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.template_conc = tk.StringVar(value="")
        ttk.Entry(advanced_frame, textvariable=self.template_conc).grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Label(advanced_frame, text="(e.g., 100 ng/µL)", font=("Arial", 8)).grid(row=3, column=2, sticky=tk.W)
        
        # Separator
        ttk.Separator(self.main_frame, orient="horizontal").grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Create calculate button
        ttk.Button(self.main_frame, text="Calculate", command=self.calculate).grid(row=6, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        # Create results display area
        res_text = "Results (safety factor of 10% included):"
        self.results_frame = ttk.LabelFrame(self.main_frame, text=res_text, padding="10")
        self.results_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        self.results_frame.columnconfigure(1, weight=1)
        
        # Labels for results
        self.result_labels = {}
        result_components = ["Master Mix", "Primer Forward", "Primer Reverse", "Template DNA", "Water (ddH₂O)"]
        
        for i, component in enumerate(result_components):
            ttk.Label(self.results_frame, text=f"{component}:").grid(row=i, column=0, sticky=tk.W, pady=3)
            self.result_labels[component] = ttk.Label(self.results_frame, text="0.0 µL", font=("Arial", 10, "bold"))
            self.result_labels[component].grid(row=i, column=1, sticky=tk.E, pady=3)

    def calculate(self):
        try:
            # Get and validate num_reactions
            try:
                num_reactions = float(self.num_reactions.get())
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid number for reactions")
                return
            
            # Prepare kwargs for calculate_volumes
            kwargs = {"num_reactions": num_reactions}
            
            # Add preset if not default
            preset = self.preset_var.get()
            if preset != "Green":
                kwargs["preset"] = preset
            
            # Add optional parameters if provided
            if self.primer_conc.get().strip():
                try:
                    kwargs["primer_concentration"] = float(self.primer_conc.get())
                except ValueError:
                    messagebox.showerror("Input Error", "Primer concentration must be a number")
                    return
            
            if self.reaction_vol.get().strip():
                try:
                    kwargs["reaction_volume"] = float(self.reaction_vol.get())
                except ValueError:
                    messagebox.showerror("Input Error", "Reaction volume must be a number")
                    return
            
            if self.template_ng.get().strip():
                try:
                    kwargs["template_dna_ng"] = float(self.template_ng.get())
                except ValueError:
                    messagebox.showerror("Input Error", "Template DNA amount must be a number")
                    return
            
            if self.template_conc.get().strip():
                try:
                    kwargs["template_dna_concentration"] = float(self.template_conc.get())
                except ValueError:
                    messagebox.showerror("Input Error", "Template DNA concentration must be a number")
                    return
            
            # Call calculator
            volumes = PCRCalculator.calculate_volumes(**kwargs)
            
            # Update display
            for component in self.result_labels.keys():
                if component in volumes:
                    self.result_labels[component].config(text=f"{volumes[component]:.2f} µL")
        
        except ValueError as e:
            messagebox.showerror("Calculation Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

def main():
    root = tk.Tk()
    app = PCRCalculatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()