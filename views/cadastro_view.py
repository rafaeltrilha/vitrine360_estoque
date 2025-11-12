import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from controllers.produto_controller import cadastrar_produto

def carregar_cadastro(root):
    for widget in root.winfo_children():
        widget.destroy()

    canvas = tk.Canvas(root)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    frame = ttk.Frame(scrollable_frame, padding=30)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Cadastro de Produto", font=("Helvetica", 18)).pack(pady=10)

    nomes_campos = {
        "Nome": "nome",
        "Fabricante": "fabricante",
        "Modelo": "modelo",
        "Descrição": "descricao",
        "Quantidade": "quantidade",
        "Estoque Mínimo": "estoque_minimo"
    }

    campos = {}
    for rotulo, chave in nomes_campos.items():
        ttk.Label(frame, text=rotulo).pack()
        entrada = ttk.Entry(frame, width=50)
        entrada.pack(pady=5)
        campos[chave] = entrada

    def limpar():
        for entrada in campos.values():
            entrada.delete(0, tk.END)

    def salvar():
        dados = {k: v.get() for k, v in campos.items()}
        if not dados["quantidade"].isdigit() or not dados["estoque_minimo"].isdigit():
            messagebox.showerror("Erro", "Quantidade e Estoque Mínimo devem ser números.")
            return
        cadastrar_produto(**dados)
        messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso.")
        limpar()

    def voltar():
        from views.menu_view import carregar_menu
        carregar_menu(root)

    botoes = ttk.Frame(frame)
    botoes.pack(pady=20)

    ttk.Button(botoes, text="Salvar", command=salvar).grid(row=0, column=0, padx=5)
    ttk.Button(botoes, text="Limpar", command=limpar).grid(row=0, column=1, padx=5)
    ttk.Button(botoes, text="Voltar", command=voltar).grid(row=0, column=2, padx=5)







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