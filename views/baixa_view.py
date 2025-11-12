import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from controllers.estoque_controller import baixar_estoque
from db.connection import conectar

def carregar_baixa(root):
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

    ttk.Label(frame, text="Baixa de Estoque", font=("Helvetica", 18)).pack(pady=10)

    # Busca por nome
    ttk.Label(frame, text="Buscar por nome").pack()
    entry_busca = ttk.Entry(frame, width=50)
    entry_busca.pack(pady=5)

    resultado_var = tk.StringVar()
    combo_resultados = ttk.Combobox(frame, textvariable=resultado_var, width=50, state="readonly")
    combo_resultados.pack(pady=5)

    # Campo oculto para ID
    produto_id_var = tk.StringVar()

    ttk.Label(frame, text="Quantidade a baixar").pack()
    entry_qtd = ttk.Entry(frame, width=30)
    entry_qtd.pack(pady=5)

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

    def carregar_id():
        selecao = resultado_var.get()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um produto da lista.")
            return
        produto_id = selecao.split(" - ")[0]
        produto_id_var.set(produto_id)
        messagebox.showinfo("Produto Selecionado", f"Produto ID {produto_id} carregado.")

    def limpar():
        entry_busca.delete(0, tk.END)
        combo_resultados.set("")
        entry_qtd.delete(0, tk.END)
        produto_id_var.set("")

    def baixar():
        try:
            produto_id = int(produto_id_var.get())
            qtd = int(entry_qtd.get())
            resultado = baixar_estoque(produto_id, qtd)

            if isinstance(resultado, int):
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("SELECT estoque_minimo FROM produtos WHERE id = %s", (produto_id,))
                minimo = cursor.fetchone()[0]
                conn.close()

                if resultado < minimo:
                    messagebox.showwarning("Estoque Baixo", f"Nova quantidade: {resultado} (abaixo do mínimo!)")
                else:
                    messagebox.showinfo("Sucesso", f"Nova quantidade: {resultado}")
                limpar()
            else:
                messagebox.showerror("Erro", resultado)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def voltar():
        from views.menu_view import carregar_menu
        carregar_menu(root)

    botoes_busca = ttk.Frame(frame)
    botoes_busca.pack(pady=10)

    ttk.Button(botoes_busca, text="Buscar", command=buscar).grid(row=0, column=0, padx=5)
    ttk.Button(botoes_busca, text="Carregar Produto", command=carregar_id).grid(row=0, column=1, padx=5)

    botoes = ttk.Frame(frame)
    botoes.pack(pady=20)

    ttk.Button(botoes, text="Lançar Baixa", command=baixar).grid(row=0, column=0, padx=5)
    ttk.Button(botoes, text="Limpar", command=limpar).grid(row=0, column=1, padx=5)
    ttk.Button(botoes, text="Voltar", command=voltar).grid(row=0, column=2, padx=5)


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