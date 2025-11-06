import tkinter as tk
from tkinter import ttk

class PCRCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("PCR Reaction Calculator")
        
        # Set up the main frame with padding
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create input field for number of reactions
        ttk.Label(self.main_frame, text="Number of reactions:").grid(row=0, column=0, sticky=tk.W)
        self.num_reactions = tk.StringVar(value="1")
        ttk.Entry(self.main_frame, textvariable=self.num_reactions).grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Create calculate button
        ttk.Button(self.main_frame, text="Calculate", command=self.calculate).grid(row=1, column=0, columnspan=2, pady=10)
        
        # Create results display area
        self.results_frame = ttk.LabelFrame(self.main_frame, text="Results", padding="10")
        self.results_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Labels for results
        self.components = [
            "2× Green Master Mix",
            "Primer Forward (10 µM)",
            "Primer Reverse (10 µM)",
            "Template DNA",
            "Water (ddH₂O)"
        ]
        
        self.result_labels = {}
        for i, component in enumerate(self.components):
            ttk.Label(self.results_frame, text=f"{component}:").grid(row=i, column=0, sticky=tk.W)
            self.result_labels[component] = ttk.Label(self.results_frame, text="0.0 µL")
            self.result_labels[component].grid(row=i, column=1, sticky=tk.E)

    def calculate(self):
        try:
            num_reactions = float(self.num_reactions.get())
            # Add 10% extra volume for pipetting errors
            safety_factor = 1.1
            
            # Base volumes per reaction
            volumes = {
                "2× Green Master Mix": 7.5,
                "Primer Forward (10 µM)": 0.5,
                "Primer Reverse (10 µM)": 0.5,
                "Template DNA": 1.0,
