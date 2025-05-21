import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
from task import extract_ingredients_to_metta, recommend
from dotenv import load_dotenv

class RecipeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recipe Recommender")
        self.root.geometry("800x600")
        
        # Load environment variables
        load_dotenv()
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Recipe Recommender", font=('Helvetica', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Input section
        input_label = ttk.Label(main_frame, text="Enter ingredients you have (comma-separated):")
        input_label.grid(row=1, column=0, columnspan=2, pady=5, sticky=tk.W)
        
        self.input_text = ttk.Entry(main_frame, width=60)
        self.input_text.grid(row=2, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        
        # Submit button
        submit_button = ttk.Button(main_frame, text="Get Recommendations", command=self.get_recommendations)
        submit_button.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Results section
        results_label = ttk.Label(main_frame, text="Recommended Recipes:", font=('Helvetica', 12, 'bold'))
        results_label.grid(row=4, column=0, columnspan=2, pady=5, sticky=tk.W)
        
        # Results text area
        self.results_text = scrolledtext.ScrolledText(main_frame, width=70, height=20, wrap=tk.WORD)
        self.results_text.grid(row=5, column=0, columnspan=2, pady=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
    def get_recommendations(self):
        try:
            # Clear previous results
            self.results_text.delete(1.0, tk.END)
            
            # Get user input
            user_input = self.input_text.get().strip()
            if not user_input:
                messagebox.showwarning("Warning", "Please enter some ingredients!")
                return
            
            # Update status
            self.status_var.set("Processing...")
            self.root.update()
            
            # Extract ingredients
            ingredients = extract_ingredients_to_metta(user_input)
            
            # Display extracted ingredients
            self.results_text.insert(tk.END, f"Extracted ingredients: {ingredients}\n\n")
            
            # Get recommendations
            recommend(ingredients)
            
            # Update status
            self.status_var.set("Ready")
            
        except Exception as e:
            self.status_var.set("Error occurred")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.results_text.insert(tk.END, f"\nError: {str(e)}")

def main():
    root = tk.Tk()
    app = RecipeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 