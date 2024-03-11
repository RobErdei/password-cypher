import tkinter as tk
from tkinter import *
from Encrypt import EncryptPage
from Decrypt import DecryptPage

class MainHub:
    def __init__(self, root, mode):
        self.root = root
        self.mode = mode
        self.root.title("Base")
        self.root.configure(bg='#74AA9C')

        self.page_frame = Frame(self.root, bg='#74AA9C')
        self.page_frame.pack()

        self.label_text = "Would you like to encrypt or decrypt?"
        self.label = Label(self.page_frame, text=self.label_text, font=('', 20, 'bold'), bg='#74AA9C')
        self.label.pack(padx=20, pady=20)

        Decrypt_button_text = "Decrypt"
        self.Decrypt_button = Button(self.page_frame, text=Decrypt_button_text, command=self.goToDecrypt, bg='#FFFDD0', width=20, height=10)
        self.Decrypt_button.pack(padx=20, pady=20)

        Encrypt_button_text = "Encrypt"
        self.Decrypt_button = Button(self.page_frame, text=Encrypt_button_text, command=self.goToEncrypt, bg='#FFFDD0', width=20, height=10)
        self.Decrypt_button.pack(padx=20, pady=20)


    def goToDecrypt(self):
        root = tk.Tk()  # Create a new instance of Tk
        new_window = DecryptPage(root, "decrypt")  # Create DecryptPage instance
        root.mainloop()  # Start the event loop for the new window

    def goToEncrypt(self):
        root = tk.Tk()  # Create a new instance of Tk
        new_window = EncryptPage(root, "encrypt")  # Create EncryptPage instance
        root.mainloop()  # Start the event loop for the new window

    def Blank(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    main_hub = MainHub(root, "main")
    root.mainloop()