import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
import numpy as np

class DataInputTable(QWidget):
    def __init__(self):
        super().__init__()

        self.table_rows = ["Ambarlı", "Büyükçekmece", "Selimpaşa", "Silivri", "Çanta"]
        self.column_labels = ["Çamur Yaşı", "Alfa", "SAE", "Düzeltilmiş AKM"]

        self.entry_widgets = []
        self.create_input_table()
        self.create_score_table()

        submit_button = QPushButton("Submit", self)
        submit_button.clicked.connect(self.collect_data)

        layout = QVBoxLayout()
        layout.addWidget(self.input_table)
        layout.addWidget(submit_button)
        layout.addWidget(self.score_table)

        self.setLayout(layout)
        self.setWindowTitle("Table Data Collector")

    def create_input_table(self):
        self.input_table = QTableWidget(len(self.table_rows), len(self.column_labels) + 1)
        self.input_table.setHorizontalHeaderLabels(["Tesis Adı"] + self.column_labels)

        for row_idx, row_name in enumerate(self.table_rows):
            item = QTableWidgetItem(row_name)
            item.setFlags(item.flags() ^ 2)  # Make the item non-editable
            self.input_table.setItem(row_idx, 0, item)

            for col_idx, _ in enumerate(self.column_labels, start=1):
                item = QTableWidgetItem()
                self.input_table.setItem(row_idx, col_idx, item)
                self.entry_widgets.append(item)

    def create_score_table(self):
        self.score_table = QTableWidget(len(self.table_rows), len(self.column_labels) + 2)
        self.score_table.setHorizontalHeaderLabels(["Tesis Adı"] + self.column_labels + ["Toplam Puan"])

        for row_idx, row_name in enumerate(self.table_rows):
            item = QTableWidgetItem(row_name)
            item.setFlags(item.flags() ^ 2)  # Make the item non-editable
            self.score_table.setItem(row_idx, 0, item)

    def collect_data(self):
        collected_data = []
        for row_idx, row_name in enumerate(self.table_rows):
            row_data = {"Row": row_name}
            for col_idx, col_label in enumerate(self.column_labels):
                text_value = self.entry_widgets[row_idx * len(self.column_labels) + col_idx].text()
                value = float(text_value) if text_value else 0.0
                row_data[col_label] = value
            collected_data.append(row_data)

        # Calculate scores using linear approximation
        scores = self.calculate_scores(collected_data)

        # Display the collected data and scores in the score table
        self.display_scores(scores)

        # Print the collected data and scores
        for row_data, score in zip(collected_data, scores):
            print(row_data, score)

    def calculate_scores(self, data):
        scores = {row_data['Row']: {} for row_data in data}
        for col_label in self.column_labels:
            values = {row_data['Row']: row_data[col_label] for row_data in data}
            min_value, max_value = min(values.values()), max(values.values())

            # Linear approximation
            if col_label == "Çamur Yaşı" or col_label == "Düzeltilmiş AKM":
                scores_col = np.interp(list(values.values()), [min_value, max_value], [10, 5])
            else:
                scores_col = np.interp(list(values.values()), [min_value, max_value], [5, 10])

            for i, row_name in enumerate(self.table_rows):
                scores[row_name][col_label] = scores_col[i]

        return scores

    def display_scores(self, scores):
        # Calculate total scores
        total_scores = {row_name: sum(scores[row_name].values()) for row_name in self.table_rows}

        # Order rows based on total score in descending order
        ordered_rows = sorted(self.table_rows, key=lambda row: total_scores[row], reverse=True)

        for i, row_name in enumerate(ordered_rows):
            # Tesis Adı
            item = QTableWidgetItem(row_name)
            item.setFlags(item.flags() ^ 2)  # Make the item non-editable
            self.score_table.setItem(i, 0, item)

            # Individual scores
            for j, col_label in enumerate(self.column_labels):
                score_item = QTableWidgetItem(f"{scores[row_name][col_label]:.2f}")
                score_item.setFlags(score_item.flags() ^ 2)  # Make the item non-editable
                self.score_table.setItem(i, j + 1, score_item)

            # Total score
            total_score_item = QTableWidgetItem(f"{total_scores[row_name]:.2f}")
            total_score_item.setFlags(total_score_item.flags() ^ 2)  # Make the item non-editable
            self.score_table.setItem(i, len(self.column_labels) + 1, total_score_item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DataInputTable()
    window.show()
    sys.exit(app.exec_())
