import tkinter as tk
from tkinter import *
from tkinter import filedialog
import secrets
import random
import pandas as pd
from pathlib import Path
import csv
import logging 
from typing import Optional

class MainHub(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#799F93')

        self.label_text = "What would you like to do?"
        self.label = Label(self, text=self.label_text, font=('', 20, 'bold'), bg='#3A5048', fg='#BDD0CB', borderwidth=2, relief="raised", width=50, height=2)
        self.label.pack(padx=20, pady=20)

        encrypt_button_text = "Generate\nKeys"
        self.encrypt_button = Button(self, text=encrypt_button_text, font=('', 15), command=self.go_to_GenerateKeys, bg='#EA9A6A', width=25, height=5, borderwidth=4, relief="raised")
        self.encrypt_button.pack(side=LEFT, padx=25, pady=20)

        encrypt_button_text = "Encrypt"
        self.encrypt_button = Button(self, text=encrypt_button_text, font=('', 15), command=self.go_to_Encrypt, bg='#EA9A6A', width=25, height=5, borderwidth=4, relief="raised")
        self.encrypt_button.pack(side=LEFT, padx=25, pady=20)

        decrypt_button_text = "Decrypt"
        self.decrypt_button = Button(self, text=decrypt_button_text, font=('', 15), command=self.go_to_Decrypt, bg='#EA9A6A', width=25, height=5, borderwidth=4, relief="raised")
        self.decrypt_button.pack(side=RIGHT, padx=25, pady=20)


    def go_to_GenerateKeys(self):   # In progress
        pass

    def go_to_Decrypt(self):
        self.controller.show_frame(DecryptPage)

    def go_to_Encrypt(self):
        self.controller.show_frame(EncryptPage)

class EncryptPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.configure(bg='#799F93')

        # Initialize initial table structure
        self.initial_table_structure = {
            'rows': 2,
            'columns': 2,
            'headers': ['Password', 'Sequence']
        }

        self.label_text = "Enter your strings and their sequences"
        self.label = Label(self, text=self.label_text, font=('', 20, 'bold'), bg='#3A5048', fg='#BDD0CB', borderwidth=2, relief="raised", width=40)
        self.label.grid(row=0, column=0, columnspan=3, pady=10)

        self.content_frame = Frame(self, bg='#799F93')
        self.content_frame.grid(row=1, column=0, columnspan=2)

        self.export_to_csv_var = tk.IntVar()  # Create a tkinter variable to hold the state of the checkbox
        self.export_to_csv_checkbox = tk.Checkbutton(self.content_frame, text="Export to CSV", bg='#799F93', variable=self.export_to_csv_var, borderwidth=2, relief="sunken")
        self.export_to_csv_checkbox.grid(row=0, column=6, padx=10, pady=10, sticky="w")

        self.create_table(2, 2, ['Password', 'Sequence'])
        self.create_buttons()

    def on_visibility(self, visible):
        if visible:
            self.bind_all("<<Paste>>", self.paste)
        else:
            self.unbind_all("<<Paste>>")

    def create_table(self, rows, columns, head):
        self.table = []

        headers = head
        for c, header_text in enumerate(headers):
            header_label = Label(self.content_frame, text=header_text, font=('', 10), bg='#3A5048', fg='#BDD0CB', relief="raised")
            header_label.grid(row=0, column=c, pady=10, padx=1)

        for r in range(1, rows + 1):
            row = []
            for c in range(columns):
                if c == 0:
                    var = StringVar()
                    entry = Entry(self.content_frame, textvar=var, show="*")
                    entry.grid(row=r, column=c, pady=1, padx=1, ipady=4)
                    row.append(var)
                else:
                    var = StringVar()
                    entry = Entry(self.content_frame, textvar=var)
                    entry.grid(row=r, column=c, pady=1, padx=1, ipady=4)
                    row.append(var)
            self.table.append(row)

    def create_buttons(self):
        encrypt_button_text = "Encrypt"
        self.encrypt_button = Button(self, text=encrypt_button_text, command=self.process_data, bg='#EA9A6A', width=20, height=10, borderwidth=4, relief="raised")
        self.encrypt_button.grid(row=1, column=2, padx=10, pady=10, sticky="e")

        refresh_button = "Refresh"
        self.other_button = Button(self, text=refresh_button, command=self.reset_table, bg='#EA9A6A', width=20, height=10, borderwidth=4, relief="raised")
        self.other_button.grid(row=2, column=2, padx=10, pady=10, sticky="e")

        main_page_redirect_button = "Return to main page"
        self.other_button = Button(self, text=main_page_redirect_button, command=lambda: self.controller.show_frame(MainHub), bg='#EA9A6A', width=20, height=10, borderwidth=4, relief="raised")
        self.other_button.grid(row=3, column=2, padx=10, pady=10, sticky="e")

    def reset_table(self):
        # Clear the existing table content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        desired_width = 800
        desired_height = 650  
        
        root = self.controller
        root.geometry(f'{desired_width}x{desired_height}')

        # Recreate the table with the initial structure
        self.create_table(
            self.initial_table_structure['rows'],
            self.initial_table_structure['columns'],
            self.initial_table_structure['headers']
        )

        self.export_to_csv_var = tk.IntVar()  # Create a tkinter variable to hold the state of the checkbox
        self.export_to_csv_checkbox = tk.Checkbutton(self.content_frame, text="Export to CSV", bg='#799F93', variable=self.export_to_csv_var, borderwidth=2, relief="sunken")
        self.export_to_csv_checkbox.grid(row=0, column=6, padx=10, pady=10, sticky="w")

    def paste(self, event):
        # Access the clipboard from the widget that triggered the event
        widget = event.widget
        clipboard_data = widget.clipboard_get()

        if clipboard_data:
            rows = clipboard_data.strip().split('\n')
            columns = len(rows[0].split('\t')) if rows else 0

            # Expand the table vertically if needed

            if len(rows) > len(self.table):
                difference = len(rows) - len(self.table)

                for additionalRow in range(difference):
                    row = []

                    for column in range(columns):
                        #   Iterate based on the number of columns in the new data
                        if column == 0:
                            var = StringVar()
                            entry = Entry(self.content_frame, textvar=var, show="*")
                            entry.grid(row=len(self.table) + additionalRow + 1, column=column, pady=1, padx=1, ipady=4)
                            row.append(var)
                        else:
                            var = StringVar()
                            entry = Entry(self.content_frame, textvar=var)
                            entry.grid(row=len(self.table) + additionalRow + 1, column=column, pady=1, padx=1, ipady=4)
                            row.append(var)

                    self.table.append(row)


            for r, row in enumerate(rows):
                values = row.split('\t')
                for c, value in enumerate(values):
                    if r < len(self.table) and c < len(self.table[0]):
                        self.table[r][c].set(value)
                    else:
                        pass

    def get_table_info(self):
        row_items = []
        for r, row in enumerate(self.table):
            row_val = []
            for c, var in enumerate(row):
                value = var.get()
                row_val.append(value)
            row_items.append(row_val)
        return row_items

    def process_data(self):
        keys_df = self.open_file_dialog()   # Prompts you to manually navigate to a CSV file to parse through for the keys
        if keys_df is not None:
            encrypted_data = self.encrypt_data(keys_df)
            self.display_output(encrypted_data)
        else:
            # Handle the case where the CSV could not be loaded
            print("Error loading the CSV file.")

    def encrypt_data(self, keys_df):
        # Use keys_df directly in your encryption logic
        # Example:
        table_info = self.get_table_info()
        saltedPasswordsSet = []
        for i in table_info:
            origPas = i[0]
            saltedSet = self.addSalt(i[0])
            salt = saltedSet[0]
            saltedPas = saltedSet[1]

            sequences = self.SequenceBreak(i[1])
            newPas = ''
            for seq in sequences:
                encdPas = self.Encrypt(saltedPas, seq, keys_df)
                newPas = encdPas

            saltedPasswordsSet.append([newPas, ''.join(sequences), salt])

        return saltedPasswordsSet

    def display_output(self, output_data):
        # Clear the existing table
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        desired_width = 1060
        desired_height = 650  
        root = self.controller
        root.geometry(f'{desired_width}x{desired_height}')

        # Create new labels for the table headers
        headers = ['Encrypted Password', 'Key Set', 'Salt']
        for c, header_text in enumerate(headers):
            header_label = Label(self.content_frame, text=header_text, font=('', 10), bg='#3A5048', fg='#BDD0CB', relief="raised")
            header_label.grid(row=0, column=c, pady=10, padx=1)

        # Populate the table with output data
        for r, row_data in enumerate(output_data, start=1):
            for c, value in enumerate(row_data, start=0):
                if c < 2:  # Check if the current column is one of the first two columns
                    masked_value = '*' * len(value)  # Replace the actual value with asterisks
                    label = Label(self.content_frame, text=masked_value)
                else: 
                    label = Label(self.content_frame, text=value)
                label.grid(row=r, column=c, pady=1, padx=1, ipady=4)

        if self.export_to_csv_var.get():
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            # Write output data to CSV file
            with open(file_path, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(headers)
                csv_writer.writerows(output_data)

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            dataFrame = self.read_csv(file_path)
            return dataFrame

    def read_csv(self, file_path):
        try:
            with open(file_path, 'r') as file:
                read_file = pd.read_csv(file)
                read_file.drop(columns=read_file.columns[0])
                correctedReadFile = read_file.drop(columns=read_file.columns[0])
                return correctedReadFile
        except Exception as e:
            print("Error reading CSV:", str(e))


    @staticmethod
    def SequenceBreak(string):  #Breaks up key set sequence string | a1b64c8 to ['a1', 'b64', 'c8']
        result = []
        current = ''

        for char in string:
            if char.isalpha():  #If character is a letter
                if current:
                    result.append(current)      #Appends the current string in the queue to the result set as a key set
                    current = char              #Resets current queue
                else:
                    current += char
            else:
                current += char
        if current:
            result.append(current)

        return result
    
    @staticmethod
    def Encrypt(string, seq, setDF):
        DefaultCharSet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','!','@','#','$','%','^','&','*','?','~','0','1','2','3','4','5','6','7','8','9']
        encryptedString = ''

        for char in string:
            defaultNum = DefaultCharSet.index(char)

            set = setDF[seq].to_list()
            setNum = set[defaultNum]
            newChar = DefaultCharSet[setNum]
            encryptedString += str(newChar)

        string = encryptedString
        return string

    @staticmethod
    def addSalt(password, length=32):
        baseCharSet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*?~0123456789'

        for i in password:
            baseCharSet = baseCharSet.replace(i,'')

        legalCharacters = baseCharSet
        saltChars = [secrets.choice(legalCharacters) for i in range(length-len(password))]
        passwordCharacters = list(password)

        salt = ''.join(saltChars)
        newSet = []


        while passwordCharacters or saltChars:
            if passwordCharacters and (not saltChars or random.random() < 0.5):
                newSet.append(passwordCharacters.pop(0))
            else:
                newSet.append(saltChars.pop(0))

        return [salt, ''.join(newSet)]
    
class DecryptPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.configure(bg='#799F93')

        self.initial_table_structure = {
            'rows': 2,
            'columns': 3,
            'headers': ['Encrypted Password', 'Sequence', 'Salt']
        }

        self.label_text = "Enter your strings, their sequence and their salt"
        self.label = Label(self, text=self.label_text, font=('', 20, 'bold'), bg='#3A5048', fg='#BDD0CB', borderwidth=2, relief="raised", width=40)
        self.label.grid(row=0, column=0, columnspan=3, pady=10)

        self.content_frame = Frame(self, bg='#799F93')
        self.content_frame.grid(row=1, column=0, columnspan=2)

        self.export_to_csv_var = tk.IntVar()  # Create a tkinter variable to hold the state of the checkbox
        self.export_to_csv_checkbox = tk.Checkbutton(self.content_frame, text="Export to CSV", bg='#799F93', variable=self.export_to_csv_var, borderwidth=2, relief="sunken")
        self.export_to_csv_checkbox.grid(row=0, column=6, padx=10, pady=10, sticky="w")

        self.create_table(2, 3, ['Encrypted Password', 'Sequence', 'Salt'])
        self.create_buttons()

    def on_visibility(self, visible):
        if visible:
            self.bind_all("<<Paste>>", self.paste)
        else:
            self.unbind_all("<<Paste>>")

    def create_table(self, rows, columns, head):
        self.table = []

        headers = head
        for c, header_text in enumerate(headers):
            header_label = Label(self.content_frame, text=header_text, font=('', 10), bg='#3A5048', fg='#BDD0CB', relief="raised")
            header_label.grid(row=0, column=c, pady=10, padx=1)

        for r in range(1, rows + 1):
            row = []
            for c in range(columns):
                if c == 0:
                    var = StringVar()
                    entry = Entry(self.content_frame, textvar=var, show="*")
                    entry.grid(row=r, column=c, pady=1, padx=1, ipady=4)
                else:
                    var = StringVar()
                    entry = Entry(self.content_frame, textvar=var)
                    entry.grid(row=r, column=c, pady=1, padx=1, ipady=4)
                row.append(var)
            self.table.append(row)

    def reset_table(self):
        # Clear the existing table content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Recreate the table with the initial structure
        self.create_table(
            self.initial_table_structure['rows'],
            self.initial_table_structure['columns'],
            self.initial_table_structure['headers']
        )

        self.export_to_csv_var = tk.IntVar()  # Create a tkinter variable to hold the state of the checkbox
        self.export_to_csv_checkbox = tk.Checkbutton(self.content_frame, text="Export to CSV", bg='#799F93', variable=self.export_to_csv_var, borderwidth=2, relief="sunken")
        self.export_to_csv_checkbox.grid(row=0, column=6, padx=10, pady=10, sticky="w")

    def create_buttons(self):
        decrypt_button_text = "Decrypt"
        self.decrypt_button = Button(self, text=decrypt_button_text, command=self.process_data, bg='#EA9A6A', width=20, height=10, borderwidth=4, relief="raised")
        self.decrypt_button.grid(row=1, column=2, padx=10, pady=10, sticky="e")

        refresh_button = "Refresh"
        self.other_button = Button(self, text=refresh_button, command=self.reset_table, bg='#EA9A6A', width=20, height=10, borderwidth=4, relief="raised")
        self.other_button.grid(row=2, column=2, padx=10, pady=10, sticky="e")

        main_page_redirect_button = "Return to main page"
        self.other_button = Button(self, text=main_page_redirect_button, command=lambda: self.controller.show_frame(MainHub), bg='#EA9A6A', width=20, height=10, borderwidth=4, relief="raised")
        self.other_button.grid(row=3, column=2, padx=10, pady=10, sticky="e")

    def paste(self, event):
        # Access the clipboard from the widget that triggered the event
        widget = event.widget
        clipboard_data = widget.clipboard_get()

        if clipboard_data:
            rows = clipboard_data.strip().split('\n')
            columns = len(rows[0].split('\t')) if rows else 0

            # Expand the table vertically if needed

            if len(rows) > len(self.table):
                difference = len(rows) - len(self.table)

                for additionalRow in range(difference):
                    row = []

                    for column in range(columns):
                        # Iterate based on the number of columns in the new data
                        if column == 0:
                            var = StringVar()
                            entry = Entry(self.content_frame, textvar=var, show="*")
                            entry.grid(row=len(self.table) + additionalRow + 1, column=column, pady=1, padx=1, ipady=4)
                            row.append(var)
                        else:
                            var = StringVar()
                            entry = Entry(self.content_frame, textvar=var)
                            entry.grid(row=len(self.table) + additionalRow + 1, column=column, pady=1, padx=1, ipady=4)
                            row.append(var)

                    self.table.append(row)


            for r, row in enumerate(rows):
                values = row.split('\t')
                for c, value in enumerate(values):
                    if r < len(self.table) and c < len(self.table[0]):
                        self.table[r][c].set(value)
                    else:
                        pass

    def get_table_info(self):
        row_items = []
        for r, row in enumerate(self.table):
            row_val = []
            for c, var in enumerate(row):
                value = var.get()
                row_val.append(value)
            row_items.append(row_val)
        return row_items

    def process_data(self):
        keys_df = self.open_file_dialog()   # All keys availible to user
        if keys_df is not None:
            encrypted_data = self.decrypt_data(keys_df)     # Runs decrypt algorithm with the key sets as an argument
            self.display_output(encrypted_data)
        else:
            # Handle the case where the CSV could not be loaded
            print("Error loading the CSV file.")

    def decrypt_data(self, setDF):
        table_info = self.get_table_info()
        
        saltedPas = [i[0] for i in table_info]
        keySets = [i[1] for i in table_info]
        saltChars = [i[2] for i in table_info]

        DecryptedPasswordsSet = []
        for pas in range(len(saltedPas)):
            currentKeySet = keySets[pas]
            newPas = pas
            for key in self.SequenceBreak(currentKeySet):
                decrypted = self.Decrypt(saltedPas[pas], key, setDF)
                newPas = decrypted
            
            curSaltChars = saltChars[pas]
            pasWithoutSalt = self.removeSalt(newPas, curSaltChars)
        
            DecryptedPasswordsSet.append([currentKeySet, curSaltChars, pasWithoutSalt])
        return DecryptedPasswordsSet
        
    def display_output(self, output_data):
        # Clear the existing table
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Create new labels for the table headers
        headers = ['Sequence', ' Salt ', 'Decrypted Password']
        for c, header_text in enumerate(headers):
            header_label = Label(self.content_frame, text=header_text, font=('', 10), bg='#3A5048', fg='#BDD0CB', relief="raised")
            header_label.grid(row=0, column=c, pady=10, padx=1)

        # Populate the table with output data
        for r, row_data in enumerate(output_data, start=1):
            for c, value in enumerate(row_data, start=0):
                if c > 1:  # Check if the current column is one of the first two columns
                    masked_value = '*' * len(value)  # Replace the actual value with asterisks
                    label = Label(self.content_frame, text=masked_value)
                else: 
                    label = Label(self.content_frame, text=value)
                label.grid(row=r, column=c, pady=1, padx=1, ipady=4)

        
        if self.export_to_csv_var.get():
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            # Write output data to CSV file
            with open(file_path, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(headers)
                csv_writer.writerows(output_data)

    def open_file_dialog(self):     # Prompts user to choose csv that contains keys
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            dataFrame = self.read_csv(file_path)    # Parses through CSV chosen
            return dataFrame

    def read_csv(self, file_path):  # CSV dataframe, gets returned as pandas DF
        try:
            with open(file_path, 'r') as file:
                read_file = pd.read_csv(file)
                read_file.drop(columns=read_file.columns[0])    # First column should be placeholder. Gets dropped due to BOM character excel creates
                correctedReadFile = read_file.drop(columns=read_file.columns[0])
                return correctedReadFile
        except Exception as e:
            print("Error reading CSV:", str(e))


    @staticmethod
    def SequenceBreak(string):  #Breaks up key set sequence string | a1b64c8 to ['a1', 'b64', 'c8']
        result = []
        current = ''

        for char in string:
            if char.isalpha():  #If character is a letter
                if current:
                    result.append(current)      #Appends the current string in the queue to the result set as a key set
                    current = char              #Resets current queue
                else:
                    current += char
            else:
                current += char
        if current:
            result.append(current)

        return result

    @staticmethod
    def Decrypt(string, seq, setDF):
        DefaultCharSet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','!','@','#','$','%','^','&','*','?','~','0','1','2','3','4','5','6','7','8','9']
        decryptedString = ''

        for char in string:
            defaultNum = DefaultCharSet.index(char)
            set = setDF[seq].to_list()
            setNum = set.index(defaultNum)
            newChar = DefaultCharSet[setNum]
            decryptedString += str(newChar)

        string = decryptedString
        return string

    @staticmethod
    def removeSalt(saltedPassword, saltCharacters):
        unsaltedPassword = ''
        for i in saltedPassword:
            if i in saltCharacters:
                pass
            else:
                unsaltedPassword += i

        return unsaltedPassword

class MainApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        geometry = self.geometry("700x500")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MainHub, DecryptPage, EncryptPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainHub)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        if hasattr(frame, 'on_visibility'):
            frame.on_visibility(True)  # Assuming the frame is now visible
    
        # Update idletasks before resizing
        self.update_idletasks()
        
        # Calculate the required size
        required_width = frame.winfo_reqwidth()
        required_height = frame.winfo_reqheight()

        # Check if the frame is an instance of EncryptPage or DecryptPage
        if isinstance(frame, EncryptPage) or isinstance(frame, DecryptPage):
            # Apply specific logic for EncryptPage and DecryptPage
            # For example, setting a minimum width
            min_width = 800  # Define a minimum width
            if required_width < min_width:
                required_width = min_width

        self.geometry(f"{required_width}x{required_height}")


if __name__ == "__main__":
    app = MainApp()
    
    app.mainloop()

