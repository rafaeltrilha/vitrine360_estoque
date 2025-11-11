import tkinter as tk
from tkinter import messagebox
from controllers.estoque_controller import baixar_estoque
from utils.alerta import verificar_alerta

def abrir_baixa():
    janela = tk.Toplevel()
    janela.title("Baixa de Estoque")

    tk.Label(janela, text="ID do Produto").grid(row=0, column=0)
    entry_id = tk.Entry(janela)
    entry_id.grid(row=0, column=1)

    tk.Label(janela, text="Quantidade a Baixar").grid(row=1, column=0)
    entry_qtd = tk.Entry(janela)
    entry_qtd.grid(row=1, column=1)

    def baixar():
        try:
            produto_id = int(entry_id.get())
            qtd_baixa = int(entry_qtd.get())
            resultado = baixar_estoque(produto_id, qtd_baixa)

            if isinstance(resultado, int):
                alerta = verificar_alerta(resultado)
                if alerta:
                    messagebox.showwarning("Alerta", alerta)
                else:
                    messagebox.showinfo("Sucesso", "Baixa realizada com sucesso.")
            else:
                messagebox.showerror("Erro", resultado)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    tk.Button(janela, text="Lançar Baixa", command=baixar).grid(row=2, columnspan=2)