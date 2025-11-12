import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from controllers.estoque_controller import baixar_estoque

def carregar_baixa(root):
    for widget in root.winfo_children():
        widget.destroy()

    frame = ttk.Frame(root, padding=30)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Baixa de Estoque", font=("Helvetica", 18)).pack(pady=10)

    ttk.Label(frame, text="ID do Produto").pack()
    entry_id = ttk.Entry(frame, width=30)
    entry_id.pack(pady=5)

    ttk.Label(frame, text="Quantidade a baixar").pack()
    entry_qtd = ttk.Entry(frame, width=30)
    entry_qtd.pack(pady=5)

    def limpar():
        entry_id.delete(0, tk.END)
        entry_qtd.delete(0, tk.END)

    def baixar():
        try:
            produto_id = int(entry_id.get())
            qtd = int(entry_qtd.get())
            resultado = baixar_estoque(produto_id, qtd)
            if isinstance(resultado, int):
                messagebox.showinfo("Sucesso", f"Nova quantidade: {resultado}")
                limpar()
            else:
                messagebox.showerror("Erro", resultado)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def voltar():
        from views.menu_view import carregar_menu
        carregar_menu(root)

    ttk.Button(frame, text="Lançar Baixa", command=baixar).pack(pady=10)
    ttk.Button(frame, text="Limpar", command=limpar).pack()
    ttk.Button(frame, text="Voltar", command=voltar).pack(pady=20)


# import tkinter as tk
# from tkinter import messagebox
# from controllers.estoque_controller import baixar_estoque
# from utils.alerta import verificar_alerta

# def abrir_baixa():
#     janela = tk.Toplevel()
#     janela.title("Baixa de Estoque")

#     tk.Label(janela, text="ID do Produto").grid(row=0, column=0)
#     entry_id = tk.Entry(janela)
#     entry_id.grid(row=0, column=1)

#     tk.Label(janela, text="Quantidade a Baixar").grid(row=1, column=0)
#     entry_qtd = tk.Entry(janela)
#     entry_qtd.grid(row=1, column=1)

#     def baixar():
#         try:
#             produto_id = int(entry_id.get())
#             qtd_baixa = int(entry_qtd.get())
#             resultado = baixar_estoque(produto_id, qtd_baixa)

#             if isinstance(resultado, int):
#                 alerta = verificar_alerta(resultado)
#                 if alerta:
#                     messagebox.showwarning("Alerta", alerta)
#                 else:
#                     messagebox.showinfo("Sucesso", "Baixa realizada com sucesso.")
#             else:
#                 messagebox.showerror("Erro", resultado)
#         except Exception as e:
#             messagebox.showerror("Erro", str(e))

#     tk.Button(janela, text="Lançar Baixa", command=baixar).grid(row=2, columnspan=2)