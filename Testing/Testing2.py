import tkinter as tk

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Main Page")
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Encrypt", command=lambda: controller.show_frame(Encrypt))
        button1.pack()

        button2 = tk.Button(self, text="Decrypt", command=lambda: controller.show_frame(Decrypt))
        button2.pack()

class Encrypt(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Encrypt")
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text="Go to Main Page", command=lambda: controller.show_frame(MainPage))
        button.pack()

class Decrypt(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Decrypt")
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text="Go to Main Page", command=lambda: controller.show_frame(MainPage))
        button.pack()

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("400x300")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MainPage, Encrypt, Decrypt):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
