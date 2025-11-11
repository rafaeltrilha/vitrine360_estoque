import tkinter as tk
from tkinter import messagebox
from db.connection import conectar

def abrir_crud():
    janela = tk.Toplevel()
    janela.title("CRUD de Produto")

    tk.Label(janela, text="ID do Produto").grid(row=0, column=0)
    entry_id = tk.Entry(janela)
    entry_id.grid(row=0, column=1)

    tk.Label(janela, text="Nome").grid