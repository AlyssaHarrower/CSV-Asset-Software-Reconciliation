import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

class CSVComparerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Data Reconciliation: Asset List + Software List")

        # Labels for file status
        self.label1 = tk.Label(root, text="Asset List with 'Software' Column: Not selected")
        self.label1.pack(pady=5)

        self.label2 = tk.Label(root, text="Software List: Not selected")
        self.label2.pack(pady=5)

        # Upload buttons
        self.upload1_btn = tk.Button(root, text="Upload CSV 1", command=self.load_csv1)
        self.upload1_btn.pack(pady=5)

        self.upload2_btn = tk.Button(root, text="Upload CSV 2", command=self.load_csv2)
        self.upload2_btn.pack(pady=5)

        # Compare button
        self.compare_btn = tk.Button(root, text="Compare", command=self.compare_software, state=tk.DISABLED)
        self.compare_btn.pack(pady=10)

        # Text widget to display results
        self.result_text = tk.Text(root, height=15, width=60)
        self.result_text.pack(pady=10)

        self.df1 = None
        self.df2 = None

    # Asks to open file and tries to read selected file
    def load_csv1(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filepath:
            try:
                self.df1 = pd.read_csv(filepath)
                self.label1.config(text=f"Asset List loaded: {filepath.split('/')[-1]}")
                self.enable_compare_if_ready()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read Asset List:\n{e}")

    def load_csv2(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filepath:
            try:
                self.df2 = pd.read_csv(filepath)
                self.label2.config(text=f"Software List loaded: {filepath.split('/')[-1]}")
                self.enable_compare_if_ready()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read CSV 2:\n{e}")

    # Enables compare button when both files are selected
    def enable_compare_if_ready(self):
        if self.df1 is not None and self.df2 is not None:
            self.compare_btn.config(state=tk.NORMAL)

    def compare_software(self):
        # Makes sure the selected files have the appropriate columns to compare
        if 'Software' not in self.df1.columns or 'Software List' not in self.df2.columns:
            messagebox.showerror("Missing Columns", "Ensure Asset List has 'Software' column and Software List has 'Software List' column.")
            return

        missing_rows = []

        # For each row in the Software column of Asset List
        for i, software_row in self.df1.iterrows():
            # Gets all software items from each row and parses on '/'
            software_items = set(s.strip().lower() for s in str(software_row['Software']).split('/'))
            
            # Get the entire 'Software List' column in Software List (as one combined set)
            software_list_items = set(s.strip().lower() for s in self.df2['Software List'].dropna())

            # Find missing items from the Software List
            missing_items = software_list_items - software_items

            # Adds all missing software items to list
            if missing_items:
                new_row = software_row.copy()
                new_row['Missing Software'] = ' / '.join(sorted(missing_items))
                missing_rows.append(new_row)

        # Update result text area
        self.result_text.delete(1.0, tk.END)
        if missing_rows:
            self.result_text.insert(tk.END, "Rows with missing software:\n\n")
            for row in missing_rows:
                self.result_text.insert(tk.END, f"- {row['Missing Software']}\n")

            # Save the result as a CSV
            result_df = pd.DataFrame(missing_rows)
            result_df.drop(columns=['Software'], inplace=True)
            try:
                result_df.to_csv('missing_software.csv', index=False)
                self.result_text.insert(tk.END, "\n\nSaved as: missing_software.csv")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save CSV:\n{e}")
        else:
            self.result_text.insert(tk.END, "All rows in Software contain the required Software List items.")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = CSVComparerApp(root)
    root.mainloop()
