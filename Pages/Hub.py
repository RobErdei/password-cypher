import tkinter as tk
from tkinter import Label, Button, LEFT, RIGHT
import json
from pathlib import Path
from Pages.Decrypt import DecryptPage
from Pages.Encrypt import EncryptPage
from Pages.KeyGen import GenerateKeysApp

class MainHub(tk.Frame):
    def __init__(self, parent, controller):

        """
        Serves as a launch point for all main functionalities of the app.
        Initializes button layout for all redirects to other frames.
        Frames get drawn via their string name rather than being called directly to avoid import conflicts.
        """

        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config_data = self.load_config()

        self.colors = self.config_data['colorScheme']
        self.buttons = self.config_data['buttonCriteria']
        self.configure(bg=self.colors['Background'])

        self.label_text = "What Would You Like To Do?"
        self.label = Label(self, text=self.label_text, font=(self.colors['Text Font'], 20, 'bold'), bg=self.colors['Label Color'], fg=self.colors['Background'], borderwidth=2, relief="solid", width=50, height=2)
        self.label.pack(padx=20, pady=20)

        encrypt_button_text = "Generate\nKeys"
        self.encrypt_button = Button(self, text=encrypt_button_text, font=(self.colors['Text Font'], self.buttons['Main Hub Font Size'], 'bold'), command=self.go_to_GenerateKeys, bg=self.colors['Button Color'], width=self.buttons['Main Hub Size'][0], height=self.buttons['Main Hub Size'][1], borderwidth=4, relief="raised")
        self.encrypt_button.pack(side=LEFT, padx=25, pady=20)

        encrypt_button_text = "Encrypt"
        self.encrypt_button = Button(self, text=encrypt_button_text, font=(self.colors['Text Font'], self.buttons['Main Hub Font Size'], 'bold'), command=self.go_to_Encrypt, bg=self.colors['Button Color'], width=self.buttons['Main Hub Size'][0], height=self.buttons['Main Hub Size'][1], borderwidth=4, relief="raised")
        self.encrypt_button.pack(side=LEFT, padx=25, pady=20)

        decrypt_button_text = "Decrypt"
        self.decrypt_button = Button(self, text=decrypt_button_text, font=(self.colors['Text Font'], self.buttons['Main Hub Font Size'], 'bold'), command=self.go_to_Decrypt, bg=self.colors['Button Color'], width=self.buttons['Main Hub Size'][0], height=self.buttons['Main Hub Size'][1], borderwidth=4, relief="raised")
        self.decrypt_button.pack(side=RIGHT, padx=25, pady=20)

    def load_config(self):
        cfg_path = Path(__file__).resolve().parent.parent / 'UiElements' / 'Config.json'
        with cfg_path.open(encoding='utf-8') as f:
            return json.load(f)

    def go_to_GenerateKeys(self):
        self.controller.show_frame(GenerateKeysApp)

    def go_to_Decrypt(self):
        self.controller.show_frame(DecryptPage)

    def go_to_Encrypt(self):
        self.controller.show_frame(EncryptPage)
