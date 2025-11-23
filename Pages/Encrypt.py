
import tkinter as tk
from tkinter import Label, Button, Entry, StringVar, filedialog, Frame, Toplevel, TOP, BOTTOM, LEFT, RIGHT, X
import random
import secrets
import pandas as pd
from pathlib import Path
import csv
import json
from pathlib import Path



class EncryptPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.config_data = self.load_config()
        self.colors = self.config_data['colorScheme']
        self.buttons = self.config_data['buttonCriteria']

        self.base_window()

    def load_config(self):
        cfg_path = Path(__file__).resolve().parent.parent / 'UiElements' / 'Config.json'
        with cfg_path.open(encoding='utf-8') as f:
            return json.load(f)

    def base_window(self):
        """
        Set up static background elements of base frame.
        """

        self.static_frame = tk.Frame(self, bg=self.colors['Background'])
        self.static_frame.pack(side='right', fill='x', pady=(10, 0))

        # Dynamic frame for variable table sizing and similar non-rigid object.
        self.dynamic_frame = tk.Frame(self, bg=self.colors['Background'])
        self.dynamic_frame.pack(side='top', fill='both', expand=True)

        self.initial_table_structure = {
            'rows': 1,
            'columns': 2,
            'headers': ['Password', 'Sequence']
        }

        self.label_text = "Enter Your Strings and Sequences"
        self.label = Label(self.dynamic_frame, text=self.label_text, font=(self.colors['Text Font'], 20, 'bold'), bg=self.colors['Label Color'], fg=self.colors['Background'], borderwidth=2, relief="raised", width=40)
        self.label.grid(row=0, column=0, columnspan=3, pady=10)

        # Establishes the grid the input table is in.
        self.content_frame = Frame(self.dynamic_frame, bg=self.colors['Background'])
        self.content_frame.grid(row=1, column=0, columnspan=2)

        # Create a tkinter variable to hold the state of the checkbox. Set in the same grid as the input table.
        self.export_to_csv_var = tk.IntVar()
        self.export_to_csv_checkbox = tk.Checkbutton(self.content_frame, text="Export to CSV", font=(self.colors['Text Font'], 12), bg=self.colors['Checkmark Foreground'], variable=self.export_to_csv_var, borderwidth=2, relief='raised')
        self.export_to_csv_checkbox.grid(row=0, column=6, padx=10, pady=10, sticky="w")

        self.create_table(1, 2, ['Password', 'Sequence'])
        self.create_buttons()

    def on_visibility(self, visible):
        '''
        Binds the paste event to the paste function in the clase
        '''

        if visible:
            self.bind_all("<<Paste>>", self.paste)
        else:
            self.unbind_all("<<Paste>>")

    def create_table(self, rows, columns, head):
        """
        Creates table structure for easier pasting and importing of data.

        Args:
            rows: Count of rows.
            columns: Count of columns.
            head: List of header names of table. Must match length of the columns count.
        returns:
            Table structure in the form of a list.
        """

        self.table = []

        headers = head
        for c, header_text in enumerate(headers):
            header_label = Label(self.content_frame, width=self.buttons['Per-app Size'][0], text=header_text, font=(self.colors['Text Font'], 12), bg=self.colors['Table Header Color'], fg=self.colors['Text Color'], relief="raised")
            header_label.grid(row=0, column=c, pady=10, padx=10)

        for r in range(1, rows + 1):
            row = []
            for c in range(columns):
                if c == 0:
                    var = StringVar()
                    # The first column in this class's table will contain sensitive information and thus will be hidden with '*' in the GUI
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
        """
        Initialize all buttons and their associated characteristics/functionalities.
        """

        encrypt_button_text = "Encrypt"
        self.encrypt_button = Button(self.static_frame, text=encrypt_button_text, font=(self.colors['Text Color'], self.buttons['Per-app Font Size'], 'bold'), command=self.process_data, bg=self.colors['Button Color'], width=self.buttons['Per-app Size'][0], height=self.buttons['Per-app Size'][1], borderwidth=4, relief="raised")
        self.encrypt_button.grid(row=1, column=2, padx=10, pady=10, sticky="e")

        refresh_button = "Refresh"
        self.other_button = Button(self.static_frame, text=refresh_button, font=(self.colors['Text Color'], self.buttons['Per-app Font Size'], 'bold'), command=self.reset_table, bg=self.colors['Button Color'], width=self.buttons['Per-app Size'][0], height=self.buttons['Per-app Size'][1], borderwidth=4, relief="raised")
        self.other_button.grid(row=2, column=2, padx=10, pady=10, sticky="e")

        main_page_redirect_button = "Return to\nMain Page"
        self.other_button = Button(self.static_frame, text=main_page_redirect_button, font=(self.colors['Text Color'], self.buttons['Per-app Font Size'], 'bold'), command=lambda: self.controller.show_frame('MainHub'), bg=self.colors['Button Color'], width=self.buttons['Per-app Size'][0], height=self.buttons['Per-app Size'][1], borderwidth=4, relief="raised")
        self.other_button.grid(row=3, column=2, padx=10, pady=10, sticky="e")

    def reset_table(self):
        """
        Destroys and rebuilds base window upon refresh.
        """

        for widget in self.winfo_children():
            widget.destroy()

        self.base_window()

    def paste(self, event):
        '''
        Access the clipboard from the widget that triggered the event

        Args:
            event: solely used for the "paste" event
        '''

        widget = event.widget
        clipboard_data = widget.clipboard_get()

        if '\t' in clipboard_data:
            rows = clipboard_data.strip().split('\n')

            # Assumes your clipboard was coppied straight from an Excel grid or similar and seperates cell contents by tab
            columns = len(rows[0].split('\t')) if rows else 0

            # Adjusts table size vertically if clipboard contents require it
            if len(rows) > len(self.table):
                difference = len(rows) - len(self.table)
                for additionalRow in range(difference):
                    row = []
                    for column in range(columns):
                        if column == 0:
                            var = StringVar()

                            # The first column in this class's table will contain sensitive information and thus will be hidden visually.
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
        else:
            # Conditional for if you're pasting a string by itself and not a grid
            if isinstance(widget, Entry):
                clipboard_data = clipboard_data.strip()
                current_content = widget.get()
                widget.delete(0, tk.END)
                widget.insert(0, clipboard_data)

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
        '''
        The process that occurs when the "Encrypt" button is clicked
        '''

        keys_df = self.open_file_dialog()
        try:
            encrypted_data = self.encrypt_data(keys_df)
            self.display_output(encrypted_data)
        except Exception as e:
            self.errorWindow(str(e))

    def encrypt_data(self, keys):
        '''
        Prepares table data for easier encrypting.

        args:
            keys_df: Pandas df of keys in sequence.
        returns:
            Table containing salted password, sequences used and salted characters.
        '''
        
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
                encdPas = self.Encrypt(saltedPas, seq, keys)
                newPas = encdPas

            saltedPasswordsSet.append([newPas, ''.join(sequences), salt])

        return saltedPasswordsSet

    def copy_to_clipboard(self, text):
        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()

    def display_output(self, output_data):
        '''
        Sets up frame that displays the encryption output and functionalities availible with that table.

        args:
            output_data: Table (list) of salted password strings, sequences and salt characters.
        '''
        
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Create new labels for the table headers
        headers = ['Encrypted Password', 'Key Set', 'Salt']
        for c, header_text in enumerate(headers):
            header_label = Label(self.content_frame, width=self.buttons['Per-app Size'][0], text=header_text, font=(self.colors['Text Font'], 12), bg=self.colors['Table Header Color'], fg=self.colors['Text Color'], relief="raised")
            header_label.grid(row=0, column=c, pady=10, padx=1)

        # Populate the table with output data
        for r, row_data in enumerate(output_data, start=1):
            for c, value in enumerate(row_data, start=0):
                label = Label(self.content_frame, width=self.buttons['Per-app Size'][0], text=value)
                label.grid(row=r, column=c, pady=1, padx=1, ipady=4)

            # Prepares row data as a string for easy copying
            row_data_str = "\t".join(map(str, row_data))

            # Creates buttons for each row allowing you to copy the password of specific rows as needed
            copy_button = Button(self.content_frame, text="Copy", command=lambda value=row_data_str: self.copy_to_clipboard(value))
            copy_button.grid(row=r, column=len(row_data), pady=1, padx=1)

        if self.export_to_csv_var.get():
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
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

                 # Drops first column (a dummy column) due to excel's encoding causing issues with the import. 
                correctedReadFile = read_file.drop(columns=read_file.columns[0])
                return correctedReadFile
        except Exception as e:
            self.errorWindow(str(e))


    def errorWindow(self, error):
        """
        Creates a new window to display the error error message.
        Window gets centered to parent window.

        Args:
            error: String of the error message
        """

        error_win = Toplevel(self)
        error_win.title("Error")
        error_win.configure(bg=self.colors['Background'])

        error_win.update_idletasks()

        parent_x = self.winfo_rootx()
        parent_y = self.winfo_rooty()
        parent_w = self.winfo_width()
        parent_h = self.winfo_height()

        popup_w = 300
        popup_h = 120

        x = parent_x + (parent_w // 2) - (popup_w // 2)
        y = parent_y + (parent_h // 2) - (popup_h // 2)

        error_win.geometry(f"{popup_w}x{popup_h}+{x}+{y}")
        error_win.resizable(False, False)

        Label(
            error_win,
            text=f"Error: {str(error)}",
            fg="red",
            bg=self.colors['Background'],
            font=(self.colors['Text Font'], 12),
            wraplength=260,
            justify="center",
            padx=10,
            pady=20
        ).pack()

        Button(
            error_win,
            text="OK",
            command=error_win.destroy,
            width=10
        ).pack(pady=5)


    @staticmethod
    def SequenceBreak(string):
        '''
        Breaks up sequence string into key set headers.
        Each key header is a string containing alphabet character followed by an integer.

        args:
            string: Concatenated string of key set headers strings.
        returns:
            A list of key set headers.
        '''
        
        result = []
        current = ''

        for char in string:
            if char.isalpha():
                if current:
                    result.append(current)
                    current = char
                else:
                    current += char
            else:
                current += char
        if current:
            result.append(current)
            
        return result
    
    @staticmethod
    def Encrypt(string, seq, setDF):
        '''
        Defines base set of allowable characters that can be encrypted.
        DefaultCharSet position values get mapped to the key set's corresponding positional value.

        args:
            string: Password string.
            seq: Sequence header.
            setDF: Key set values data frame.
        returns:
            Encrypted string.
        '''
        
        DefaultCharSet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','!','@','#','$','%','^','&','*','?','~','0','1','2','3','4','5','6','7','8','9']
        encryptedString = ''

        for char in string:
            defaultNum = DefaultCharSet.index(char)
            set = setDF[seq].to_list()
            setNum = set[defaultNum]

            # Get character in default set using the new integer as position
            newChar = DefaultCharSet[setNum]
            encryptedString += str(newChar)

        string = encryptedString
        return string

    @staticmethod
    def addSalt(password, length=32):
        '''
        Add valid characters to random locations in the password string.

        args:
            password: Password string inputed into entry table widget.
            length: Fixed, may be changed in the future.
        returns:
            List of salt characters and salted password string.
        '''
        
        baseCharSet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*?~0123456789'

        for i in password:
            baseCharSet = baseCharSet.replace(i,'')
        
        legalCharacters = baseCharSet

        # Randomly select valid characters not in password until max string length (32) is reached
        saltChars = [secrets.choice(legalCharacters) for i in range(length-len(password))]
        passwordCharacters = list(password)
        salt = ''.join(saltChars)
        newSet = []

        while passwordCharacters or saltChars:
            # Randomize order of salt character set
            random.shuffle(saltChars)

            # Alternates randomly between adding a password character or a salt character to the empty set
            if passwordCharacters and (not saltChars or random.random() < 0.5):
                newSet.append(passwordCharacters.pop(0))
            else:
                newSet.append(saltChars.pop(0))

        return [salt, ''.join(newSet)]
    