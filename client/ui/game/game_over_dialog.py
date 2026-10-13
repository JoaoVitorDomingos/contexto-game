"""Janela apresentada quando o jogador desiste da partida."""

import tkinter as tk
from tkinter import ttk


class GameOverDialog(tk.Toplevel):
    """Exibe a palavra secreta e as palavras mais próximas retornadas pelo servidor."""

    def __init__(self, parent, palavra, palavras_proximas, screen):
        super().__init__(parent)
        self.screen = screen
        self.title("Partida encerrada")
        self.geometry("780x680")
        self.minsize(650, 550)
        self.configure(bg=screen.BG)
        self.transient(parent.winfo_toplevel())
        self.grab_set()
        self._criar_interface(palavra, palavras_proximas)

    def _criar_interface(self, palavra, palavras_proximas):
        screen = self.screen
        tk.Label(self, text="PARTIDA ENCERRADA", font=("Arial", 11, "bold"), bg=screen.BG, fg=screen.PURPLE).pack(pady=(25, 3))
        tk.Label(self, text="Você desistiu da partida", font=("Arial", 22, "bold"), bg=screen.BG, fg=screen.WHITE).pack()

        quadro = tk.Frame(self, bg="#351827", highlightbackground="#7f1d1d", highlightthickness=1)
        quadro.pack(fill="x", padx=35, pady=20)
        tk.Label(quadro, text="A PALAVRA SECRETA ERA", font=("Arial", 9, "bold"), bg="#351827", fg="#fca5a5").pack(pady=(15, 4))
        tk.Label(quadro, text=str(palavra).upper(), font=("Arial", 28, "bold"), bg="#351827", fg="#f87171").pack(pady=(0, 15))

        tk.Label(self, text="30 palavras mais próximas", font=("Arial", 14, "bold"), bg=screen.BG, fg=screen.WHITE).pack(anchor="w", padx=35, pady=(0, 10))
        quadro_tabela = tk.Frame(self, bg=screen.PANEL, highlightbackground=screen.BORDER, highlightthickness=1)
        quadro_tabela.pack(fill="both", expand=True, padx=35, pady=(0, 15))
        colunas = ("posicao", "palavra", "proximidade")
        tabela = ttk.Treeview(quadro_tabela, columns=colunas, show="headings")
        for coluna, titulo, largura in (("posicao", "POSIÇÃO", 120), ("palavra", "PALAVRA", 300), ("proximidade", "PROXIMIDADE", 160)):
            tabela.heading(coluna, text=titulo)
            tabela.column(coluna, width=largura, anchor="center")
        barra = ttk.Scrollbar(quadro_tabela, orient="vertical", command=tabela.yview)
        tabela.configure(yscrollcommand=barra.set)
        tabela.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

        for item in palavras_proximas:
            posicao = item.get("posicao", "-")
            proximidade = item.get("proximidade", item.get("similaridade", "-"))
            tabela.insert("", "end", values=(f"#{posicao}", item.get("palavra", ""), screen._formatar_proximidade(proximidade)))

        tk.Button(self, text="FECHAR", width=15, font=("Arial", 10, "bold"), bg=screen.PANEL_LIGHT, fg=screen.WHITE, activebackground=screen.BORDER, activeforeground=screen.WHITE, relief="flat", bd=0, cursor="hand2", command=self.destroy).pack(pady=(0, 20), ipady=7)
