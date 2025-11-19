"""
Protein Comparator GUI Application

User interface for comparing protein sequences between humans and zebrafish.
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
from business_logic import ProteinComparator


class ProteinComparatorApp:
    """Main GUI application for protein comparison."""
    
    def __init__(self, root):
        """
        Initialize the GUI application.
        
        Args:
            root: tkinter root window
        """
        self.root = root
        self.root.title("NCBI Protein Comparator")
        self.root.geometry("900x700")
        
        self.comparator = ProteinComparator()
        self.search_results = {}
        self.comparison_results = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface."""
        # Main container
        main_frame = tk.Frame(self.root, bg="#2B2D42", padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="NCBI Protein Comparator",
            font=("Helvetica", 16, "bold"),
            bg="#2B2D42",
            fg="#00D9FF"
        )
        title_label.pack(pady=10)
        
        # Input section
        input_frame = tk.Frame(main_frame, bg="#2B2D42")
        input_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            input_frame,
            text="Enter protein name:",
            font=("Helvetica", 10),
            bg="#2B2D42",
            fg="#00D9FF"
        ).pack(side=tk.LEFT, padx=5)
        
        self.protein_entry = tk.Entry(
            input_frame,
            font=("Helvetica", 10),
            width=30
        )
        self.protein_entry.pack(side=tk.LEFT, padx=5)
        self.protein_entry.bind('<Return>', lambda e: self.perform_search())
        
        search_button = tk.Button(
            input_frame,
            text="Search & Compare",
            command=self.perform_search,
            font=("Helvetica", 10),
            bg="#00D9FF",
            fg="#2B2D42",
            padx=10
        )
        search_button.pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = tk.Label(
            main_frame,
            text="Ready to search",
            font=("Helvetica", 9),
            bg="#2B2D42",
            fg="#FFD700"
        )
        self.status_label.pack(pady=5)
        
        # Results section
        results_label = tk.Label(
            main_frame,
            text="Results:",
            font=("Helvetica", 11, "bold"),
            bg="#2B2D42",
            fg="#00D9FF"
        )
        results_label.pack(anchor=tk.W, pady=(10, 5))
        
        # Results text area
        self.results_text = scrolledtext.ScrolledText(
            main_frame,
            height=20,
            width=100,
            font=("Courier", 9),
            bg="#1A1A2E",
            fg="#90EE90",
            insertbackground="#00D9FF"
        )
        self.results_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Configure text tags for results
        self.results_text.tag_config("header", foreground="#00D9FF", font=("Courier", 9, "bold"))
        self.results_text.tag_config("success", foreground="#90EE90")
        self.results_text.tag_config("error", foreground="#FF6B6B")
        self.results_text.tag_config("info", foreground="#87CEEB")
    
    def perform_search(self):
        """Perform protein search in background thread."""
        protein_name = self.protein_entry.get().strip()
        
        if not protein_name:
            messagebox.showwarning("Input Error", "Please enter a protein name")
            return
        
        self.status_label.config(text="Searching NCBI...", fg="#FFD700")
        self.results_text.delete(1.0, tk.END)
        
        # Run search in background thread
        thread = threading.Thread(
            target=self._search_worker,
            args=(protein_name,),
            daemon=True
        )
        thread.start()
    
    def _search_worker(self, protein_name):
        """Background worker for search."""
        try:
            organisms = ["Homo sapiens", "Danio rerio"]
            self.search_results = self.comparator.search_and_compare(
                protein_name,
                organisms
            )
            
            self.root.after(0, self.display_search_results, protein_name)
        
        except Exception as e:
            self.root.after(0, self.display_error, str(e))
    
    def display_search_results(self, protein_name):
        """Display search results."""
        self.results_text.delete(1.0, tk.END)
        
        self.results_text.insert(tk.END, f"Search Results for: {protein_name}\n", "header")
        self.results_text.insert(tk.END, "=" * 80 + "\n\n")
        
        human_data = self.search_results.get("Homo sapiens")
        zebrafish_data = self.search_results.get("Danio rerio")
        
        # Human results
        self.results_text.insert(tk.END, "HOMO SAPIENS (Human)\n", "header")
        if human_data:
            self.results_text.insert(tk.END, "Status: ", "info")
            self.results_text.insert(tk.END, "FOUND\n", "success")
            self.results_text.insert(tk.END, f"Accession: {human_data['accession']}\n", "info")
            self.results_text.insert(tk.END, f"Sequence Length: {human_data['length']} amino acids\n", "info")
            self.results_text.insert(tk.END, f"Title: {human_data['title']}\n", "info")
        else:
            self.results_text.insert(tk.END, "Status: ", "info")
            self.results_text.insert(tk.END, "NOT FOUND\n", "error")
        
        self.results_text.insert(tk.END, "\n" + "-" * 80 + "\n\n")
        
        # Zebrafish results
        self.results_text.insert(tk.END, "DANIO RERIO (Zebrafish)\n", "header")
        if zebrafish_data:
            self.results_text.insert(tk.END, "Status: ", "info")
            self.results_text.insert(tk.END, "FOUND\n", "success")
            self.results_text.insert(tk.END, f"Accession: {zebrafish_data['accession']}\n", "info")
            self.results_text.insert(tk.END, f"Sequence Length: {zebrafish_data['length']} amino acids\n", "info")
            self.results_text.insert(tk.END, f"Title: {zebrafish_data['title']}\n", "info")
        else:
            self.results_text.insert(tk.END, "Status: ", "info")
            self.results_text.insert(tk.END, "NOT FOUND\n", "error")
        
        # Comparison section
        if human_data and zebrafish_data:
            self.results_text.insert(tk.END, "\n" + "=" * 80 + "\n\n")
            self.perform_comparison(human_data, zebrafish_data)
        else:
            self.results_text.insert(tk.END, "\n" + "=" * 80 + "\n\n")
            self.results_text.insert(tk.END, "Note: ", "info")
            self.results_text.insert(
                tk.END,
                "Protein must be found in both organisms for comparison.\n",
                "error"
            )
            self.status_label.config(text="Search complete: Protein not found in both organisms", fg="#FF6B6B")
    
    def perform_comparison(self, human_data, zebrafish_data):
        """Perform sequence comparison."""
        self.status_label.config(text="Comparing sequences...", fg="#FFD700")
        
        thread = threading.Thread(
            target=self._comparison_worker,
            args=(human_data, zebrafish_data),
            daemon=True
        )
        thread.start()
    
    def _comparison_worker(self, human_data, zebrafish_data):
        """Background worker for comparison."""
        try:
            self.comparison_results = self.comparator.compare_sequences(
                human_data,
                zebrafish_data
            )
            self.root.after(0, self.display_comparison_results)
        
        except Exception as e:
            self.root.after(0, self.display_error, str(e))
    
    def display_comparison_results(self):
        """Display comparison results."""
        if not self.comparison_results:
            return
        
        results = self.comparison_results
        
        if 'error' in results:
            self.results_text.insert(tk.END, f"Error: {results['error']}\n", "error")
            return
        
        # Comparison header
        self.results_text.insert(tk.END, "SEQUENCE COMPARISON\n", "header")
        self.results_text.insert(tk.END, "-" * 80 + "\n\n")
        
        # Identity percentage
        identity = results['identity_percentage']
        self.results_text.insert(tk.END, "Identity Percentage: ", "info")
        self.results_text.insert(tk.END, f"{identity:.2f}%\n", "success")
        
        # Similarity ratio
        similarity = results['similarity_ratio']
        self.results_text.insert(tk.END, "Similarity Ratio: ", "info")
        self.results_text.insert(tk.END, f"{similarity:.4f}\n", "success")
        
        # Interpretation
        self.results_text.insert(tk.END, "\nInterpretation: ", "header")
        if identity > 80:
            interpretation = "HIGH similarity - Likely homologous proteins"
            color = "success"
        elif identity > 50:
            interpretation = "MODERATE similarity - Probable functional conservation"
            color = "info"
        else:
            interpretation = "LOW similarity - Distantly related proteins"
            color = "error"
        
        self.results_text.insert(tk.END, interpretation + "\n", color)
        
        # Sequence lengths
        self.results_text.insert(tk.END, "\n" + "-" * 80 + "\n\n")
        self.results_text.insert(tk.END, "Sequence Information:\n", "header")
        self.results_text.insert(
            tk.END,
            f"Human sequence length: {results['seq1']['length']} amino acids\n",
            "info"
        )
        self.results_text.insert(
            tk.END,
            f"Zebrafish sequence length: {results['seq2']['length']} amino acids\n",
            "info"
        )
        
        self.status_label.config(text="Comparison complete", fg="#90EE90")
    
    def display_error(self, error_message):
        """Display error message."""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "ERROR\n", "header")
        self.results_text.insert(tk.END, "=" * 80 + "\n\n")
        self.results_text.insert(tk.END, error_message + "\n", "error")
        self.status_label.config(text="Error occurred", fg="#FF6B6B")


def main():
    """Launch the GUI application."""
    root = tk.Tk()
    app = ProteinComparatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
