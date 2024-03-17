import tkinter as tk
from tkinter import *
from tkinter import filedialog
import secrets
import random
from random import shuffle
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
        self.controller.show_frame(GenerateKeysApp)

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
            'rows': 1,
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

        self.create_table(1, 2, ['Password', 'Sequence'])
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
            'rows': 1,
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

        self.create_table(1, 3, ['Encrypted Password', 'Sequence', 'Salt']) # Change to 1 row as empty rows create an error
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

class GenerateKeysApp(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.configure(bg='#799F93')

        self.label_text = "Generate a sequence!"
        self.label = Label(self, text=self.label_text, font=('', 20, 'bold'), bg='#3A5048', fg='#BDD0CB', borderwidth=2, relief="raised", width=40)
        self.label.grid(row=0, column=0, columnspan=3, pady=10)

        # Create frame for valid characters so they can be packed into a single grid cell
        self.valid_char_frame_setup()

        # Create frame for Generate Set input values so they can be in a single grid cell
        self.generate_tab_frame = Frame(self, bg='#799F93')
        self.generate_tab_frame.grid(row=1, column=1, padx=10, pady=10, sticky="e")
        self.genTable = self.create_table(self.generate_tab_frame, 1, 2, ['Characters', 'Number of Sets'])

        self.randomize_tab_frame = Frame(self, bg='#799F93')
        self.randomize_tab_frame.grid(row=2, column=1, padx=10, pady=10, sticky="e")
        self.randTable = self.create_table(self.randomize_tab_frame, 1, 2, ['Sequences to be Generated', 'Amount of Keys to Use'])

        self.create_buttons()

    def create_buttons(self):
        generate_key_set = "Generate Key Set"
        self.generate_key_button = Button(self, text=generate_key_set, command=self.Generate_Button_Action, bg='#EA9A6A', width=20, height=10, borderwidth=4, relief="raised")
        self.generate_key_button.grid(row=1, column=2, padx=10, pady=10, sticky="e")

        randomize_sets = "Randomize Sets Into\nSequences"
        self.randomize_sets_button = Button(self, text=randomize_sets, command=self.Randomize_Button_Action, bg='#EA9A6A', width=20, height=10, borderwidth=4, relief="raised")
        self.randomize_sets_button.grid(row=2, column=2, padx=10, pady=10, sticky="e")

        refresh_button = "Refresh"
        self.other_button = Button(self, text=refresh_button, command=self.Refresh_Button_Action, bg='#EA9A6A', width=20, height=10, borderwidth=4, relief="raised")
        self.other_button.grid(row=3, column=2, padx=10, pady=10, sticky="e")

        main_page_redirect_button = "Return to main page"
        self.other_button = Button(self, text=main_page_redirect_button, command=lambda: self.controller.show_frame(MainHub), bg='#EA9A6A', width=20, height=10, borderwidth=4, relief="raised")
        self.other_button.grid(row=4, column=2, padx=10, pady=10, sticky="e")

    def Refresh_Button_Action(self):
        for widget in self.randomize_output_frame.winfo_children():
            widget.destroy()


    def Generate_Button_Action(self):
        input = self.get_table_info(self.genTable)
        charset = str(input[0])
        count = int(input[1])
        keySets = self.generate_keys(charset, count)
        
        csv_file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

        if csv_file_path:
            keySets.to_csv(csv_file_path)
        else:
            pass

    def Randomize_Button_Action(self):
        keySets = self.process_existing_keys()
        list = self.SequenceBreak(''.join(keySets))

        input = self.get_table_info(self.randTable)

        try:
            amt = int(input[0])     # Amount of sequences to be generated
            count = int(input[1])   # Amount of keys to be selected in each randomization

            randomizedList = self.randomize_created_keys(list, amt, count)

            self.randomize_output_frame = Frame(self, bg='#799F93')
            self.randomize_output_frame.grid(row=2, column=0, padx=10, pady=10, sticky="e")

            # Create a header for the table
            header_label = Label(self.randomize_output_frame, text='Sequences', font=('', 10), bg='#3A5048', fg='#BDD0CB', relief="raised")
            header_label.grid(row=0, column=0, pady=10, padx=1)

            # Iterate over randomizedList to populate the table
            for r, value in enumerate(randomizedList, start=1):
                label = Label(self.randomize_output_frame, text=value)
                label.grid(row=r, column=0, pady=1, padx=1, ipady=4)
            
            output = '\t\n'.join(randomizedList)

            copy_btn = Button(self.randomize_output_frame, text="Copy to Clipboard", command=lambda value=output: self.copy_to_clipboard(output))
            copy_btn.grid(row=0, column=1, pady=1, padx=30)

        except Exception as e:
            print("Error:", str(e))

    def valid_char_frame_setup(self):
        self.char_container = Frame(self, bg='#799F93')
        self.char_container.grid(row=1, column=0, padx=0, pady=(0, 10))

        self.valid_characters_label = Label(self.char_container, text="Valid Characters:", font=('', 12, 'bold'), bg='#BDD0CB', relief="raised")
        self.valid_characters_label.pack(side=TOP, fill=X)

        valid_characters = 'a b c d e f g h i j k l m\nn o p q r s t u v w x y z\nA B C D E F G H I J K L M\nN O P Q R S T U V W X Y Z'
        self.val_char_box = Text(self.char_container, bg='#BDD0CB', height=4, width=25)
        self.val_char_box.pack(side=BOTTOM, fill=X, pady=5)
        self.val_char_box.insert(tk.END, valid_characters)

    def copy_to_clipboard(self, text):
        self.clipboard_clear()  # Clear the clipboard
        self.clipboard_append(text)  # Append new text to the clipboard

    def create_table(self, root, rows, columns, head):
        table = []

        headers = head
        for c, header_text in enumerate(headers):
            header_label = Label(root, text=header_text, font=('', 10), bg='#3A5048', fg='#BDD0CB', relief="raised")
            header_label.grid(row=0, column=c, pady=10, padx=1)

        for r in range(1, rows + 1):
            row = []
            for c in range(columns):
                var = StringVar()
                entry = Entry(root, textvar=var)
                entry.grid(row=r, column=c, pady=1, padx=1, ipady=4)
                row.append(var)
            table.append(row)
        return table

    def get_table_info(self, table):
        row_items = []

        for r, row in enumerate(table):
            row_val = []
            for c, var in enumerate(row):
                value = var.get()
                row_val.append(value)
            row_items.append(row_val)

        return row_items[0]

    def process_existing_keys(self):
        keys_df = self.open_file_dialog()   # Prompts you to manually navigate to a CSV file to parse through for the keys
        if keys_df is not None:
            keySets = []
            for header in keys_df:
                keySets.append(header)
            return keySets
        else:
            # Handle the case where the CSV could not be loaded
            print("Error loading the CSV file.")

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
    def generate_keys(charSet, countPerChar):   # takes string, int
        charSet = ''.join(dict.fromkeys(charSet))   # Converts to dict to remove duplicates then converts back to string
        baseNumSet = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71]
        # ^Represents int versions of all legal characters allowed in the cypher
        
        keySets = []

        for char in charSet:
            keys = []
            for _ in range(countPerChar):
                shuffle(baseNumSet)
                new_key = tuple(baseNumSet)

                while new_key in keys:  # Checks if randomized key is unique and not apart of the keySets list. Continues to randomize until it's not
                    shuffle(baseNumSet)
                    new_key = tuple(baseNumSet)
                    
                keys.append(new_key)
            
            for i, key in enumerate(keys):
                columnName = char + str(i)
                keySets.append(pd.Series(key, name=columnName))

        keySets = pd.concat(keySets, axis=1)
        keySets.index = ['placeholder'] * len(keySets)
        keySets.index.name = 'placeholder'

        return keySets

    @staticmethod
    def randomize_created_keys(keySet, amount=1, count=None):   # Randomizes order of keys by count of keys used and amount of sequences created
        # ^keySet is the list of all keys in data frame
        sequenceSet = []

        if count is None:
            count = len(keySet)
        
        for seqSet in range(amount):   # For each sequence
            randomSequence = random.sample(keySet, count)
            random.shuffle(randomSequence)
            sequenceSet.append(''.join(randomSequence))
        
        return sequenceSet
    
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


class MainApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        geometry = self.geometry("700x500")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (GenerateKeysApp, MainHub, DecryptPage, EncryptPage):
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

