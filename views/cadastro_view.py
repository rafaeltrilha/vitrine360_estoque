import tkinter as tk
from tkinter import messagebox
from models.produto import Produto
from controllers.estoque_controller import cadastrar_produto

def abrir_cadastro():
    janela = tk.Toplevel()
    janela.title("Cadastro de Produto")

    campos = ["Nome", "Fabricante", "Modelo", "Descrição", "Quantidade"]
    entradas = {}

    for i, campo in enumerate(campos):
        tk.Label(janela, text=campo).grid(row=i, column=0)
        entradas[campo] = tk.Entry(janela)
        entradas[campo].grid(row=i, column=1)

    def salvar():
        try:
            produto = Produto(
                entradas["Nome"].get(),
                entradas["Fabricante"].get(),
                entradas["Modelo"].get(),
                entradas["Descrição"].get(),
                int(entradas["Quantidade"].get())
            )
            cadastrar_produto(produto)
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            janela.destroy()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    tk.Button(janela, text="Salvar", command=salvar).grid(row=len(campos), columnspan=2)