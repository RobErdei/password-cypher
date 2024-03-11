import tkinter as tk
from tkinter import filedialog
import csv

class CSVReaderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CSV Reader App")
        self.geometry("400x200")

        self.label = tk.Label(self, text="Click here to select a CSV file")
        self.label.pack(pady=20)
        self.label.bind("<Button-1>", self.open_file_dialog)

    def open_file_dialog(self, event):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.read_csv(file_path)

    def read_csv(self, file_path):
        try:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                # Example: printing the content of the CSV file
                for row in reader:
                    print(row)
        except Exception as e:
            print("Error reading CSV:", str(e))

if __name__ == "__main__":
    app = CSVReaderApp()
    app.mainloop()
