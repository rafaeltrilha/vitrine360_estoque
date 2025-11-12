import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from db.connection import conectar

def carregar_crud(root):
    for widget in root.winfo_children():
        widget.destroy()

    frame = ttk.Frame(root, padding=30)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Consulta e Edição de Produto", font=("Helvetica", 18)).pack(pady=10)

    campos = {}
    for campo in ["ID", "Nome", "Fabricante", "Modelo", "Descrição", "Quantidade"]:
        ttk.Label(frame, text=campo).pack()
        entrada = ttk.Entry(frame, width=50)
        entrada.pack(pady=5)
        campos[campo.lower()] = entrada

    def limpar():
        for entrada in campos.values():
            entrada.delete(0, tk.END)

    def buscar():
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM produtos WHERE id = %s", (campos["id"].get(),))
            produto = cursor.fetchone()
            conn.close()

            if produto:
                campos["nome"].delete(0, tk.END)
                campos["fabricante"].delete(0, tk.END)
                campos["modelo"].delete(0, tk.END)
                campos["descricao"].delete(0, tk.END)
                campos["quantidade"].delete(0, tk.END)

                campos["nome"].insert(0, produto[1])
                campos["fabricante"].insert(0, produto[2])
                campos["modelo"].insert(0, produto[3])
                campos["descricao"].insert(0, produto[4])
                campos["quantidade"].insert(0, produto[5])
            else:
                messagebox.showinfo("Aviso", "Produto não encontrado.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def atualizar():
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE produtos
                SET nome=%s, fabricante=%s, modelo=%s, descricao=%s, quantidade=%s
                WHERE id=%s
            """, (
                campos["nome"].get(),
                campos["fabricante"].get(),
                campos["modelo"].get(),
                campos["descricao"].get(),
                int(campos["quantidade"].get()),
                int(campos["id"].get())
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Produto atualizado com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def excluir():
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM produtos WHERE id = %s", (campos["id"].get(),))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Produto excluído com sucesso.")
            limpar()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def voltar():
        from views.menu_view import carregar_menu
        carregar_menu(root)

    ttk.Button(frame, text="Buscar", command=buscar).pack(pady=5)
    ttk.Button(frame, text="Atualizar", command=atualizar).pack(pady=5)
    ttk.Button(frame, text="Excluir", command=excluir).pack(pady=5)
    ttk.Button(frame, text="Limpar", command=limpar).pack(pady=5)
    ttk.Button(frame, text="Voltar", command=voltar).pack(pady=20)


# import tkinter as tk
# from tkinter import messagebox
# from db.connection import conectar

# def abrir_crud():
#     janela = tk.Toplevel()
#     janela.title("Consulta e Edição de Produto")

#     tk.Label(janela, text="ID do Produto").grid(row=0, column=0)
#     entry_id = tk.Entry(janela)
#     entry_id.grid(row=0, column=1)

#     tk.Label(janela, text="Nome").grid(row=1, column=0)
#     entry_nome = tk.Entry(janela)
#     entry_nome.grid(row=1, column=1)

#     tk.Label(janela, text="Fabricante").grid(row=2, column=0)
#     entry_fabricante = tk.Entry(janela)
#     entry_fabricante.grid(row=2, column=1)

#     tk.Label(janela, text="Modelo").grid(row=3, column=0)
#     entry_modelo = tk.Entry(janela)
#     entry_modelo.grid(row=3, column=1)

#     tk.Label(janela, text="Descrição").grid(row=4, column=0)
#     entry_descricao = tk.Entry(janela)
#     entry_descricao.grid(row=4, column=1)

#     tk.Label(janela, text="Quantidade").grid(row=5, column=0)
#     entry_quantidade = tk.Entry(janela)
#     entry_quantidade.grid(row=5, column=1)

#     def buscar():
#         try:
#             conn = conectar()
#             cursor = conn.cursor()
#             cursor.execute("SELECT * FROM produtos WHERE id = %s", (entry_id.get(),))
#             produto = cursor.fetchone()
#             conn.close()

#             if produto:
#                 entry_nome.delete(0, tk.END)
#                 entry_fabricante.delete(0, tk.END)
#                 entry_modelo.delete(0, tk.END)
#                 entry_descricao.delete(0, tk.END)
#                 entry_quantidade.delete(0, tk.END)

#                 entry_nome.insert(0, produto[1])
#                 entry_fabricante.insert(0, produto[2])
#                 entry_modelo.insert(0, produto[3])
#                 entry_descricao.insert(0, produto[4])
#                 entry_quantidade.insert(0, produto[5])
#             else:
#                 messagebox.showinfo("Aviso", "Produto não encontrado.")
#         except Exception as e:
#             messagebox.showerror("Erro", str(e))

#     def atualizar():
#         try:
#             conn = conectar()
#             cursor = conn.cursor()
#             cursor.execute("""
#                 UPDATE produtos
#                 SET nome=%s, fabricante=%s, modelo=%s, descricao=%s, quantidade=%s
#                 WHERE id=%s
#             """, (
#                 entry_nome.get(),
#                 entry_fabricante.get(),
#                 entry_modelo.get(),
#                 entry_descricao.get(),
#                 int(entry_quantidade.get()),
#                 int(entry_id.get())
#             ))
#             conn.commit()
#             conn.close()
#             messagebox.showinfo("Sucesso", "Produto atualizado com sucesso.")
#         except Exception as e:
#             messagebox.showerror("Erro", str(e))

#     def excluir():
#         try:
#             conn = conectar()
#             cursor = conn.cursor()
#             cursor.execute("DELETE FROM produtos WHERE id = %s", (entry_id.get(),))
#             conn.commit()
#             conn.close()
#             messagebox.showinfo("Sucesso", "Produto excluído com sucesso.")
#             entry_nome.delete(0, tk.END)
#             entry_fabricante.delete(0, tk.END)
#             entry_modelo.delete(0, tk.END)
#             entry_descricao.delete(0, tk.END)
#             entry_quantidade.delete(0, tk.END)
#         except Exception as e:
#             messagebox.showerror("Erro", str(e))

#     tk.Button(janela, text="Buscar", command=buscar).grid(row=0, column=2, padx=10)
#     tk.Button(janela, text="Atualizar", command=atualizar).grid(row=6, column=0, pady=10)
#     tk.Button(janela, text="Excluir", command=excluir).grid(row=6, column=1, pady=10)