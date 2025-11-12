import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from controllers.produto_controller import cadastrar_produto

def carregar_cadastro(root):
    for widget in root.winfo_children():
        widget.destroy()

    frame = ttk.Frame(root, padding=30)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Cadastro de Produto", font=("Helvetica", 18)).pack(pady=10)

    campos = {}
    for campo in ["Nome", "Fabricante", "Modelo", "Descrição", "Quantidade"]:
        ttk.Label(frame, text=campo).pack()
        entrada = ttk.Entry(frame, width=50)
        entrada.pack(pady=5)
        campos[campo.lower()] = entrada

    def limpar():
        for entrada in campos.values():
            entrada.delete(0, tk.END)

    def salvar():
        dados = {k: v.get() for k, v in campos.items()}
        if not dados["quantidade"].isdigit():
            messagebox.showerror("Erro", "Quantidade deve ser um número.")
            return
        cadastrar_produto(**dados)
        messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso.")
        limpar()

    def voltar():
        from views.menu_view import carregar_menu
        carregar_menu(root)

    ttk.Button(frame, text="Salvar", command=salvar).pack(pady=10)
    ttk.Button(frame, text="Limpar", command=limpar).pack()
    ttk.Button(frame, text="Voltar", command=voltar).pack(pady=20)







# import tkinter as tk
# from tkinter import messagebox
# from models.produto import Produto
# from controllers.estoque_controller import cadastrar_produto

# def abrir_cadastro():
#     janela = tk.Toplevel()
#     janela.title("Cadastro de Produto")

#     campos = ["Nome", "Fabricante", "Modelo", "Descrição", "Quantidade"]
#     entradas = {}

#     for i, campo in enumerate(campos):
#         tk.Label(janela, text=campo).grid(row=i, column=0)
#         entradas[campo] = tk.Entry(janela)
#         entradas[campo].grid(row=i, column=1)

#     def salvar():
#         try:
#             produto = Produto(
#                 entradas["Nome"].get(),
#                 entradas["Fabricante"].get(),
#                 entradas["Modelo"].get(),
#                 entradas["Descrição"].get(),
#                 int(entradas["Quantidade"].get())
#             )
#             cadastrar_produto(produto)
#             messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
#             janela.destroy()
#         except Exception as e:
#             messagebox.showerror("Erro", str(e))

#     tk.Button(janela, text="Salvar", command=salvar).grid(row=len(campos), columnspan=2)