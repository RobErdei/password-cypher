
import tkinter as tk
from Pages.Hub import MainHub
from Pages.Decrypt import DecryptPage
from Pages.Encrypt import EncryptPage
from Pages.KeyGen import GenerateKeysApp


class MainApp(tk.Tk):
    def __init__(self):

        """
        Initializes all frames that can be used in this app under a parent container
        """

        tk.Tk.__init__(self)

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
        
        """
        Render child frame within existing parent container in this instance if it"s name is called. 
        As frame is called, the instance gets updated with required config values.
        """

        if isinstance(cont, str):
            frame = self.frames[next(f for f in self.frames if f.__name__ == cont)]
        else:
            frame = self.frames[cont]
        
        frame.tkraise()
        if hasattr(frame, "on_visibility"):
            frame.on_visibility(True)
    
        self.update_idletasks()
        
        required_width = frame.winfo_reqwidth()
        required_height = frame.winfo_reqheight()

        if isinstance(frame, EncryptPage) or isinstance(frame, DecryptPage):
            min_width = 800
            if required_width < min_width:
                required_width = min_width

        self.geometry(f"{required_width}x{required_height}")


if __name__ == "__main__":
    app = MainApp()
    
    app.mainloop()