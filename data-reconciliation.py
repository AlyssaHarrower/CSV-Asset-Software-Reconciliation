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
        self.upload1_btn = tk.Button(root, text="Upload Asset List CSV", command=self.load_csv1)
        self.upload1_btn.pack(pady=5)

        self.upload2_btn = tk.Button(root, text="Upload Software List CSV", command=self.load_csv2)
        self.upload2_btn.pack(pady=5)

        # Compare button
        self.compare_btn = tk.Button(root, text="Compare", command=self.compare_software, state=tk.DISABLED)
        self.compare_btn.pack(pady=10)

        # Text widget to display results
        self.result_text = tk.Text(root, height=20, width=80)
        self.result_text.pack(pady=10)

        self.df1 = None
        self.df2 = None
        self.asset_col_name = None

    # Asks to open file 1
    def load_csv1(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filepath:
            # Tries to read file
            try:
                self.df1 = pd.read_csv(filepath)
                self.label1.config(text=f"Asset List loaded: {filepath.split('/')[-1]}")
                self.enable_compare_if_ready()
            # If unable to read shows error message
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read Asset List:\n{e}")

    # Asks to open file 2
    def load_csv2(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filepath:
            # Tries to read file
            try:
                self.df2 = pd.read_csv(filepath)
                self.label2.config(text=f"Software List loaded: {filepath.split('/')[-1]}")
                self.enable_compare_if_ready()
            # If unable to read shows error message
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read Software List:\n{e}")

    # Enables compare button if both files are uploaded
    def enable_compare_if_ready(self):
        if self.df1 is not None and self.df2 is not None:
            self.compare_btn.config(state=tk.NORMAL)

    # Finds appropriate column names 
    def find_column_name(self, df, expected_name):
        for col in df.columns:
            if col.strip().lower() == expected_name.lower():
                return col
        return None

    # Finds Asset Column
    def find_asset_identifier_column(self, df):
        possible_names = ['asset name', 'asset', 'hostname', 'device', 'computer name']  # Contains all possible column names
        for name in possible_names:
            col = self.find_column_name(df, name) 
            if col:
                return col
        # If unable to find a column with the provided names it defaults to the first column
        return df.columns[0]

    # Compares software list
    def compare_software(self):
        # Find correct column names
        software_col_name = self.find_column_name(self.df1, 'Software')
        software_list_col_name = self.find_column_name(self.df2, 'Software List')
        self.asset_col_name = self.find_asset_identifier_column(self.df1)

        # Makes sure both required columns exist
        if not software_col_name or not software_list_col_name:
            messagebox.showerror("Missing Columns",
                                 "Ensure Asset List has a 'Software' column and Software List has a 'Software List' column.")
            return

        # Get all software list items from the software list CSV
        software_list_items = set(s.strip().lower() for s in self.df2[software_list_col_name].dropna())
        missing_rows = []

        # For each row in the asset list
        for _, row in self.df1.iterrows():
            # Get the software string and split it
            asset_software_set = set(s.strip().lower() for s in str(row[software_col_name]).split('/'))

            # Calculate what's missing
            missing_items = software_list_items - asset_software_set

            # If any items are missing, copy the row and note them
            if missing_items:
                new_row = row.copy()
                new_row['Missing Software'] = ' / '.join(sorted(missing_items))
                missing_rows.append(new_row)

        # Clear the result area
        self.result_text.delete(1.0, tk.END)

        # If there are missing items, display them and offer to save
        if missing_rows:
            self.result_text.insert(tk.END, "Assets with missing software:\n\n")
            for row in missing_rows:
                asset_identifier = row[self.asset_col_name]
                self.result_text.insert(tk.END, f"{asset_identifier}: {row['Missing Software']}\n")

            result_df = pd.DataFrame(missing_rows)
            result_df.drop(columns=[software_col_name], inplace=True)

            # Save the result
            save_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                     filetypes=[("CSV files", "*.csv")],
                                                     title="Save results as")
            if save_path:
                try:
                    result_df.to_csv(save_path, index=False)
                    self.result_text.insert(tk.END, f"\n\nSaved as: {save_path}")
                except Exception as e:
                    messagebox.showerror("Save Error", f"Failed to save CSV:\n{e}")
        else:
            self.result_text.insert(tk.END, "All assets contain the required software.")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = CSVComparerApp(root)
    root.mainloop()