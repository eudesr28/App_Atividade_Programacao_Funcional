import tkinter as tk
from tkinter import ttk
from views.login import LoginFrame
from views.register import RegisterFrame
from views.consult import ConsultFrame
from views.create_appt import CreateApptFrame
from views.edit_appt import EditApptFrame
from views.admin import AdminFrame
from views.edit_user import EditUserFrame 

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Agendamento")
        self.geometry("1000x400")
        self.minsize(500, 300)
        self.current_user = None

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Inicializa todas as telas
        for F in (LoginFrame, RegisterFrame, ConsultFrame, CreateApptFrame, EditApptFrame, AdminFrame, EditUserFrame):
            frame_name = F.__name__
            frame = F(container, self)
            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginFrame")

    def show_frame(self, frame_name, **kwargs):
        """
        Mostra o frame desejado, passando parâmetros opcionais
        """
        frame = self.frames[frame_name]

        if hasattr(frame, "update_data"):
            frame.update_data(**kwargs)
        elif kwargs:
            parent = frame.master
            frame.destroy()
            frame = self.frames[frame_name] = frame.__class__(parent, self, **kwargs)
            frame.grid(row=0, column=0, sticky="nsew")

        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()
