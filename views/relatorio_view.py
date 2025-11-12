import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox

def carregar_relatorios(root):
    for widget in root.winfo_children():
        widget.destroy()

    frame = ttk.Frame(root, padding=30)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Relatórios", font=("Helvetica", 18)).pack(pady=20)
    ttk.Label(frame, text="(Em breve: gráficos, exportações, filtros...)").pack()

    def voltar():
        from views.menu_view import carregar_menu
        carregar_menu(root)

    ttk.Button(frame, text="Voltar", command=voltar).pack(pady=30)