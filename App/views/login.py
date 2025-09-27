import tkinter as tk
from tkinter import ttk, messagebox
from database.data import get_user_by_login

class LoginFrame(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        container = ttk.Frame(self)
        container.place(relx=0.5, rely=0.5, anchor="center")
        container.columnconfigure(1, weight=1)

        # Título
        ttk.Label(container, text="Login", font=("Arial", 18)).grid(row=0, column=0, columnspan=2, pady=(0, 15))

        # Formulário
        ttk.Label(container, text="Email ou Telefone:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.login_entry = ttk.Entry(container)
        self.login_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(container, text="Senha:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.pwd_entry = ttk.Entry(container, show="*")
        self.pwd_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        # Botões
        btn_frame = ttk.Frame(container)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=(10, 0))

        ttk.Button(btn_frame, text="Login", command=self.login_action).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self.clear_fields).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Cadastrar", command=lambda: controller.show_frame("RegisterFrame")).grid(row=0, column=2, padx=5)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def login_action(self):
        login_value = self.login_entry.get().strip()
        password_value = self.pwd_entry.get().strip()

        if not login_value or not password_value:
            messagebox.showerror("Erro", "Preencha todos os campos")
            return

        user = get_user_by_login(login_value, password_value)
        if not user:
            messagebox.showerror("Erro", "Usuário ou senha incorretos")
            return

        self.controller.current_user = user
        # admin?
        if user.get("is_admin"):
            self.controller.show_frame("AdminFrame", user=user)
        else:
            self.controller.show_frame("ConsultFrame", user=user)    
    
    def clear_fields(self):
        self.login_entry.delete(0, tk.END)
        self.pwd_entry.delete(0, tk.END)
    
    def update_data(self, **kwargs):
        """Chamado sempre que voltar para a tela"""
        self.clear_fields()
