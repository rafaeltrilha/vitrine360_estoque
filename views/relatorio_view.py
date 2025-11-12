import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from db.connection import conectar
import pandas as pd
from fpdf import FPDF

def carregar_relatorios(root):
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

    ttk.Label(frame, text="Relatório de Estoque Baixo", font=("Helvetica", 18)).pack(pady=10)

    ttk.Label(frame, text="Filtrar por fabricante").pack()
    entry_fabricante = ttk.Entry(frame, width=50)
    entry_fabricante.pack(pady=5)

    tabela = ttk.Treeview(frame, columns=("ID", "Nome", "Fabricante", "Qtd", "Mínimo"), show="headings", height=15)
    tabela.heading("ID", text="ID")
    tabela.heading("Nome", text="Nome")
    tabela.heading("Fabricante", text="Fabricante")
    tabela.heading("Qtd", text="Qtd Atual")
    tabela.heading("Mínimo", text="Estoque Mínimo")
    tabela.pack(pady=10, fill="x")

    global dados_relatorio
    dados_relatorio = []

    def carregar_dados():
        try:
            filtro = entry_fabricante.get()
            conn = conectar()
            cursor = conn.cursor()

            if filtro:
                cursor.execute("""
                    SELECT id, nome, fabricante, quantidade, estoque_minimo
                    FROM produtos
                    WHERE quantidade < estoque_minimo AND fabricante LIKE %s
                    ORDER BY nome
                """, (f"%{filtro}%",))
            else:
                cursor.execute("""
                    SELECT id, nome, fabricante, quantidade, estoque_minimo
                    FROM produtos
                    WHERE quantidade < estoque_minimo
                    ORDER BY nome
                """)

            produtos = cursor.fetchall()
            conn.close()

            dados_relatorio.clear()
            dados_relatorio.extend(produtos)

            for item in tabela.get_children():
                tabela.delete(item)

            if produtos:
                for p in produtos:
                    tabela.insert("", "end", values=(p[0], p[1], p[2], p[3], p[4]))
            else:
                messagebox.showinfo("Relatório", "Nenhum produto abaixo do estoque mínimo.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar relatório: {str(e)}")

    def exportar_excel():
        try:
            df = pd.DataFrame(dados_relatorio, columns=["ID", "Nome", "Fabricante", "Quantidade", "Estoque Mínimo"])
            df.to_excel("relatorio_estoque_baixo.xlsx", index=False)
            messagebox.showinfo("Exportação", "Relatório exportado para Excel com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao exportar Excel: {str(e)}")

    def gerar_pdf():
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Relatório de Estoque Baixo", ln=True, align="C")
            pdf.ln(10)

            colunas = ["ID", "Nome", "Fabricante", "Qtd", "Mínimo"]
            larguras = [20, 60, 40, 25, 25]

            for i, col in enumerate(colunas):
                pdf.cell(larguras[i], 10, col, border=1)
            pdf.ln()

            for linha in dados_relatorio:
                for i, valor in enumerate(linha):
                    pdf.cell(larguras[i], 10, str(valor), border=1)
                pdf.ln()

            pdf.output("relatorio_estoque_baixo.pdf")
            messagebox.showinfo("Exportação", "Relatório PDF gerado com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao gerar PDF: {str(e)}")

    def voltar():
        from views.menu_view import carregar_menu
        carregar_menu(root)

    botoes = ttk.Frame(frame)
    botoes.pack(pady=20)

    ttk.Button(botoes, text="Atualizar Relatório", command=carregar_dados).grid(row=0, column=0, padx=5)
    ttk.Button(botoes, text="Exportar Excel", command=exportar_excel).grid(row=0, column=1, padx=5)
    ttk.Button(botoes, text="Gerar PDF", command=gerar_pdf).grid(row=0, column=2, padx=5)
    ttk.Button(botoes, text="Voltar", command=voltar).grid(row=0, column=3, padx=5)

    carregar_dados()