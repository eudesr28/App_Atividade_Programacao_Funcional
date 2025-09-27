import tkinter as tk
from tkinter import ttk
from database.data import get_appointment
from datetime import datetime

class ConsultFrame(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.title_label = ttk.Label(self, text="", font=("Arial", 16))
        self.title_label.pack(pady=10)

        self.info_frame = ttk.Frame(self)
        self.info_frame.pack()

        ttk.Button(self, text="Sair", command=lambda: controller.show_frame("LoginFrame")).pack(pady=10)

    def update_data(self, user):
        self.user = user

        # Limpa info anterior
        for widget in self.info_frame.winfo_children():
            widget.destroy()

        self.title_label.config(text=f"Bem-vindo {user['name']}")
        
        dob_str = user['dob']
        try:
            dob_fmt = datetime.strptime(dob_str, "%Y-%m-%d").strftime("%d/%m/%Y")
        except Exception:
            dob_fmt = dob_str
        
        ttk.Label(self.info_frame, text=f"Email: {user['email']}").pack()
        ttk.Label(self.info_frame, text=f"Telefone: {user['phone']}").pack()
        ttk.Label(self.info_frame, text=f"Nascimento: {user['dob']}").pack()

        appt = get_appointment(user['id'])
        if appt:
            
            try:
                appt_date_fmt = datetime.strptime(appt['date'], "%Y-%m-%d").strftime("%d/%m/%Y")
            except Exception:
                appt_date_fmt = appt['date']
            
            ttk.Label(self.info_frame, text=f"Serviço: {appt['service']} em {appt['date']} às {appt['time']}").pack(pady=5)
            
            ttk.Button(self.info_frame, text="Alterar Agendamento",
                       command=lambda: self.controller.show_frame("EditApptFrame", user=user, appt=appt, return_to="ConsultFrame")).pack(pady=5)
        else:
            ttk.Label(self.info_frame, text="Você não possui serviço agendado").pack(pady=5)
            
            ttk.Button(self.info_frame, text="Criar Agendamento",
                       command=lambda: self.controller.show_frame("CreateApptFrame", user=user,return_to="ConsultFrame")).pack(pady=5)
