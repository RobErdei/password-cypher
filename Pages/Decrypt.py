import tkinter as tk
from tkinter import Label, Button, Entry, StringVar, filedialog, Frame, Toplevel, TOP, BOTTOM, LEFT, RIGHT, X
from random import shuffle
import pandas as pd
import csv
import json
from pathlib import Path


class DecryptPage(tk.Frame):
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
        self.static_frame = tk.Frame(self, bg=self.colors['Background'])
        self.static_frame.pack(side='right', fill='x', pady=(10, 0))

        # Dynamic frame for variable table sizing and similar non-rigid object.
        self.dynamic_frame = tk.Frame(self, bg=self.colors['Background'])
        self.dynamic_frame.pack(side='top', fill='both', expand=True)

        self.initial_table_structure = {
            'rows': 1,
            'columns': 3,
            'headers': ['Encrypted Password', 'Sequence', 'Salt']
        }

        self.label_text = "Enter Your Strings, Sequence and Salt"
        self.label = Label(self.dynamic_frame, text=self.label_text, font=(self.colors['Text Font'], 20, 'bold'), bg=self.colors['Label Color'], fg=self.colors['Background'], borderwidth=2, relief="raised", width=50)
        self.label.grid(row=0, column=0, columnspan=3, pady=10)

        # Establishes the grid the input table is in.
        self.content_frame = Frame(self.dynamic_frame, bg=self.colors['Background'])
        self.content_frame.grid(row=1, column=0, columnspan=2)

        # Create a tkinter variable to hold the state of the checkbox. Set in the same grid as the input table.
        self.export_to_csv_var = tk.IntVar()
        self.export_to_csv_checkbox = tk.Checkbutton(self.content_frame, text="Export to CSV", font=(self.colors['Text Font'], 12), bg=self.colors['Checkmark Foreground'], variable=self.export_to_csv_var, borderwidth=2, relief='raised')
        self.export_to_csv_checkbox.grid(row=0, column=6, padx=10, pady=10, sticky="w")

        self.create_table(1, 3, ['Encrypted Password', 'Sequence', 'Salt'])
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
                else:
                    var = StringVar()
                    entry = Entry(self.content_frame, textvar=var)
                    entry.grid(row=r, column=c, pady=1, padx=1, ipady=4)
                row.append(var)
            self.table.append(row)

    def reset_window(self):
        for widget in self.winfo_children():
            widget.destroy()
        
        self.base_window()

    def create_buttons(self):
        """
        Initialize all buttons and their associated characteristics/functionalities.
        """

        decrypt_button_text = "Decrypt"
        self.decrypt_button = Button(self.static_frame, text=decrypt_button_text, font=(self.colors['Text Color'], self.buttons['Per-app Font Size'], 'bold'), command=self.process_data, bg=self.colors['Button Color'], width=self.buttons['Per-app Size'][0], height=self.buttons['Per-app Size'][1], borderwidth=4, relief="raised")
        self.decrypt_button.grid(row=1, column=2, padx=10, pady=10, sticky="e")

        refresh_button = "Refresh"
        self.other_button = Button(self.static_frame, text=refresh_button, font=(self.colors['Text Color'], self.buttons['Per-app Font Size'], 'bold'), command=self.reset_window, bg=self.colors['Button Color'], width=self.buttons['Per-app Size'][0], height=self.buttons['Per-app Size'][1], borderwidth=4, relief="raised")
        self.other_button.grid(row=2, column=2, padx=10, pady=10, sticky="e")

        main_page_redirect_button = "Return to\nMain Page"
        self.other_button = Button(self.static_frame, text=main_page_redirect_button, font=(self.colors['Text Color'], self.buttons['Per-app Font Size'], 'bold'), command=lambda: self.controller.show_frame('MainHub'), bg=self.colors['Button Color'], width=self.buttons['Per-app Size'][0], height=self.buttons['Per-app Size'][1], borderwidth=4, relief="raised")
        self.other_button.grid(row=3, column=2, padx=10, pady=10, sticky="e")

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

            # Assumes your clipboard was coppied straight from an Excel grid and seperates cell contents
            columns = len(rows[0].split('\t')) if rows else 0

            # Expands the table vertically if needed
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
            encrypted_data = self.decrypt_data(keys_df)
            self.display_output(encrypted_data)
        except Exception as e:
            self.errorWindow(str(e))

    def decrypt_data(self, setDF):
        '''
        Prepares table data for easier decrypting.

        args:
            keys_df: Pandas df of keys in sequence.
        returns:
            Table containing sequence, salt characters and decrypted password string.
        '''

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
    
    def copy_to_clipboard(self, text):
        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()

    def display_output(self, output_data):
        '''
        Sets up frame that displays the decryption output and functionalities availible with that table.

        args:
            output_data: Table (list) of sequence, salt characters string and decrypted password string.
        '''

        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

        # Creates new labels for the table headers
        headers = ['Sequence', 'Salt', 'Decrypted Password']
        for c, header_text in enumerate(headers):
            header_label = Label(self.dynamic_frame, width=self.buttons['Per-app Size'][0],  text=header_text, font=(self.colors['Text Font'], 10), bg=self.colors['Table Header Color'], fg=self.colors['Text Color'], relief="raised")
            header_label.grid(row=0, column=c, pady=10, padx=1)

        # Populates the table with output data
        for r, row_data in enumerate(output_data, start=1):
            for c, value in enumerate(row_data, start=0):
                if c > 1:
                    # Replace the actual value with asterisks as values are sensitive.
                    masked_value = '*' * len(value)
                    label = Label(self.dynamic_frame, width=self.buttons['Per-app Size'][0], text=masked_value)
                else: 
                    label = Label(self.dynamic_frame, width=self.buttons['Per-app Size'][0], text=value)
                label.grid(row=r, column=c, pady=1, padx=1, ipady=4)

            # Joined with a tab character for Excel compatibility
            row_data_str = "\t".join(map(str, row_data))

            # Creates buttons for each row allowing you to copy the password of specific rows.
            copy_button = Button(self.dynamic_frame, text="Copy", command=lambda value=row_data_str: self.copy_to_clipboard(value))
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
                read_file.drop(columns=read_file.columns[0])
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
    def Decrypt(string, seq, setDF):
        '''
        Defines base set of allowable characters that can be decrypted.
        DefaultCharSet position values get mapped to the key set's corresponding positional value.

        args:
            string: Password string.
            seq: Sequence header.
            setDF: Key set values data frame.
        returns:
            Decrypted string.
        '''

        DefaultCharSet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','!','@','#','$','%','^','&','*','?','~','0','1','2','3','4','5','6','7','8','9']
        decryptedString = ''

        for char in string:
            defaultNum = DefaultCharSet.index(char)
            set = setDF[seq].to_list()
            setNum = set.index(defaultNum)

            # Get DefaultCharSet character at that positional value
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
