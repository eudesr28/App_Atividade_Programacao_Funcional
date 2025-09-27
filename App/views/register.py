import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database.data import create_user

class RegisterFrame(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        # Container central
        container = ttk.Frame(self)
        container.place(relx=0.5, rely=0.5, anchor="center")
        container.columnconfigure(1, weight=1)

        # Título
        ttk.Label(container, text="Cadastro", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=(0,15))

        # Formulário
        labels = ["Nome", "Email", "Telefone", "Data Nascimento (DD/MM/YYYY)", "Senha"]
        self.entries = {}

        for i, label in enumerate(labels):
            ttk.Label(container, text=label).grid(row=i+1, column=0, sticky="e", padx=5, pady=3)
            entry = ttk.Entry(container)
            if label == "Senha":
                entry.config(show="*")
            entry.grid(row=i+1, column=1, sticky="ew", padx=5, pady=3)
            self.entries[label] = entry

        # Botões
        btn_frame = ttk.Frame(container)
        btn_frame.grid(row=len(labels)+1, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Salvar", command=self.save).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self.clear_fields).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Voltar", command=lambda: controller.show_frame("LoginFrame")).grid(row=0, column=2, padx=5)

    def save(self):
        try:
            nome = self.entries["Nome"].get().strip()
            email = self.entries["Email"].get().strip()
            telefone = self.entries["Telefone"].get().strip()
            dob_str = self.entries["Data Nascimento (DD/MM/YYYY)"].get().strip()
            senha = self.entries["Senha"].get().strip()

            if not nome or not email or not telefone or not dob_str or not senha:
                messagebox.showerror("Erro", "Preencha todos os campos")
                return

            # Valida a data no formato DD/MM/YYYY
            try:
                dob = datetime.strptime(dob_str, "%d/%m/%Y").strftime("%Y-%m-%d") 
            except ValueError:
                messagebox.showerror("Erro", "Data inválida. Use o formato DD/MM/YYYY")
                return

            user_id = create_user(nome, email, telefone, dob, senha)
            messagebox.showinfo("Sucesso", f"Usuário cadastrado com sucesso! ID: {user_id}")
            self.controller.show_frame("LoginFrame")

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
