import tkinter as tk
from tkinter import Label, Button, Entry, StringVar, Text, filedialog, Frame, Toplevel, TOP, BOTTOM, X
import random
from random import shuffle
import pandas as pd
import json
from pathlib import Path


class GenerateKeysApp(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.config_data = self.load_config()
        self.colors = self.config_data['colorScheme']
        self.buttons = self.config_data['buttonCriteria']
        self.configure(bg=self.colors['Background'])

        self.static_frame = tk.Frame(self, bg=self.colors['Background'])
        self.static_frame.pack(side='right', fill='x', pady=(10, 0))

        self.dynamic_frame = tk.Frame(self, bg=self.colors['Background'])
        self.dynamic_frame.pack(fill='both', expand=True)

        self.base_window()


    def load_config(self):
        cfg_path = Path(__file__).resolve().parent.parent / 'UiElements' / 'Config.json'
        with cfg_path.open(encoding='utf-8') as f:
            return json.load(f)
        
    def base_window(self):
        """
        Set up static background elements of base frame.
        """

        self.label_text = "Generate a sequence!"
        self.label = Label(self.dynamic_frame, text=self.label_text, font=(self.colors['Text Font'], 20, 'bold'), bg=self.colors['Label Color'], fg=self.colors['Background'], borderwidth=2, relief="raised", width=40)
        self.label.grid(row=0, column=0, columnspan=3, padx=150, pady=20)

        self.valCharFrameSetup()

        self.generate_tab_frame = Frame(self.dynamic_frame, bg=self.colors['Background'])
        self.generate_tab_frame.grid(row=1, column=1, padx=10, pady=10, sticky="e")
        self.genTable = self.create_table(self.generate_tab_frame, 1, 2, ['Characters', 'Number of Sets'])

        self.randomize_tab_frame = Frame(self.dynamic_frame, bg=self.colors['Background'])
        self.randomize_tab_frame.grid(row=2, column=1, padx=10, pady=100, sticky="e")
        self.randTable = self.create_table(self.randomize_tab_frame, 1, 2, ['Amount of Sequences', 'Amount of Keys to Use'])

        self.create_buttons()

    def create_buttons(self):
        """
        Initialize all buttons and their associated characteristics/functionalities.
        """

        generate_key_set = "Generate Key Set"
        self.generate_key_button = Button(self.static_frame, text=generate_key_set, font=(self.colors['Text Color'], self.buttons['Per-app Font Size'], 'bold'), command=self.Generate_Button_Action, bg=self.colors['Button Color'], width=self.buttons['Per-app Size'][0], height=self.buttons['Per-app Size'][1], borderwidth=4, relief="raised")
        self.generate_key_button.grid(row=1, column=2, padx=10, pady=10, sticky="e")

        randomize_sets = "Randomize Sets Into\nSequences"
        self.randomize_sets_button = Button(self.static_frame, text=randomize_sets, font=(self.colors['Text Color'], self.buttons['Per-app Font Size'], 'bold'), command=self.Randomize_Button_Action, bg=self.colors['Button Color'], width=self.buttons['Per-app Size'][0], height=self.buttons['Per-app Size'][1], borderwidth=4, relief="raised")
        self.randomize_sets_button.grid(row=2, column=2, padx=10, pady=10, sticky="e")

        refresh_button = "Refresh"
        self.other_button = Button(self.static_frame, text=refresh_button, font=(self.colors['Text Color'], self.buttons['Per-app Font Size'], 'bold'), command=self.Refresh_Button_Action, bg=self.colors['Button Color'], width=self.buttons['Per-app Size'][0], height=self.buttons['Per-app Size'][1], borderwidth=4, relief="raised")
        self.other_button.grid(row=3, column=2, padx=10, pady=10, sticky="e")

        main_page_redirect_button = "Return to\nMain Page"
        self.other_button = Button(self.static_frame, text=main_page_redirect_button, font=(self.colors['Text Color'], self.buttons['Per-app Font Size'], 'bold'), command=lambda: self.controller.show_frame('MainHub'), bg=self.colors['Button Color'], width=self.buttons['Per-app Size'][0], height=self.buttons['Per-app Size'][1], borderwidth=4, relief="raised")
        self.other_button.grid(row=4, column=2, padx=10, pady=10, sticky="e")

    def Refresh_Button_Action(self):
        """
        Destroys adn rebuilds base window upon refresh.
        """

        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

        self.base_window()

    def Generate_Button_Action(self):
        """
        Calls static method to create specified key sets based off of valid character set.
        Takes values from genTable entry widget.
        Exports key sets to csv for external storage.
        """
        
        input = self.getTableInfo(self.genTable)
        charset = str(input[0])
        count = int(input[1])
        keySets = self.generate_keys(charset, count)
        csv_file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if csv_file_path:
            keySets.to_csv(csv_file_path)
        else:
            pass

    def Randomize_Button_Action(self):
        """
        Randomizes order of imported key sets into single sequence string for easy copy-and-paste when encrypting.
        Takes values from randTable entry widget.
        Calls the static methods sequenceBreak and processExistingKeys
        """
        
        keySets = self.processExistingKeys()
        list = self.sequenceBreak(''.join(keySets))
        input = self.getTableInfo(self.randTable)
        try:
            amt = int(input[0])
            count = int(input[1])
            randomizedList = self.randomizeCreatedKeys(list, amt, count)

            self.randomize_output_frame = Frame(self.dynamic_frame, bg=self.colors['Background'])
            self.randomize_output_frame.grid(row=2, column=0, padx=10, pady=10, sticky="e")

            header_label = Label(self.randomize_output_frame, width=15, text='Sequences', font=(self.colors['Text Font'], 12), bg=self.colors['Table Header Color'], fg=self.colors['Text Color'], relief="raised")
            header_label.grid(row=0, column=0, pady=10, padx=1)

            for r, value in enumerate(randomizedList, start=1):
                label = Label(self.randomize_output_frame, width=15, text=value)
                label.grid(row=r, column=0, pady=1, padx=1, ipady=4)
            
            output = '\t\n'.join(randomizedList)
            copy_btn = Button(self.randomize_output_frame, text="Copy to Clipboard", command=lambda value=output: self.copy_to_clipboard(output))
            copy_btn.grid(row=0, column=1, pady=1, padx=30)
        except Exception as e:
            self.errorWindow(str(e))

    def valCharFrameSetup(self):
        """
        Initializes static frame for displaying valid characters that can be used for key sets.
        """
        self.char_container = Frame(self.dynamic_frame, bg=self.colors['Valid Characters Table'])
        self.char_container.grid(row=1, column=0, padx=0, pady=(0, 10))

        self.valid_characters_label = Label(self.char_container, text="Valid Characters:", font=(self.colors['Text Font'], 16, 'bold'), bg=self.colors['Valid Characters Table'], fg=self.colors['Text Color'], highlightthickness=2, relief="solid")
        self.valid_characters_label.pack(side=TOP, fill=X)

        valid_characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.val_char_box = Text(self.char_container, font=(self.colors['Text Font'], 14), bg=self.colors['Valid Characters Table'], fg=self.colors['Text Color'], height=2, width=26, relief='flat')
        self.val_char_box.pack(side=BOTTOM, fill=X, pady=5)
        self.val_char_box.insert(tk.END, valid_characters)

    def copy_to_clipboard(self, text): 
        self.clipboard_clear()
        self.clipboard_append(text)

    def create_table(self, root, rows, columns, head):
        """
        Creates table structure for easier pasting and importing of data.

        Args:
            root: Parent frame this table structure sits over.
            rows: Count of rows.
            columns: Count of columns.
            head: List of header names of table. Must match length of the columns count.
        returns:
            Table structure in the form of a list.
        """
        
        table = []

        for c, header_text in enumerate(head):
            header_label = Label(root, text=header_text, width=25, font=(self.colors['Text Font'], 12), bg=self.colors['Table Header Color'], fg=self.colors['Text Color'], relief="raised")
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

    def getTableInfo(self, table):
        row_items = []

        for r, row in enumerate(table):
            row_val = []
            for c, var in enumerate(row):
                value = var.get()
                row_val.append(value)
            row_items.append(row_val)

        return row_items[0]

    def processExistingKeys(self):
        """
        Prompts user to navigate to and open existing/gernerated key set csv file.
        """

        keys_df = self.open_file_dialog()
        try:
            keySets = []
            for header in keys_df:
                keySets.append(header)
            return keySets
        except Exception as e:
            self.errorWindow(str(e))

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

        try:
            dataFrame = self.read_csv(file_path)
            return dataFrame
        except Exception as e:
            self.errorWindow(str(e))

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
    def generate_keys(charSet, countPerChar):
        """
        Randomizes allowed password character set for each keyset character a specified number of times.

        Args:
            charSet: a string of characters that will be used as headers for the final set of keys.
            countPerChar: determines how many versions key sets will be created per character in charSet string.
        
        returns:
            A Pandas dataframe of all randomized key sets with the set headers in the first row and a dummy "placeholder" column (prevents pandas from writing it into frame on import).
        """
        charSet = ''.join(dict.fromkeys(charSet))

        baseNumSet = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71]
        keySets = []

        for char in charSet:
            keys = []
            for _ in range(countPerChar):
                shuffle(baseNumSet)
                new_key = tuple(baseNumSet)
                while new_key in keys:
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
    def randomizeCreatedKeys(keySet, amount=1, count=None):
        sequenceSet = []

        if count is None:
            count = len(keySet)
        
        for seqSet in range(amount):
            randomSequence = random.sample(keySet, count)
            random.shuffle(randomSequence)
            sequenceSet.append(''.join(randomSequence))
        
        return sequenceSet
    
    @staticmethod
    def sequenceBreak(seqStr):
        """
        Splits sequence into key sets.

        Args:
            seqStr: A sequence string of key sets with each set denoted by an alpha-numeric character and an integer of varying digits.

        return:
            A list of key set headers
        """
        result = []
        current = ''

        for char in seqStr:
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
