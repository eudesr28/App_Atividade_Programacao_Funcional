import tkinter as tk
from tkinter import ttk, messagebox
from database.data import get_user_by_id, get_appointment, with_db
from datetime import datetime

class AdminFrame(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        ttk.Label(self, text="Painel do Administrador", font=("Arial", 16)).pack(pady=10)

        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill="both", expand=True, pady=10)

        # barra horizontal
        self.h_scroll = ttk.Scrollbar(tree_frame, orient="horizontal")
        self.h_scroll.pack(side="bottom", fill="x")

        columns = ("ID", "Nome", "Email", "Telefone", "Nascimento", "Agendamento")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", xscrollcommand=self.h_scroll.set)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(fill="both", expand=True)
        self.h_scroll.config(command=self.tree.xview)

        # Botões
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Editar Cadastro", command=self.edit_user).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Editar Agendamento", command=self.edit_appt).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Excluir Agendamento", command=self.delete_appt).grid(row=0, column=3, padx=5)
        ttk.Button(btn_frame, text="Atualizar Lista", command=self.update_data).grid(row=0, column=4, padx=5)
        ttk.Button(btn_frame, text="Excluir Usuário", command=self.delete_user).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Sair", command=lambda: controller.show_frame("LoginFrame")).grid(row=0, column=5, padx=5)

    def update_data(self, **kwargs):
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Puxa todos os usuários
        @with_db
        def fetch_users(conn):
            cur = conn.cursor()
            cur.execute("SELECT id, name, email, phone, dob FROM users")
            return cur.fetchall()

        users = fetch_users()

        # Preenche
        for u in users:
            user_id, name, email, phone, dob = u

            # Converte a data de nascimento
            try:
                dob_fmt = datetime.strptime(dob, "%Y-%m-%d").strftime("%d/%m/%Y")
            except Exception:
                dob_fmt = dob

            appt_text = "Sem agendamento"

            # Busca agendamento
            appt = get_appointment(user_id)
            if appt:
                try:
                    appt_date_fmt = datetime.strptime(appt['date'], "%Y-%m-%d").strftime("%d/%m/%Y")
                except Exception:
                    appt_date_fmt = appt['date']
                appt_text = f"{appt['service']} em {appt_date_fmt} {appt['time']}"

            self.tree.insert("", "end", values=(user_id, name, email, phone, dob_fmt, appt_text))

    def edit_user(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um usuário")
            return
        user_id = self.tree.item(selected[0])['values'][0]
        user = get_user_by_id(user_id)
        self.controller.show_frame("EditUserFrame", user=user, return_to="AdminFrame")

    def edit_appt(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um usuário")
            return
        user_id = self.tree.item(selected[0])['values'][0]
        appt = get_appointment(user_id)
        if not appt:
            messagebox.showerror("Erro", "Usuário não possui agendamento")
            return
        user = get_user_by_id(user_id)
        self.controller.show_frame("EditApptFrame", user=user, appt=appt, return_to="AdminFrame")

    def delete_user(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um usuário")
            return
        user_id = self.tree.item(selected[0])['values'][0]
        confirm = messagebox.askyesno("Confirmação", "Deseja realmente excluir o usuário?")
        if confirm:
            @with_db
            def remove_user(conn):
                conn.execute("DELETE FROM appointments WHERE user_id = ?", (user_id,))
                conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
            remove_user()
            messagebox.showinfo("Sucesso", "Usuário excluído")
            self.update_data()

    def delete_appt(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um usuário")
            return
        user_id = self.tree.item(selected[0])['values'][0]
        appt = get_appointment(user_id)
        if not appt:
            messagebox.showerror("Erro", "Usuário não possui agendamento")
            return
        confirm = messagebox.askyesno("Confirmação", "Deseja realmente excluir o agendamento?")
        if confirm:
            @with_db
            def remove_appt(conn):
                conn.execute("DELETE FROM appointments WHERE id = ?", (appt['id'],))
            remove_appt()
            messagebox.showinfo("Sucesso", "Agendamento excluído")
            self.update_data()
