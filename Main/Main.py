import tkinter as tk
from tkinter import Label, Button, Entry, StringVar, IntVar, Checkbutton, Text, filedialog, Frame, messagebox, TOP, BOTTOM, LEFT, RIGHT, X

import secrets
import random
from random import shuffle
import pandas as pd
from pathlib import Path
import csv
import logging 
from typing import Optional

# Standard color scheme for entire app
colorScheme = {
    'Table Header Color' : ['#F8A87C'],
    'Label Color' : ['#FAA312'],
    'Background' : ['#12213E'],
    'Button Color' : ['#8FCAE4'],
    'Checkmark Foreground' : ['#33C481'],

    'Valid Characters Table' : ['#E9D7A9'],

    'Text Color' : ['black'],
    'Text Font' : ['Consolas']
}

# Standard button criteria for entire app
buttonCriteria = {
    "Per-app Size" : [18, 9],    #width, height
    "Per-app Font Size" : [10],

    "Main Hub Size" : [25, 5],
    "Main Hub Font Size" : [15],
}

class MainHub(tk.Frame):    # Serves as a launch point for all main functionalities of the app
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=colorScheme['Background'])

        self.label_text = "What Would You Like To Do?"
        self.label = Label(self, text=self.label_text, font=(colorScheme['Text Font'], 20, 'bold'), bg=colorScheme['Label Color'], fg=colorScheme['Background'], borderwidth=2, relief="solid", width=50, height=2)
        self.label.pack(padx=20, pady=20)

        encrypt_button_text = "Generate\nKeys"
        self.encrypt_button = Button(self, text=encrypt_button_text, font=(colorScheme['Text Font'], buttonCriteria['Main Hub Font Size'], 'bold'), command=self.go_to_GenerateKeys, bg=colorScheme['Button Color'], width=buttonCriteria['Main Hub Size'][0], height=buttonCriteria['Main Hub Size'][1], borderwidth=4, relief="raised")
        self.encrypt_button.pack(side=LEFT, padx=25, pady=20)

        encrypt_button_text = "Encrypt"
        self.encrypt_button = Button(self, text=encrypt_button_text, font=(colorScheme['Text Font'], buttonCriteria['Main Hub Font Size'], 'bold'), command=self.go_to_Encrypt, bg=colorScheme['Button Color'], width=buttonCriteria['Main Hub Size'][0], height=buttonCriteria['Main Hub Size'][1], borderwidth=4, relief="raised")
        self.encrypt_button.pack(side=LEFT, padx=25, pady=20)

        decrypt_button_text = "Decrypt"
        self.decrypt_button = Button(self, text=decrypt_button_text, font=(colorScheme['Text Font'], buttonCriteria['Main Hub Font Size'], 'bold'), command=self.go_to_Decrypt, bg=colorScheme['Button Color'], width=buttonCriteria['Main Hub Size'][0], height=buttonCriteria['Main Hub Size'][1], borderwidth=4, relief="raised")
        self.decrypt_button.pack(side=RIGHT, padx=25, pady=20)

    def go_to_GenerateKeys(self):
        self.controller.show_frame(GenerateKeysApp)

    def go_to_Decrypt(self):
        self.controller.show_frame(DecryptPage)

    def go_to_Encrypt(self):
        self.controller.show_frame(EncryptPage)

class EncryptPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.configure(bg=colorScheme['Background'])

        self.base_window()

    def base_window(self):  # Creates base instance of page that can be reverted to as needed
        # Static frame for fixed button location
        self.static_frame = tk.Frame(self, bg=colorScheme['Background'])
        self.static_frame.pack(side='right', fill='x', pady=(10, 0))

        # Dynamic frame for variable table sizing and similar non-rigid object
        self.dynamic_frame = tk.Frame(self, bg=colorScheme['Background'])
        self.dynamic_frame.pack(side='top', fill='both', expand=True)

        # Initialize input table structure
        self.initial_table_structure = {
            'rows': 1,
            'columns': 2,
            'headers': ['Password', 'Sequence']
        }

        self.label_text = "Enter Your Strings and Sequences"
        self.label = Label(self.dynamic_frame, text=self.label_text, font=(colorScheme['Text Font'], 20, 'bold'), bg=colorScheme['Label Color'], fg=colorScheme['Background'], borderwidth=2, relief="raised", width=40)
        self.label.grid(row=0, column=0, columnspan=3, pady=10)

        self.content_frame = Frame(self.dynamic_frame, bg=colorScheme['Background'])    # Establishes the grid the input table is in
        self.content_frame.grid(row=1, column=0, columnspan=2)

        self.export_to_csv_var = tk.IntVar()  # Create a tkinter variable to hold the state of the checkbox. Set in the same grid as the input table
        self.export_to_csv_checkbox = tk.Checkbutton(self.content_frame, text="Export to CSV", font=(colorScheme['Text Font'], 12), bg=colorScheme['Checkmark Foreground'], variable=self.export_to_csv_var, borderwidth=2, relief='raised')
        self.export_to_csv_checkbox.grid(row=0, column=6, padx=10, pady=10, sticky="w")

        self.create_table(1, 2, ['Password', 'Sequence'])
        self.create_buttons()

    def on_visibility(self, visible):   # Binds the paste event to the paste function in the clase
        if visible:
            self.bind_all("<<Paste>>", self.paste)
        else:
            self.unbind_all("<<Paste>>")

    def create_table(self, rows, columns, head):    # Create Table based off of amount of rows and columns and list of headers
        self.table = []

        headers = head
        for c, header_text in enumerate(headers):
            header_label = Label(self.content_frame, width=buttonCriteria['Per-app Size'][0], text=header_text, font=(colorScheme['Text Font'], 12), bg=colorScheme['Table Header Color'], fg=colorScheme['Text Color'], relief="raised")
            header_label.grid(row=0, column=c, pady=10, padx=10)

        for r in range(1, rows + 1):
            row = []
            for c in range(columns):
                if c == 0:
                    var = StringVar()
                    entry = Entry(self.content_frame, textvar=var, show="*")    # The first column in this class's table will contain sensitive information and thus will be hidden visually.
                    entry.grid(row=r, column=c, pady=1, padx=1, ipady=4)
                    row.append(var)
                else:
                    var = StringVar()
                    entry = Entry(self.content_frame, textvar=var)
                    entry.grid(row=r, column=c, pady=1, padx=1, ipady=4)
                    row.append(var)
            self.table.append(row)

    def create_buttons(self):   # Create all buttons used for page
        encrypt_button_text = "Encrypt"
        self.encrypt_button = Button(self.static_frame, text=encrypt_button_text, font=(colorScheme['Text Color'], buttonCriteria['Per-app Font Size'], 'bold'), command=self.process_data, bg=colorScheme['Button Color'], width=buttonCriteria['Per-app Size'][0], height=buttonCriteria['Per-app Size'][1], borderwidth=4, relief="raised")
        self.encrypt_button.grid(row=1, column=2, padx=10, pady=10, sticky="e")

        refresh_button = "Refresh"
        self.other_button = Button(self.static_frame, text=refresh_button, font=(colorScheme['Text Color'], buttonCriteria['Per-app Font Size'], 'bold'), command=self.reset_table, bg=colorScheme['Button Color'], width=buttonCriteria['Per-app Size'][0], height=buttonCriteria['Per-app Size'][1], borderwidth=4, relief="raised")
        self.other_button.grid(row=2, column=2, padx=10, pady=10, sticky="e")

        main_page_redirect_button = "Return to\nMain Page"
        self.other_button = Button(self.static_frame, text=main_page_redirect_button, font=(colorScheme['Text Color'], buttonCriteria['Per-app Font Size'], 'bold'), command=lambda: self.controller.show_frame(MainHub), bg=colorScheme['Button Color'], width=buttonCriteria['Per-app Size'][0], height=buttonCriteria['Per-app Size'][1], borderwidth=4, relief="raised")
        self.other_button.grid(row=3, column=2, padx=10, pady=10, sticky="e")

    def reset_table(self):  # Destroy current page and rebuild the base window setup
        # Clear the existing table content
        for widget in self.winfo_children():
            widget.destroy()

        self.base_window()

    def paste(self, event): # Access the clipboard from the widget that triggered the "Paste" event
        widget = event.widget
        clipboard_data = widget.clipboard_get()

        if clipboard_data:
            rows = clipboard_data.strip().split('\n')
            columns = len(rows[0].split('\t')) if rows else 0   # Assumes your clipboard was coppied straight from an Excel grid and seperates cell contents
            if len(rows) > len(self.table): # Expands the table vertically if clipboard contents require it
                difference = len(rows) - len(self.table)
                for additionalRow in range(difference):
                    row = []
                    for column in range(columns):
                        if column == 0:
                            var = StringVar()
                            entry = Entry(self.content_frame, textvar=var, show="*")    # The first column in this class's table will contain sensitive information and thus will be hidden visually.
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

    def get_table_info(self):   # Retrieve data entered in input table
        row_items = []
        for r, row in enumerate(self.table):
            row_val = []
            for c, var in enumerate(row):
                value = var.get()
                row_val.append(value)
            row_items.append(row_val)
        return row_items

    def process_data(self): # The process that occurs when the "Encrypt" button is clicked
        keys_df = self.open_file_dialog()   # Prompts you to manually navigate to a CSV file for the key sets
        if keys_df is not None:
            encrypted_data = self.encrypt_data(keys_df) # Runs the encrypt algorithm with key sets as argument
            self.display_output(encrypted_data)
        else:
            # Handles the case where the CSV could not be loaded
            print("Error loading the CSV file.")

    def encrypt_data(self, keys_df):    # Salts password, splits sequence into key sets and encrypts through those keys
        table_info = self.get_table_info()
        saltedPasswordsSet = []
        for i in table_info:
            origPas = i[0]
            saltedSet = self.addSalt(i[0])  # Calls static function where salt is randomly added to string
            salt = saltedSet[0]
            saltedPas = saltedSet[1]

            sequences = self.SequenceBreak(i[1])    # Calls static function to seperate the inputted sequences
            newPas = ''
            for seq in sequences:
                encdPas = self.Encrypt(saltedPas, seq, keys_df) # Calls the encryption algorithm for selected string, keys set header and keys
                newPas = encdPas

            saltedPasswordsSet.append([newPas, ''.join(sequences), salt])

        return saltedPasswordsSet

    def copy_to_clipboard(self, text):
        self.clipboard_clear()  # Clear the clipboard
        self.clipboard_append(text)  # Append the text to the clipboard
        self.update()

    def display_output(self, output_data):
        # Clear the existing table
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Create new labels for the table headers
        headers = ['Encrypted Password', 'Key Set', 'Salt']
        for c, header_text in enumerate(headers):
            header_label = Label(self.content_frame, width=buttonCriteria['Per-app Size'][0], text=header_text, font=(colorScheme['Text Font'], 12), bg=colorScheme['Table Header Color'], fg=colorScheme['Text Color'], relief="raised")
            header_label.grid(row=0, column=c, pady=10, padx=1)

        # Populate the table with output data
        for r, row_data in enumerate(output_data, start=1):
            for c, value in enumerate(row_data, start=0):
                label = Label(self.content_frame, width=buttonCriteria['Per-app Size'][0], text=value)
                label.grid(row=r, column=c, pady=1, padx=1, ipady=4)

            # Prepares row data as a string for copying
            row_data_str = "\t".join(map(str, row_data))  # Joined with a tab character for Excel compatibility

            # Creates buttons for each row allowing you to copy the password of specific rows
            copy_button = Button(self.content_frame, text="Copy", command=lambda value=row_data_str: self.copy_to_clipboard(value))
            copy_button.grid(row=r, column=len(row_data), pady=1, padx=1)

        if self.export_to_csv_var.get():
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            # Write output data to CSV file
            with open(file_path, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(headers)
                csv_writer.writerows(output_data)

    def open_file_dialog(self): # Promts user to navigate to location of CSV
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            dataFrame = self.read_csv(file_path)
            return dataFrame

    def read_csv(self, file_path):  # Reads CSV
        try:
            with open(file_path, 'r') as file:
                read_file = pd.read_csv(file)
                correctedReadFile = read_file.drop(columns=read_file.columns[0]) # Drops first column (a dummy column) due to excel's encoding causing issues with the import. 
                return correctedReadFile
        except Exception as e:
            print("Error reading CSV:", str(e))


    @staticmethod
    def SequenceBreak(string):  # Breaks up sequence string into key set headers
        result = []
        current = ''

        for char in string:
            if char.isalpha():  # Checks if character is a letter
                if current:
                    result.append(current)      # Appends the current string in the queue to the result set as a key set
                    current = char              # Resets current queue
                else:
                    current += char
            else:
                current += char
        if current:
            result.append(current)
            
        return result
    
    @staticmethod
    def Encrypt(string, seq, setDF):    # The encryption algorithm
        # Defines base set of allowable characters as DefaultCharSet
        DefaultCharSet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','!','@','#','$','%','^','&','*','?','~','0','1','2','3','4','5','6','7','8','9']
        encryptedString = ''

        for char in string:
            defaultNum = DefaultCharSet.index(char) # Get position in defalt set
            set = setDF[seq].to_list()              # Get list of keys using the necessary header
            setNum = set[defaultNum]                # Get integer value in key set of the positional defaultNum function
            newChar = DefaultCharSet[setNum]        # Get character in default set using the new integer as position
            encryptedString += str(newChar)

        string = encryptedString
        return string

    @staticmethod
    def addSalt(password, length=32):   # Add valid characters to random locations in the password string
        baseCharSet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*?~0123456789'

        for i in password:
            baseCharSet = baseCharSet.replace(i,'')
        legalCharacters = baseCharSet
        saltChars = [secrets.choice(legalCharacters) for i in range(length-len(password))]  # Randomly select valid characters not in password until max string length (32) is reached
        passwordCharacters = list(password)
        salt = ''.join(saltChars)   #   String of characters to be salted into password
        newSet = []

        while passwordCharacters or saltChars:
            random.shuffle(saltChars)   # Randomize order of salt character set
            if passwordCharacters and (not saltChars or random.random() < 0.5): # Alternates randomly between adding a password character or a salt character to the empty set
                newSet.append(passwordCharacters.pop(0))
            else:
                newSet.append(saltChars.pop(0))

        return [salt, ''.join(newSet)]
    
class DecryptPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.configure(bg=colorScheme['Background'])

        

        self.base_window()

    def base_window(self):  # Creates base instance of page that can be reverted to as needed
        # Static frame for fixed button location
        self.static_frame = tk.Frame(self, bg=colorScheme['Background'])
        self.static_frame.pack(side='right', fill='x', pady=(10, 0))

        # Dynamic frame for variable table sizing and similar non-rigid object
        self.dynamic_frame = tk.Frame(self, bg=colorScheme['Background'])
        self.dynamic_frame.pack(side='top', fill='both', expand=True)

        # Initialize input table structure
        self.initial_table_structure = {
            'rows': 1,
            'columns': 3,
            'headers': ['Encrypted Password', 'Sequence', 'Salt']
        }

        self.label_text = "Enter Your Strings, Sequence and Salt"
        self.label = Label(self.dynamic_frame, text=self.label_text, font=(colorScheme['Text Font'], 20, 'bold'), bg=colorScheme['Label Color'], fg=colorScheme['Background'], borderwidth=2, relief="raised", width=50)
        self.label.grid(row=0, column=0, columnspan=3, pady=10)

        self.content_frame = Frame(self.dynamic_frame, bg=colorScheme['Background'])
        self.content_frame.grid(row=1, column=0, columnspan=2)  # Establishes the grid the input table is in

        self.export_to_csv_var = tk.IntVar()  # Create a tkinter variable to hold the state of the checkbox
        self.export_to_csv_checkbox = tk.Checkbutton(self.content_frame, text="Export to CSV", font=(colorScheme['Text Font'], 12), bg=colorScheme['Checkmark Foreground'], variable=self.export_to_csv_var, borderwidth=2, relief='raised')
        self.export_to_csv_checkbox.grid(row=0, column=6, padx=10, pady=10, sticky="w")

        self.create_table(1, 3, ['Encrypted Password', 'Sequence', 'Salt']) # Change to 1 row as empty rows create an error
        self.create_buttons()

    def on_visibility(self, visible):   # Binds the paste event to the paste function in the clase
        if visible:
            self.bind_all("<<Paste>>", self.paste)
        else:
            self.unbind_all("<<Paste>>")

    def create_table(self, rows, columns, head):    # Create Table based off of amount of rows and columns and list of headers
        self.table = []

        headers = head
        for c, header_text in enumerate(headers):
            header_label = Label(self.content_frame, width=buttonCriteria['Per-app Size'][0], text=header_text, font=(colorScheme['Text Font'], 12), bg=colorScheme['Table Header Color'], fg=colorScheme['Text Color'], relief="raised")
            header_label.grid(row=0, column=c, pady=10, padx=10)

        for r in range(1, rows + 1):
            row = []
            for c in range(columns):
                if c == 0:
                    var = StringVar()
                    entry = Entry(self.content_frame, textvar=var, show="*")    # The first column in this class's table will contain sensitive information and thus will be hidden visually.
                    entry.grid(row=r, column=c, pady=1, padx=1, ipady=4)
                else:
                    var = StringVar()
                    entry = Entry(self.content_frame, textvar=var)
                    entry.grid(row=r, column=c, pady=1, padx=1, ipady=4)
                row.append(var)
            self.table.append(row)

    def reset_window(self): # Destroy current page and rebuild the base window setup
        for widget in self.winfo_children():
            widget.destroy()
        
        self.base_window()

    def create_buttons(self):   # Create all buttons used for page
        decrypt_button_text = "Decrypt"
        self.decrypt_button = Button(self.static_frame, text=decrypt_button_text, font=(colorScheme['Text Color'], buttonCriteria['Per-app Font Size'], 'bold'), command=self.process_data, bg=colorScheme['Button Color'], width=buttonCriteria['Per-app Size'][0], height=buttonCriteria['Per-app Size'][1], borderwidth=4, relief="raised")
        self.decrypt_button.grid(row=1, column=2, padx=10, pady=10, sticky="e")

        refresh_button = "Refresh"
        self.other_button = Button(self.static_frame, text=refresh_button, font=(colorScheme['Text Color'], buttonCriteria['Per-app Font Size'], 'bold'), command=self.reset_window, bg=colorScheme['Button Color'], width=buttonCriteria['Per-app Size'][0], height=buttonCriteria['Per-app Size'][1], borderwidth=4, relief="raised")
        self.other_button.grid(row=2, column=2, padx=10, pady=10, sticky="e")

        main_page_redirect_button = "Return to\nMain Page"
        self.other_button = Button(self.static_frame, text=main_page_redirect_button, font=(colorScheme['Text Color'], buttonCriteria['Per-app Font Size'], 'bold'), command=lambda: self.controller.show_frame(MainHub), bg=colorScheme['Button Color'], width=buttonCriteria['Per-app Size'][0], height=buttonCriteria['Per-app Size'][1], borderwidth=4, relief="raised")
        self.other_button.grid(row=3, column=2, padx=10, pady=10, sticky="e")

    def paste(self, event): # Access the clipboard from the widget that triggered the "Paste" event
        widget = event.widget
        clipboard_data = widget.clipboard_get()

        if clipboard_data:
            rows = clipboard_data.strip().split('\n')
            columns = len(rows[0].split('\t')) if rows else 0   # Assumes your clipboard was coppied straight from an Excel grid and seperates cell contents
            if len(rows) > len(self.table): # Expands the table vertically if needed
                difference = len(rows) - len(self.table)
                for additionalRow in range(difference):
                    row = []
                    for column in range(columns):
                        if column == 0:
                            var = StringVar()
                            entry = Entry(self.content_frame, textvar=var, show="*")    # The first column in this class's table will contain sensitive information and thus will be hidden visually.
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

    def get_table_info(self):   # Retrieve data entered in input table
        row_items = []
        for r, row in enumerate(self.table):
            row_val = []
            for c, var in enumerate(row):
                value = var.get()
                row_val.append(value)
            row_items.append(row_val)
        return row_items

    def process_data(self): # The process that occurs when the "Encrypt" button is clicked
        keys_df = self.open_file_dialog()   # Prompts you to manually navigate to a CSV file for the key sets
        if keys_df is not None:
            encrypted_data = self.decrypt_data(keys_df)     # Runs decrypt algorithm with the key sets as an argument
            self.display_output(encrypted_data)
        else:
            # Handles the case where the CSV could not be loaded
            print("Error loading the CSV file.")

    def decrypt_data(self, setDF):  # Decrypts password using key sets and removes salt characters
        table_info = self.get_table_info()
        
        saltedPas = [i[0] for i in table_info]
        keySets = [i[1] for i in table_info]
        saltChars = [i[2] for i in table_info]

        DecryptedPasswordsSet = []
        for pas in range(len(saltedPas)):
            currentKeySet = keySets[pas]
            newPas = pas
            for key in self.SequenceBreak(currentKeySet):   # Calls static function to seperate the inputted sequences
                decrypted = self.Decrypt(saltedPas[pas], key, setDF)    # Calls the encryption algorithm for selected character, key set header and keys
                newPas = decrypted
            
            curSaltChars = saltChars[pas]
            pasWithoutSalt = self.removeSalt(newPas, curSaltChars)  # Calls static function where salted characters are removed

            DecryptedPasswordsSet.append([currentKeySet, curSaltChars, pasWithoutSalt])
        return DecryptedPasswordsSet
    
    def copy_to_clipboard(self, text):
        self.clipboard_clear()  # Clear the clipboard
        self.clipboard_append(text)  # Append the text to the clipboard
        self.update()

    def display_output(self, output_data):  # What happens after execution
        # Clears the existing table
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

        # Creates new labels for the table headers
        headers = ['Sequence', 'Salt', 'Decrypted Password']
        for c, header_text in enumerate(headers):
            header_label = Label(self.dynamic_frame, width=buttonCriteria['Per-app Size'][0],  text=header_text, font=(colorScheme['Text Font'], 10), bg=colorScheme['Table Header Color'], fg=colorScheme['Text Color'], relief="raised")
            header_label.grid(row=0, column=c, pady=10, padx=1)

        # Populates the table with output data
        for r, row_data in enumerate(output_data, start=1):
            for c, value in enumerate(row_data, start=0):
                if c > 1:  # Check if the current column is one of the first two columns
                    masked_value = '*' * len(value)  # Replace the actual value with asterisks
                    label = Label(self.dynamic_frame, width=buttonCriteria['Per-app Size'][0], text=masked_value)
                else: 
                    label = Label(self.dynamic_frame, width=buttonCriteria['Per-app Size'][0], text=value)
                label.grid(row=r, column=c, pady=1, padx=1, ipady=4)

            # Prepares row data as a string for copying
            row_data_str = "\t".join(map(str, row_data))  # Joined with a tab character for Excel compatibility

            # Creates buttons for each row allowing you to copy the password of specific rows
            copy_button = Button(self.dynamic_frame, text="Copy", command=lambda value=row_data_str: self.copy_to_clipboard(value))
            copy_button.grid(row=r, column=len(row_data), pady=1, padx=1)

        # Exports table if option is ticked
        if self.export_to_csv_var.get():
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            with open(file_path, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(headers)
                csv_writer.writerows(output_data)

    def open_file_dialog(self):     # Promts user to navigate to location of CSV
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            dataFrame = self.read_csv(file_path)
            return dataFrame

    def read_csv(self, file_path):  # Reads CSV as dataframe
        try:
            with open(file_path, 'r') as file:
                read_file = pd.read_csv(file)
                read_file.drop(columns=read_file.columns[0])    # Drops first column (a dummy column) due to excel's encoding causing issues with the import. 
                correctedReadFile = read_file.drop(columns=read_file.columns[0])
                return correctedReadFile
        except Exception as e:
            print("Error reading CSV:", str(e))


    @staticmethod
    def SequenceBreak(string):  #Breaks up key set sequence string
        result = []
        current = ''

        for char in string:
            if char.isalpha():  # Checks if character is a letter
                if current:
                    result.append(current)  # Appends the current string in the queue to the result set as a key set
                    current = char  # Resets current queue
                else:
                    current += char
            else:
                current += char
        if current:
            result.append(current)

        return result

    @staticmethod
    def Decrypt(string, seq, setDF):    # The decryption algorithm
        DefaultCharSet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','!','@','#','$','%','^','&','*','?','~','0','1','2','3','4','5','6','7','8','9']
        decryptedString = ''

        for char in string:
            defaultNum = DefaultCharSet.index(char) # Get position in defalt set
            set = setDF[seq].to_list()              # Get list of keys using the necessary header
            setNum = set.index(defaultNum)          # Get position of integer in key set
            newChar = DefaultCharSet[setNum]        # Get DefaultCharSet character at that positional value
            decryptedString += str(newChar)

        string = decryptedString
        return string

    @staticmethod
    def removeSalt(saltedPassword, saltCharacters): # Removes salt characters from string
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
        self.configure(bg=colorScheme['Background'])

        self.static_frame = tk.Frame(self, bg=colorScheme['Background'])
        self.static_frame.pack(side='right', fill='x', pady=(10, 0))

        self.dynamic_frame = tk.Frame(self, bg=colorScheme['Background'])
        self.dynamic_frame.pack(fill='both', expand=True)

        self.base_window()

    def create_buttons(self):   # Create all buttons used for page
        generate_key_set = "Generate Key Set"
        self.generate_key_button = Button(self.static_frame, text=generate_key_set, font=(colorScheme['Text Color'], buttonCriteria['Per-app Font Size'], 'bold'), command=self.Generate_Button_Action, bg=colorScheme['Button Color'], width=buttonCriteria['Per-app Size'][0], height=buttonCriteria['Per-app Size'][1], borderwidth=4, relief="raised")
        self.generate_key_button.grid(row=1, column=2, padx=10, pady=10, sticky="e")

        randomize_sets = "Randomize Sets Into\nSequences"
        self.randomize_sets_button = Button(self.static_frame, text=randomize_sets, font=(colorScheme['Text Color'], buttonCriteria['Per-app Font Size'], 'bold'), command=self.Randomize_Button_Action, bg=colorScheme['Button Color'], width=buttonCriteria['Per-app Size'][0], height=buttonCriteria['Per-app Size'][1], borderwidth=4, relief="raised")
        self.randomize_sets_button.grid(row=2, column=2, padx=10, pady=10, sticky="e")

        refresh_button = "Refresh"
        self.other_button = Button(self.static_frame, text=refresh_button, font=(colorScheme['Text Color'], buttonCriteria['Per-app Font Size'], 'bold'), command=self.Refresh_Button_Action, bg=colorScheme['Button Color'], width=buttonCriteria['Per-app Size'][0], height=buttonCriteria['Per-app Size'][1], borderwidth=4, relief="raised")
        self.other_button.grid(row=3, column=2, padx=10, pady=10, sticky="e")

        main_page_redirect_button = "Return to\nMain Page"
        self.other_button = Button(self.static_frame, text=main_page_redirect_button, font=(colorScheme['Text Color'], buttonCriteria['Per-app Font Size'], 'bold'), command=lambda: self.controller.show_frame(MainHub), bg=colorScheme['Button Color'], width=buttonCriteria['Per-app Size'][0], height=buttonCriteria['Per-app Size'][1], borderwidth=4, relief="raised")
        self.other_button.grid(row=4, column=2, padx=10, pady=10, sticky="e")

    def Refresh_Button_Action(self):    # Destroy current page and rebuild the base window setup
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

        self.base_window()

    def base_window(self):  # Creates base instance of page that can be reverted to as needed
        self.label_text = "Generate a sequence!"
        self.label = Label(self.dynamic_frame, text=self.label_text, font=(colorScheme['Text Font'], 20, 'bold'), bg=colorScheme['Label Color'], fg=colorScheme['Background'], borderwidth=2, relief="raised", width=40)
        self.label.grid(row=0, column=0, columnspan=3, padx=150, pady=20)

        # Creates frame for valid characters so they can be packed into a single grid cell
        self.valid_char_frame_setup()

        # Creates frame for Generate Set input values so they can be in a single grid cell
        self.generate_tab_frame = Frame(self.dynamic_frame, bg=colorScheme['Background'])
        self.generate_tab_frame.grid(row=1, column=1, padx=10, pady=10, sticky="e")
        self.genTable = self.create_table(self.generate_tab_frame, 1, 2, ['Characters', 'Number of Sets'])

        self.randomize_tab_frame = Frame(self.dynamic_frame, bg=colorScheme['Background'])
        self.randomize_tab_frame.grid(row=2, column=1, padx=10, pady=100, sticky="e")
        self.randTable = self.create_table(self.randomize_tab_frame, 1, 2, ['Amount of Sequences', 'Amount of Keys to Use'])

        self.create_buttons()

    def Generate_Button_Action(self):   # The process that happens when the "Generate Key Sets" button is clicked
        input = self.get_table_info(self.genTable)
        charset = str(input[0]) # String, characters to be used for key set headers
        count = int(input[1])   # Integer, amount of sets to be made for each character
        keySets = self.generate_keys(charset, count)
        csv_file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])   # Prompts user to select a path to add file to
        if csv_file_path:
            keySets.to_csv(csv_file_path)
        else:
            pass

    def Randomize_Button_Action(self):  # The process that happens when the "Randomize Sets into Sequences" button is clicked
        keySets = self.process_existing_keys()
        list = self.SequenceBreak(''.join(keySets))
        input = self.get_table_info(self.randTable)
        try:
            amt = int(input[0])     # Amount of sequences to be generated
            count = int(input[1])   # Amount of keys to be selected in each randomization
            randomizedList = self.randomize_created_keys(list, amt, count)

            self.randomize_output_frame = Frame(self.dynamic_frame, bg=colorScheme['Background'])
            self.randomize_output_frame.grid(row=2, column=0, padx=10, pady=10, sticky="e")

            # Creates a header for the table
            header_label = Label(self.randomize_output_frame, width=15, text='Sequences', font=(colorScheme['Text Font'], 12), bg=colorScheme['Table Header Color'], fg=colorScheme['Text Color'], relief="raised")
            header_label.grid(row=0, column=0, pady=10, padx=1)

            # Iterates over randomizedList to populate the table
            for r, value in enumerate(randomizedList, start=1):
                label = Label(self.randomize_output_frame, width=15, text=value)
                label.grid(row=r, column=0, pady=1, padx=1, ipady=4)
            
            output = '\t\n'.join(randomizedList)
            copy_btn = Button(self.randomize_output_frame, text="Copy to Clipboard", command=lambda value=output: self.copy_to_clipboard(output))
            copy_btn.grid(row=0, column=1, pady=1, padx=30)
        except Exception as e:
            print("Error:", str(e))

    def valid_char_frame_setup(self):   #Creates the frame where the valid characters table will be
        self.char_container = Frame(self.dynamic_frame, bg=colorScheme['Valid Characters Table'])
        self.char_container.grid(row=1, column=0, padx=0, pady=(0, 10))

        self.valid_characters_label = Label(self.char_container, text="Valid Characters:", font=(colorScheme['Text Font'], 16, 'bold'), bg=colorScheme['Valid Characters Table'], fg=colorScheme['Text Color'], highlightthickness=2, relief="solid")
        self.valid_characters_label.pack(side=TOP, fill=X)

        valid_characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.val_char_box = Text(self.char_container, font=(colorScheme['Text Font'], 14), bg=colorScheme['Valid Characters Table'], fg=colorScheme['Text Color'], height=2, width=26, relief='flat')
        self.val_char_box.pack(side=BOTTOM, fill=X, pady=5)
        self.val_char_box.insert(tk.END, valid_characters)

    def copy_to_clipboard(self, text):  # Handles clipboard
        self.clipboard_clear()  # Clear the clipboard
        self.clipboard_append(text)  # Append new text to the clipboard

    def create_table(self, root, rows, columns, head):  # Creates table
        table = []

        headers = head
        for c, header_text in enumerate(headers):
            header_label = Label(root, text=header_text, width=25, font=(colorScheme['Text Font'], 12), bg=colorScheme['Table Header Color'], fg=colorScheme['Text Color'], relief="raised")
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

    def get_table_info(self, table):    # Retrieves information from table
        row_items = []

        for r, row in enumerate(table):
            row_val = []
            for c, var in enumerate(row):
                value = var.get()
                row_val.append(value)
            row_items.append(row_val)

        return row_items[0]

    def process_existing_keys(self):    # Prompts user to import key sets
        keys_df = self.open_file_dialog()   # Prompts you to manually navigate to a CSV file to parse through for the keys
        if keys_df is not None:
            keySets = []
            for header in keys_df:
                keySets.append(header)
            return keySets
        else:
            # Handles the case where the CSV could not be loaded
            print("Error loading the CSV file.")

    def open_file_dialog(self): # Prompts user to navigate to CSV file location
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            dataFrame = self.read_csv(file_path)
            return dataFrame

    def read_csv(self, file_path):  # Reads CSV
        try:
            with open(file_path, 'r') as file:
                read_file = pd.read_csv(file)
                read_file.drop(columns=read_file.columns[0])
                correctedReadFile = read_file.drop(columns=read_file.columns[0])
                return correctedReadFile
        except Exception as e:
            print("Error reading CSV:", str(e))


    @staticmethod
    def generate_keys(charSet, countPerChar):   # Generates key sets. Takes string, int
        charSet = ''.join(dict.fromkeys(charSet))   # Converts to dict to remove duplicates then converts back to string
        # The below represents int versions of all legal characters allowed in the cypher
        baseNumSet = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71]
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
        # "KeySet" is the list of all keys in data frame
        sequenceSet = []

        if count is None:
            count = len(keySet)
        
        for seqSet in range(amount):   # For each sequence
            randomSequence = random.sample(keySet, count)
            random.shuffle(randomSequence)
            sequenceSet.append(''.join(randomSequence))
        
        return sequenceSet
    
    @staticmethod
    def SequenceBreak(string):  # Breaks up key set sequence string
        result = []
        current = ''

        for char in string:
            if char.isalpha():  # Checks if character is a letter
                if current:
                    result.append(current)      # Appends the current string in the queue to the result set as a key set
                    current = char              # Resets current queue
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
            min_width = 800  # Define a minimum width
            if required_width < min_width:
                required_width = min_width

        self.geometry(f"{required_width}x{required_height}")


if __name__ == "__main__":
    app = MainApp()
    
    app.mainloop()