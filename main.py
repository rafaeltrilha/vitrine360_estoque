import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from views.menu_view import carregar_menu

def main():
    app = ttk.Window(themename="flatly")  # Você pode trocar o tema: 'darkly', 'cosmo', 'journal', etc.
    app.title("Vitrine360")
    app.geometry("900x600")
    app.resizable(False, False)

    carregar_menu(app)

    app.mainloop()

if __name__ == "__main__":
    main()



# import tkinter as tk
# from views.login_view import abrir_login
# from views.cadastro_view import abrir_cadastro
# from views.baixa_view import abrir_baixa
# from views.crud_view import abrir_crud
# from utils.relatorio import gerar_relatorio_pdf, gerar_relatorio_excel

# def iniciar_sistema():
#     root = tk.Tk()
#     root.title("Vitrine360 - Sistema de Estoque")

#     tk.Button(root, text="Cadastrar Produto", width=30, command=abrir_cadastro).pack(pady=10)
#     tk.Button(root, text="Lançar Baixa de Estoque", width=30, command=abrir_baixa).pack(pady=10)
#     tk.Button(root, text="Consultar/Editar/Excluir Produto", width=30, command=abrir_crud).pack(pady=10)
#     tk.Button(root, text="Gerar Relatório PDF", width=30, command=gerar_relatorio_pdf).pack(pady=10)
#     tk.Button(root, text="Gerar Relatório Excel", width=30, command=gerar_relatorio_excel).pack(pady=10)

#     root.mainloop()

# abrir_login(iniciar_sistema)