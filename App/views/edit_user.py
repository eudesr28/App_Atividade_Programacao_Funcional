import tkinter as tk
from tkinter import ttk, messagebox
from database.data import get_user_by_id, create_user, with_db

@with_db
def update_user(conn, user_id, name, email, phone, dob):
    cur = conn.cursor()
    cur.execute("""
        UPDATE users
        SET name = ?, email = ?, phone = ?, dob = ?
        WHERE id = ?
    """, (name.strip(), email.strip().lower(), phone.strip(), dob, user_id))

class EditUserFrame(ttk.Frame):
    def __init__(self, master, controller, user=None ,return_to="AdminFrame"):
        super().__init__(master)
        self.controller = controller
        self.user = user
        self.return_to = return_to

        ttk.Label(self, text="Editar Usuário", font=("Arial", 16)).pack(pady=10)

        frm = ttk.Frame(self)
        frm.pack(pady=5, padx=10, fill="x")

        labels = ["Nome", "Email", "Telefone", "Data Nascimento (DD/MM/YYYY)"]
        self.entries = {}

        for i, label in enumerate(labels):
            ttk.Label(frm, text=label).grid(row=i, column=0, sticky="e", pady=2)
            entry = ttk.Entry(frm)
            entry.grid(row=i, column=1, sticky="ew", pady=2)
            self.entries[label] = entry

        if user:
            self.entries["Nome"].insert(0, user["name"])
            self.entries["Email"].insert(0, user["email"])
            self.entries["Telefone"].insert(0, user["phone"])
            self.entries["Data Nascimento (DD/MM/YYYY)"].insert(0, user["dob"])

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Salvar", command=self.save).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self.clear_fields).grid(row=0, column=1, padx=5)
        ttk.Button(self, text="Voltar", command=lambda: controller.show_frame(self.return_to)).pack()


    def save(self):
        try:
            name = self.entries["Nome"].get()
            email = self.entries["Email"].get()
            phone = self.entries["Telefone"].get()
            dob = self.entries["Data Nascimento (DD/MM/YYYY)"].get()

            if not all([name, email, phone, dob]):
                messagebox.showerror("Erro", "Preencha todos os campos")
                return

            update_user(self.user["id"], name, email, phone, dob)
            messagebox.showinfo("Sucesso", "Dados do usuário atualizados!")
            self.controller.show_frame("AdminFrame")

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
