import tkinter as tk
from tkinter import ttk
import numpy as np

class DataInputTable:
    def __init__(self, root):
        self.root = root
        self.root.title("Table Data Collector")

        # Entry variables
        self.entry_vars = []
        self.table_rows = ["Ambarlı", "Büyükçekmece", "Selimpaşa", "Silivri", "Çanta"]

        # Column labels
        column_labels = ["Çamur Yaşı", "Alfa", "SAE", "Düzeltilmiş AKM"]

        # Create a table with entry widgets using grid
        table_frame_grid = tk.Frame(root)
        table_frame_grid.grid(row=0, column=0, sticky="nsew")

        # Add column labels
        for col_idx, col_label in enumerate(column_labels, start=1):
            label = tk.Label(table_frame_grid, text=col_label, borderwidth=1, relief="solid", bg="lightgray", anchor="center")
            label.grid(row=0, column=col_idx, padx=10, pady=5, sticky="nsew")

        # Create a table with entry widgets using grid
        for row_idx, row_name in enumerate(self.table_rows, start=1):
            # Add row label
            row_label = tk.Label(table_frame_grid, text=row_name, borderwidth=1, relief="solid", bg="lightgray", anchor="w")
            row_label.grid(row=row_idx, column=0, padx=10, pady=5, sticky="nsew")

            # Add entry widgets for each column
            for col_idx, col_label in enumerate(column_labels, start=1):
                entry_var = tk.StringVar()
                self.entry_vars.append(entry_var)

                entry_entry = tk.Entry(table_frame_grid, textvariable=entry_var, borderwidth=1, relief="solid", bg="white", justify="center")
                entry_entry.grid(row=row_idx, column=col_idx, padx=10, pady=5, sticky="nsew")

        # Configure row and column weights
        for i in range(len(column_labels) + 1):
            table_frame_grid.grid_columnconfigure(i, weight=1)

        for i in range(len(self.table_rows) + 1):
            table_frame_grid.grid_rowconfigure(i, weight=1)

        # Create a submit button to collect data
        submit_button = tk.Button(root, text="Submit", command=self.collect_data)
        submit_button.grid(row=len(self.table_rows) + 1, column=0, columnspan=len(column_labels) + 1, pady=10, sticky="nsew")

        # Create a score table
        self.score_table = tk.Frame(root)
        self.score_table.grid(row=len(self.table_rows) + 2, column=0, columnspan=len(column_labels) + 2, pady=10, sticky="nsew")

        # Create a summary table
        self.summary_table = tk.Frame(root)
        self.summary_table.grid(row=len(self.table_rows) + 3, column=0, columnspan=len(column_labels) + 2, pady=10, sticky="nsew")

    def collect_data(self):
        collected_data = []
        for i, row_name in enumerate(self.table_rows):
            row_data = {"Row": row_name}
            for j, col_label in enumerate(["Çamur Yaşı", "Alfa", "SAE", "Düzeltilmiş AKM"]):
                value = float(self.entry_vars[i * len(["Çamur Yaşı", "Alfa", "SAE", "Düzeltilmiş AKM"]) + j].get())
                row_data[col_label] = value
            collected_data.append(row_data)

        # Calculate scores using linear approximation
        scores = self.calculate_scores(collected_data)

        # Display the collected data and scores in the score table
        self.display_scores(scores)

        # Display the collected data and scores in the summary table
        self.display_summary(scores)

        # Print the collected data and scores
        for row_data, score in zip(collected_data, scores):
            print(row_data, score)

    def calculate_scores(self, data):
        scores = {row_data['Row']: {} for row_data in data}
        for col_label in ["Çamur Yaşı", "Alfa", "SAE", "Düzeltilmiş AKM"]:
            values = {row_data['Row']: row_data[col_label] for row_data in data}
            min_value, max_value = min(values.values()), max(values.values())

            # Linear approximation
            scores_col = np.interp(list(values.values()), [min_value, max_value], [5, 10])

            for i, row_name in enumerate(self.table_rows):
                scores[row_name][col_label] = scores_col[i]

        return scores

    def display_scores(self, scores):
        # Create a score table header
        score_header = ["Tesis Adı"] + sum([[f"{col_label} Score", f"{col_label} Individual"] for col_label in ["Çamur Yaşı", "Alfa", "SAE", "Düzeltilmiş AKM"]], [])
        for col_idx, col_label in enumerate(score_header):
            label = tk.Label(self.score_table, text=col_label, borderwidth=1, relief="solid", bg="lightgray", anchor="center")
            label.grid(row=0, column=col_idx, padx=10, pady=5, sticky="nsew")

        # Display tesis adı and scores in the score table
        for i, row_name in enumerate(self.table_rows, start=1):
            # Tesis Adı
            tesis_adi_label = tk.Label(self.score_table, text=row_name, borderwidth=1, relief="solid", anchor="w")
            tesis_adi_label.grid(row=i, column=0, padx=10, pady=5, sticky="nsew")

            # Individual and Total scores
            for j, col_label in enumerate(["Çamur Yaşı", "Alfa", "SAE", "Düzeltilmiş AKM"]):
                score_label = tk.Label(self.score_table, text=f"{scores[row_name][col_label]:.2f}", borderwidth=1, relief="solid", anchor="center")
                score_label.grid(row=i, column=j * 2 + 1, padx=10, pady=5, sticky="nsew")

                individual_label = tk.Label(self.score_table, text=f"{scores[row_name][col_label]:.2f}", borderwidth=1, relief="solid", anchor="center")
                individual_label.grid(row=i, column=j * 2 + 2, padx=10, pady=5, sticky="nsew")

    def display_summary(self, scores):
        # Create a summary table header
        summary_header = ["Tesis Adı"] + ["Çamur Yaşı", "Alfa", "SAE", "Düzeltilmiş AKM"] + ["Toplam Puan"]
        for col_idx, col_label in enumerate(summary_header):
            label = tk.Label(self.summary_table, text=col_label, borderwidth=1, relief="solid", bg="lightgray", anchor="center")
            label.grid(row=0, column=col_idx, padx=10, pady=5, sticky="nsew")

        # Calculate total scores
        total_scores = {}
        for row_name in self.table_rows:
            total_scores[row_name] = sum(scores[row_name].values())

        # Order rows based on total score in descending order
        ordered_rows = sorted(self.table_rows, key=lambda row: total_scores[row], reverse=True)

        # Display tesis adı, individual scores, and total scores in the summary table
        for i, row_name in enumerate(ordered_rows, start=1):
            # Tesis Adı
            tesis_adi_label = tk.Label(self.summary_table, text=row_name, borderwidth=1, relief="solid", anchor="w")
            tesis_adi_label.grid(row=i, column=0, padx=10, pady=5, sticky="nsew")

            # Individual scores
            for j, col_label in enumerate(["Çamur Yaşı", "Alfa", "SAE", "Düzeltilmiş AKM"]):
                score_value = tk.Label(self.summary_table, text=f"{scores[row_name][col_label]:.2f}", borderwidth=1, relief="solid", anchor="center")
                score_value.grid(row=i, column=j + 1, padx=10, pady=5, sticky="nsew")

            # Total score
            total_score_label = tk.Label(self.summary_table, text=f"{total_scores[row_name]:.2f}", borderwidth=1, relief="solid", anchor="center")
            total_score_label.grid(row=i, column=len(column_labels) + 1, padx=10, pady=5, sticky="nsew")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataInputTable(root)
    root.mainloop()