from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from openpyxl import Workbook
from db.connection import conectar

def gerar_relatorio_pdf():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    conn.close()

    c = canvas.Canvas("relatorio.pdf", pagesize=A4)
    c.drawString(100, 800, "Relatório de Estoque - Vitrine360")

    y = 760
    for p in produtos:
        texto = f"ID: {p[0]} | Nome: {p[1]} | Fabricante: {p[2]} | Modelo: {p[3]} | Qtd: {p[5]}"
        c.drawString(100, y, texto)
        y -= 20
        if y < 50:
            c.showPage()
            y = 800

    c.save()

def gerar_relatorio_excel():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    conn.close()

    wb = Workbook()
    ws = wb.active
    ws.title = "Estoque Vitrine360"
    ws.append(["ID", "Nome", "Fabricante", "Modelo", "Descrição", "Quantidade"])

    for p in produtos:
        ws.append(list(p))

    wb.save("relatorio.xlsx")