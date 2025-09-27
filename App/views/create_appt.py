import tkinter as tk
from tkinter import ttk, messagebox
from database.data import create_appointment

SERVICES = ["Serviço A", "Serviço B", "Serviço C"]

class CreateApptFrame(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        ttk.Label(self, text="Criar Agendamento", font=("Arial", 16)).pack(pady=10)

        frm = ttk.Frame(self)
        frm.pack(pady=5)

        ttk.Label(frm, text="Serviço:").grid(row=0, column=0)
        self.service_cb = ttk.Combobox(frm, values=SERVICES, state="readonly")
        self.service_cb.grid(row=0, column=1)

        ttk.Label(frm, text="Data (DD-MM-YYYY):").grid(row=1, column=0)
        self.date_entry = ttk.Entry(frm)
        self.date_entry.grid(row=1, column=1)

        ttk.Label(frm, text="Hora (HH:MM):").grid(row=2, column=0)
        self.time_entry = ttk.Entry(frm)
        self.time_entry.grid(row=2, column=1)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        
        # Botões
        ttk.Button(btn_frame, text="Salvar", command=self.save).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self.clear_fields).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Voltar", command=lambda: controller.show_frame("ConsultFrame", user=self.user)).grid(row=0, column=1, padx=5)

    #def update_data(self, user):
    #    self.user = user
        # limpa campos
    
    def update_data(self, user=None, return_to="ConsultFrame"):
        self.user = user
        self.return_to = return_to
        
        self.service_cb.set("")
        self.date_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)

    def save(self):
        service = self.service_cb.get()
        date = self.date_entry.get()
        time = self.time_entry.get()

        if not service or not date or not time:
            messagebox.showerror("Erro", "Preencha todos os campos")
            return

        create_appointment(self.user['id'], service, date, time)
        messagebox.showinfo("Sucesso", "Agendamento criado!")
        self.controller.show_frame("ConsultFrame", user=self.user)
    def clear_fields(self):
        self.service_cb.set("")
        self.date_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)        
