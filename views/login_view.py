import tkinter as tk
from tkinter import messagebox
from controllers.usuario_controller import autenticar

def abrir_login(callback_sucesso):
    janela = tk.Tk()
    janela.title("Login - Vitrine360")

    tk.Label(janela, text="Email").grid(row=0, column=0)
    entry_email = tk.Entry(janela)
    entry_email.grid(row=0, column=1)

    tk.Label(janela, text="Senha").grid(row=1, column=0)
    entry_senha = tk.Entry(janela, show="*")
    entry_senha.grid(row=1, column=1)

    def login():
        email = entry_email.get()
        senha = entry_senha.get()
        usuario = autenticar(email, senha)
        if usuario:
            janela.destroy()
            callback_sucesso()
        else:
            messagebox.showerror("Erro", "Credenciais inválidas")

    tk.Button(janela, text="Entrar", command=login).grid(row=2, columnspan=2)
    janela.mainloop()