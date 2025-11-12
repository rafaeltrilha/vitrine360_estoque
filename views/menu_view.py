import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from views.cadastro_view import carregar_cadastro
from views.baixa_view import carregar_baixa
from views.crud_view import carregar_crud
from views.relatorio_view import carregar_relatorios

def carregar_menu(root):
    for widget in root.winfo_children():
        widget.destroy()

    frame = ttk.Frame(root, padding=30)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Menu Principal", font=("Helvetica", 20)).pack(pady=20)

    ttk.Button(frame, text="Cadastrar Produto", width=30, command=lambda: carregar_cadastro(root)).pack(pady=10)
    ttk.Button(frame, text="Lançar Baixa de Estoque", width=30, command=lambda: carregar_baixa(root)).pack(pady=10)
    ttk.Button(frame, text="Consultar / Editar Produto", width=30, command=lambda: carregar_crud(root)).pack(pady=10)
    ttk.Button(frame, text="Gerar Relatórios", width=30, command=lambda: carregar_relatorios(root)).pack(pady=10)
    ttk.Button(frame, text="Sair", width=30, bootstyle="danger", command=root.destroy).pack(pady=30)