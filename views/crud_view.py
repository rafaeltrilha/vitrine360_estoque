import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from db.connection import conectar

def carregar_crud(root):
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

    ttk.Label(frame, text="Consulta e Edição de Produto", font=("Helvetica", 18)).pack(pady=10)

    # Campo de busca por nome
    ttk.Label(frame, text="Buscar por nome").pack()
    entry_busca = ttk.Entry(frame, width=50)
    entry_busca.pack(pady=5)

    resultado_var = tk.StringVar()
    combo_resultados = ttk.Combobox(frame, textvariable=resultado_var, width=50, state="readonly")
    combo_resultados.pack(pady=5)

    # Campos de edição
    nomes_campos = {
        "ID": "id",
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

    def buscar():
        try:
            termo = entry_busca.get()
            if not termo:
                messagebox.showwarning("Aviso", "Digite parte do nome do produto.")
                return

            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nome FROM produtos
                WHERE nome LIKE %s
                ORDER BY nome
            """, (f"%{termo}%",))
            resultados = cursor.fetchall()
            conn.close()

            if resultados:
                opcoes = [f"{r[0]} - {r[1]}" for r in resultados]
                combo_resultados["values"] = opcoes
                combo_resultados.current(0)
            else:
                combo_resultados["values"] = []
                messagebox.showinfo("Aviso", "Nenhum produto encontrado.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na busca: {str(e)}")

    def carregar_produto():
        try:
            selecao = resultado_var.get()
            if not selecao:
                messagebox.showwarning("Aviso", "Selecione um produto da lista.")
                return

            produto_id = selecao.split(" - ")[0]

            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nome, fabricante, modelo, descricao, quantidade, estoque_minimo
                FROM produtos WHERE id = %s
            """, (produto_id,))
            produto = cursor.fetchone()
            conn.close()

            if produto:
                limpar()
                campos["id"].insert(0, str(produto[0]))
                campos["nome"].insert(0, str(produto[1] or ""))
                campos["fabricante"].insert(0, str(produto[2] or ""))
                campos["modelo"].insert(0, str(produto[3] or ""))
                campos["descricao"].insert(0, str(produto[4] or ""))
                campos["quantidade"].insert(0, str(produto[5] or ""))
                campos["estoque_minimo"].insert(0, str(produto[6] or ""))
                if produto[5] < produto[6]:
                    messagebox.showwarning("Estoque Baixo", "Este produto está abaixo do estoque mínimo!")
            else:
                messagebox.showinfo("Aviso", "Produto não encontrado.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar produto: {str(e)}")

    def atualizar():
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE produtos
                SET nome=%s, fabricante=%s, modelo=%s, descricao=%s, quantidade=%s, estoque_minimo=%s
                WHERE id=%s
            """, (
                campos["nome"].get(),
                campos["fabricante"].get(),
                campos["modelo"].get(),
                campos["descricao"].get(),
                int(campos["quantidade"].get()),
                int(campos["estoque_minimo"].get()),
                int(campos["id"].get())
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Produto atualizado com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao atualizar: {str(e)}")

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
            messagebox.showerror("Erro", f"Falha ao excluir: {str(e)}")

    def voltar():
        from views.menu_view import carregar_menu
        carregar_menu(root)

    botoes_busca = ttk.Frame(frame)
    botoes_busca.pack(pady=10)

    ttk.Button(botoes_busca, text="Buscar", command=buscar).grid(row=0, column=0, padx=5)
    ttk.Button(botoes_busca, text="Carregar Produto", command=carregar_produto).grid(row=0, column=1, padx=5)

    botoes = ttk.Frame(frame)
    botoes.pack(pady=20)

    ttk.Button(botoes, text="Atualizar", command=atualizar).grid(row=0, column=0, padx=5)
    ttk.Button(botoes, text="Excluir", command=excluir).grid(row=0, column=1, padx=5)
    ttk.Button(botoes, text="Limpar", command=limpar).grid(row=0, column=2, padx=5)
    ttk.Button(botoes, text="Voltar", command=voltar).grid(row=0, column=3, padx=5)


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